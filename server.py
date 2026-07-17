import os
import json
from flask import Flask, render_template, request, Response, jsonify
from engine.cbam_engine import CBAMEngine
from engine.models import Company, Product
from agent.orchestrator import AIOrchestrator, SYSTEM_PROMPT
from agent.prompt_builder import build_single_product_prompt
from agent.output_parser import OutputParser

app = Flask(__name__, template_folder="templates")

# Initialize Engine for lookup operations
engine = CBAMEngine()

@app.route("/")
def home():
    """Serve the dashboard UI."""
    return render_template("index.html")

@app.route("/api/config", methods=["GET"])
def get_config():
    """Return active LLM Configuration summary."""
    try:
        orchestrator = AIOrchestrator()
        llm_desc = orchestrator.client.describe()
        return jsonify({"llm_config": llm_desc})
    except Exception as e:
        return jsonify({"llm_config": f"Error loading client: {str(e)}"}), 500

@app.route("/api/eu-countries", methods=["GET"])
def get_eu_countries():
    """Return dictionary of EU member states."""
    return jsonify(engine.eu_countries)

@app.route("/api/cn-lookup", methods=["GET"])
def cn_lookup():
    """
    Search CBAM Annex I codes by prefix or keywords.
    Matches against code prefix, description, or sector.
    """
    query = request.args.get("q", "").strip().lower()
    if not query:
        return jsonify([])

    matches = []
    # Search all rules loaded in the engine
    for rule in engine.cbam_rules:
        prefix = rule["prefix"].lower()
        
        # Bi-directional prefix matching
        prefix_match = False
        if rule["match_type"] == "PREFIX":
            if query.startswith(prefix) or prefix.startswith(query):
                prefix_match = True
        else: # EXACT
            if query == prefix or prefix.startswith(query):
                prefix_match = True

        desc_match = query in rule["description"].lower()
        sector_match = query in rule["sector"].lower()

        if prefix_match or desc_match or sector_match:
            matches.append({
                "prefix": rule["prefix"],
                "match_type": rule["match_type"],
                "coverage": rule["coverage"],
                "description": rule["description"],
                "sector": rule["sector"],
                "reference": rule["reference"]
            })
            
            # Limit search results to first 12 matches for responsiveness
            if len(matches) >= 12:
                break

    return jsonify(matches)

@app.route("/api/assess", methods=["POST"])
def assess_cbam():
    """
    Evaluate products and stream JSON chunk logs as they complete (NDJSON).
    Returns intermediate progress states, then streams the final evaluations.
    """
    data = request.json
    if not data:
        return jsonify({"error": "Missing request payload"}), 400

    company_data = data.get("company", {})
    products_data = data.get("products", [])

    company = Company(
        name=company_data.get("name", ""),
        country=company_data.get("country", ""),
        annual_turnover=int(company_data.get("annual_turnover") or 0),
        has_eu_subsidiary=bool(company_data.get("has_eu_subsidiary")),
        has_eu_branch=bool(company_data.get("has_eu_branch")),
        is_listed_in_eu=bool(company_data.get("is_listed_in_eu"))
    )

    def generate_events():
        orchestrator = AIOrchestrator()
        parser = OutputParser()

        # 1. Yield init header details
        llm_desc = orchestrator.client.describe()
        yield json.dumps({"type": "init", "llm_config": llm_desc}) + "\n"

        # 2. Iterate and evaluate each product
        for idx, p_data in enumerate(products_data):
            p_name = p_data.get("name") or f"Product {idx + 1}"
            p_cn = p_data.get("cn_code", "").replace(" ", "").strip()
            p_dest = p_data.get("export_destination", "").strip()
            
            # Extract quantity and emissions values safely
            qty_raw = p_data.get("annual_export_quantity")
            qty = float(qty_raw) if qty_raw not in (None, "") else 0.0
            
            emissions_raw = p_data.get("embedded_emissions")
            emissions = float(emissions_raw) if emissions_raw not in (None, "") else None

            # Strict Backend Override: Force product name to match the official database description
            ctx = engine.get_product_context(p_cn)
            if ctx and ctx.get("description"):
                official_desc = ctx["description"].split(";")[0].split(",")[0].strip()
                p_name = f"{official_desc} (CN {p_cn})"
            else:
                p_name = f"Unmapped Commodity (CN {p_cn})"

            product = Product(
                name=p_name,
                cn_code=p_cn,
                export_destination=p_dest,
                annual_export_quantity=qty,
                embedded_emissions=emissions
            )

            # A. Rule Engine Check
            decision = engine.assess_product_cbam(product)
            yield json.dumps({
                "type": "progress",
                "product_index": idx,
                "product_name": p_name,
                "status": "Deterministic rules assessed"
            }) + "\n"

            # B. AI reasoning check
            context = orchestrator._build_context(product)
            prompt = build_single_product_prompt(company, product, context)
            
            yield json.dumps({
                "type": "progress",
                "product_index": idx,
                "product_name": p_name,
                "status": "Calling AI reasoning pipeline..."
            }) + "\n"

            try:
                raw_json = orchestrator.client.chat(
                    system_prompt=SYSTEM_PROMPT,
                    user_prompt=prompt,
                    format="json",
                    think=False
                )
                assessment = parser.parse(raw_json)

                llm_said_applicable = assessment.cbam.applicable
                authoritative = decision.cbam_applicable
                llm_overrode = llm_said_applicable != authoritative

                ai_data = {
                    "applicable": authoritative, # Override LLM with deterministic engine
                    "llm_overrode": llm_overrode,
                    "confidence": assessment.cbam.confidence,
                    "reasoning": assessment.cbam.reasoning,
                    "articles": assessment.cbam.articles,
                    "recommendations": assessment.cbam.recommendations,
                    "missing_information": assessment.cbam.missing_information,
                    "risk_rating": assessment.risk_rating or "Low"
                }

            except Exception as e:
                # Handle timeout/LLM issues gracefully
                ai_data = {
                    "applicable": decision.cbam_applicable,
                    "llm_overrode": False,
                    "confidence": 0.50,
                    "reasoning": f"AI narrative generation failed: {str(e)}",
                    "articles": [],
                    "recommendations": ["Consult regulatory advisor due to processing error."],
                    "missing_information": [],
                    "risk_rating": "Medium"
                }

            # C. Yield product result
            yield json.dumps({
                "type": "product_result",
                "product_index": idx,
                "product_name": p_name,
                "decision": {
                    "product_name": decision.product_name,
                    "cn_code": decision.cn_code,
                    "destination": decision.destination,
                    "cbam_applicable": decision.cbam_applicable,
                    "decision_reason": decision.decision_reason,
                    "sector": decision.sector,
                    "description": decision.description,
                    "legal_reference": decision.legal_reference,
                    "checks": [
                        {
                            "rule": c.rule,
                            "result": c.result,
                            "detail": c.detail,
                            "rule_reference": c.rule_reference
                        } for c in decision.checks
                    ]
                },
                "ai": ai_data
            }) + "\n"

        yield json.dumps({"type": "complete"}) + "\n"

    return Response(generate_events(), mimetype="application/x-ndjson")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Open to external access
    app.run(host="0.0.0.0", port=port, debug=True)
