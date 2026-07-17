from engine.models import Company, Product
from engine.cbam_engine import CBAMEngine
from agent.orchestrator import AIOrchestrator
from agent.output_parser import OutputParser


# =============================================================================
# DISPLAY HELPERS
# =============================================================================

WIDTH = 80


def _rule_icon(result: bool) -> str:
    return "✅ PASS" if result else "❌ FAIL"


def line(char="─", width=WIDTH):
    print(char * width)


def print_product_decision(decision):
    """
    Print the deterministic 3-step CBAM rule chain for a single product.
    """
    print()
    line("═")
    verdict = "✅  CBAM APPLICABLE" if decision.cbam_applicable else "❌  CBAM NOT APPLICABLE"
    print(f"  PRODUCT : {decision.product_name}")
    print(f"  CN Code : {decision.cn_code}   |   Destination : {decision.destination}")
    print(f"  VERDICT : {verdict}")
    line("═")

    for check in decision.checks:
        print(f"\n  {_rule_icon(check.result)}  {check.rule}")
        line("─", WIDTH - 2)
        # Wrap detail text
        words = check.detail.split()
        buf = "     "
        for word in words:
            if len(buf) + len(word) + 1 > 78:
                print(buf)
                buf = "     " + word
            else:
                buf += (" " if buf.strip() else "") + word
        if buf.strip():
            print(buf)
        if check.rule_reference:
            print(f"     📎 {check.rule_reference}")

    print()
    line("─")
    print(f"  Decision Basis : {decision.decision_reason}")
    if decision.sector:
        print(f"  Sector         : {decision.sector}")
    if decision.legal_reference:
        print(f"  Legal Ref      : {decision.legal_reference}")


def print_summary_table(decisions):
    """Compact summary table of all products."""
    print()
    line("═")
    print("  CBAM APPLICABILITY SUMMARY — ALL PRODUCTS")
    line("─")
    header = (
        f"  {'Product':<22}{'CN Code':<12}{'Destination':<14}"
        f"{'Rule 1':<8}{'Rule 2':<8}{'Rule 3':<8}{'Verdict':<20}"
    )
    print(header)
    line("─")
    for d in decisions:
        syms = [("✅" if c.result else "❌") for c in d.checks]
        v = "✅ APPLICABLE" if d.cbam_applicable else "❌ NOT APPLICABLE"
        print(
            f"  {d.product_name[:21]:<22}{d.cn_code:<12}{d.destination[:13]:<14}"
            f"{syms[0]:<8}{syms[1]:<8}{syms[2]:<8}{v}"
        )
    line("═")


def print_cbam_assessment(product, decision, assessment):
    """
    Print the AI-generated CBAM ASSESSMENT for a single product.

    The 'Applicable' field is ALWAYS taken from the deterministic engine
    (decision.cbam_applicable). The LLM provides reasoning text only.
    If the LLM contradicted the engine, an ENGINE OVERRIDE note is shown.
    """
    llm_said_applicable = assessment.cbam.applicable
    authoritative       = decision.cbam_applicable          # engine is truth
    llm_overrode        = llm_said_applicable != authoritative

    print()
    print("CBAM ASSESSMENT")
    line("-")
    print(f"Export         : {product.name}")
    print(f"Applicable     : {authoritative}", end="")
    if llm_overrode:
        print(f"  ⚠️  [ENGINE OVERRIDE — LLM said {llm_said_applicable}, corrected to {authoritative}]")
    else:
        print()
    print(f"Confidence     : {assessment.cbam.confidence:.2f}")
    print(f"Reasoning      : {assessment.cbam.reasoning}")

    if assessment.cbam.articles:
        print(f"Articles       : {', '.join(assessment.cbam.articles)}")
    if assessment.cbam.recommendations:
        print("Recommendations:")
        for r in assessment.cbam.recommendations:
            print(f"  • {r}")
    if assessment.cbam.missing_information:
        print("Missing Info   :")
        for m in assessment.cbam.missing_information:
            print(f"  • {m}")

    print(f"Risk Rating    : {assessment.risk_rating or 'Not provided'}")


def print_list(title, items):
    print(f"\n{title}")
    line("-")
    if items:
        for item in items:
            print(f"  • {item}")
    else:
        print("  None")


# =============================================================================
# MAIN
# =============================================================================

def main():

    company = Company(
        name="ABC Ltd",
        country="India",
        annual_turnover=5_000_000,
        has_eu_subsidiary=False,
        has_eu_branch=False,
        is_listed_in_eu=False,
    )

    products = [

        Product(
            name="Steel Pipe",
            cn_code="73041000",
            export_destination="Germany",
            annual_export_quantity=1000,
            embedded_emissions=2.5,
        ),

        Product(
            name="Ferro Silicon",
            cn_code="72023000",
            export_destination="Germany",
            annual_export_quantity=500,
            embedded_emissions=1.2,
        ),

        Product(
            name="Aluminium Sheet",
            cn_code="76061100",
            export_destination="India",
            annual_export_quantity=800,
            embedded_emissions=3.1,
        ),

    ]

    # ── HEADER ────────────────────────────────────────────────────────────────
    ai     = AIOrchestrator()   # init early so we can show LLM config
    parser = OutputParser()

    print()
    line("═")
    print("  AI-NATIVE REGULATORY INTELLIGENCE PLATFORM")
    print("  CBAM Applicability Assessment")
    line("═")
    print(f"\n  Company    : {company.name}  ({company.country})")
    print(f"  Products   : {len(products)}")
    print(f"  LLM        : {ai.client.describe()}")

    # ── STEP 1: DETERMINISTIC RULE ENGINE ─────────────────────────────────────
    print("\n\n── DETERMINISTIC RULE ENGINE ─────────────────────────────────────────────")

    engine    = CBAMEngine()
    decisions = [engine.assess_product_cbam(p) for p in products]

    # Per-product rule-chain drill-down
    for decision in decisions:
        print_product_decision(decision)

    # Summary table
    print_summary_table(decisions)

    # ── STEP 2: AI NARRATIVE — PER PRODUCT ────────────────────────────────────
    print(f"\n\n── AI NARRATIVE (per product) · {ai.client.describe()} ────────────────────")

    per_product_results = ai.assess_each(company, products)

    # decisions and per_product_results are both ordered by products list
    for (product, raw_json), decision in zip(per_product_results, decisions):
        assessment = parser.parse(raw_json)
        print_cbam_assessment(product, decision, assessment)

    print()
    line("═")
    print("  END OF REPORT")
    line("═")
    print()


if __name__ == "__main__":
    main()