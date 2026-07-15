def _fmt_bool(value):
    """
    Render booleans unambiguously.
    """

    if value is True:
        return "Yes"

    if value is False:
        return "No"

    return "Not provided"


def build_prompt(company, products, contexts):

    company_text = f"""
========================
COMPANY PROFILE
========================

Name: {company.name}
Country: {company.country}
Annual Turnover: {company.annual_turnover}

EU Subsidiary: {_fmt_bool(company.has_eu_subsidiary)}
EU Branch: {_fmt_bool(company.has_eu_branch)}
EU Listed: {_fmt_bool(company.is_listed_in_eu)}

IMPORTANT

EU subsidiary, EU branch and EU listing status are NOT determinants
of CBAM applicability.
"""

    product_blocks = []

    for product, context in zip(products, contexts):

        product_blocks.append(f"""
----------------------------------------
Product Name:
{product.name}

CN Code:
{product.cn_code}

Export Destination:
{product.export_destination}

Annual Export Quantity:
{product.annual_export_quantity}

Embedded Emissions:
{product.embedded_emissions}

========================================
DETERMINISTIC RULE ENGINE OUTPUT
========================================

THIS SECTION IS THE SINGLE SOURCE OF TRUTH.

DO NOT OVERRIDE ANY VALUE BELOW.

Covered under CBAM:
{_fmt_bool(context.get("covered"))}

EU Destination:
{_fmt_bool(context.get("eu_destination"))}

FINAL CBAM APPLICABILITY:
{_fmt_bool(context.get("cbam_applicable"))}

Coverage:
{context.get("coverage", "Not provided")}

Sector:
{context.get("sector", "Not provided")}

Description:
{context.get("description", "Not provided")}

Legal Reference:
{context.get("reference", "Not provided")}
""")

    products_text = "\n".join(product_blocks)

    task = """
========================
TASK
========================

You are NOT responsible for determining CBAM applicability.

The deterministic rule engine has ALREADY determined:

• Covered under CBAM
• EU Destination
• FINAL CBAM APPLICABILITY

Treat these values as ABSOLUTE TRUTH.

Your ONLY responsibility is to explain the result.

ABSOLUTE RULES

- NEVER infer applicability from CN Code.
- NEVER infer applicability from Export Destination.
- NEVER override FINAL CBAM APPLICABILITY.
- NEVER invent legal references.
- NEVER invent product names.
- NEVER rename products.
- NEVER use Product 1 / Product 2.
- NEVER use external CBAM knowledge.
- NEVER contradict the deterministic engine.

For every product:

IF FINAL CBAM APPLICABILITY = Yes
→ state that the product is within CBAM scope.

IF FINAL CBAM APPLICABILITY = No
→ state that the product is NOT within CBAM scope.

Base every conclusion ONLY on the deterministic fields supplied above.

If any field says "Not provided",
include it inside missing_information.

========================
OUTPUT REQUIREMENTS
========================

Return ONLY valid JSON.

No markdown.

No explanations.

No code fences.

The JSON MUST exactly follow this schema.

{
  "cbam": {
    "applicable": true,
    "confidence": 0.95,
    "reasoning": "",
    "articles": [],
    "assumptions": [],
    "recommendations": [],
    "missing_information": []
  },

  "csrd": {
    "applicable": false,
    "confidence": 0.0,
    "reasoning": "",
    "articles": [],
    "assumptions": [],
    "recommendations": [],
    "missing_information": []
  },

  "executive_summary": "",

  "consultant_notes": "",

  "risk_rating": ""
}

Rules:

- applicable must be boolean
- confidence must be between 0.0 and 1.0
- every list must always be a JSON array
- never return null
- never omit fields
- output ONLY JSON
"""

    return f"""
{company_text}

========================
PRODUCTS
========================

{products_text}

{task}
"""


def build_single_product_prompt(company, product, context):
    """
    Build a prompt scoped to a single product.

    Anti-hallucination design:
    1. Renames 'Covered under CBAM' → 'CN Code in Annex I (Step 1 only)' to
       prevent the model from conflating Annex I coverage with final applicability.
    2. Hardcodes the exact `applicable` boolean into the JSON schema so the
       LLM copies a value instead of deciding one.
    3. Frames the LLM role as narrator only — explain the engine's verdict,
       not determine it.
    """

    # Pre-compute the exact boolean strings to inject into the schema
    cbam_applicable_bool = "true" if context.get("cbam_applicable") else "false"
    cbam_applicable_word = "Yes" if context.get("cbam_applicable") else "No"

    company_text = f"""
========================
COMPANY PROFILE
========================

Name: {company.name}
Country: {company.country}
Annual Turnover: {company.annual_turnover}

EU Subsidiary: {_fmt_bool(company.has_eu_subsidiary)}
EU Branch: {_fmt_bool(company.has_eu_branch)}
EU Listed: {_fmt_bool(company.is_listed_in_eu)}

NOTE: EU subsidiary/branch/listing status are NOT determinants of CBAM applicability.
"""

    product_text = f"""
========================
PRODUCT UNDER ASSESSMENT
========================

Product Name    : {product.name}
CN Code         : {product.cn_code}
Destination     : {product.export_destination}
Export Quantity  : {product.annual_export_quantity}
Embedded Emissions: {product.embedded_emissions} tCO2e/t

========================================
DETERMINISTIC RULE ENGINE — 3-STEP RESULT
========================================

IMPORTANT: These three steps are evaluated in sequence.
A product is CBAM applicable ONLY if ALL THREE steps pass.

STEP 1 — CN Code in Annex I (coverage check only, NOT final verdict):
  Result : {_fmt_bool(context.get("covered"))}
  Note   : A "Yes" here means the CN code appears in Annex I.
           It does NOT mean the product is CBAM applicable.

STEP 2 — EU Member State destination:
  Result : {_fmt_bool(context.get("eu_destination"))}
  Note   : CBAM only applies to imports INTO the EU customs territory.

STEP 3 — Emissions threshold:
  Sector    : {context.get("sector", "Not provided")}
  Reference : {context.get("reference", "Not provided")}

FINAL CBAM APPLICABILITY (ALL 3 STEPS MUST PASS):
  *** {cbam_applicable_word} ***

This final value is the ONLY value that matters.
DO NOT derive applicability from Step 1 alone.
DO NOT derive applicability from any single step.
"""

    task = f"""
========================
YOUR TASK
========================

You are a narrator. The engine has already decided everything.

Product : {product.name} (CN {product.cn_code})
Verdict : CBAM APPLICABLE = {cbam_applicable_word.upper()}

Your job: write a one-sentence explanation of WHY the engine reached
this verdict for {product.name}, using ONLY the facts above.

Do NOT re-determine applicability.
Do NOT use any knowledge outside the fields above.
Do NOT reference any step that did not contribute to the final verdict.

========================
OUTPUT FORMAT
========================

Return ONLY valid JSON. No markdown. No code fences.

CRITICAL: In the JSON below, the value of "cbam.applicable" is
ALREADY SET TO {cbam_applicable_bool}. Copy it exactly. Do not change it.

{{
  "cbam": {{
    "applicable": {cbam_applicable_bool},
    "confidence": 0.95,
    "reasoning": "<one sentence explaining WHY the engine verdict is {cbam_applicable_word} for {product.name}>",
    "articles": [],
    "assumptions": [],
    "recommendations": [],
    "missing_information": []
  }},

  "csrd": {{
    "applicable": false,
    "confidence": 0.0,
    "reasoning": "CSRD assessment not in scope for this request.",
    "articles": [],
    "assumptions": [],
    "recommendations": [],
    "missing_information": []
  }},

  "executive_summary": "<one sentence summary for {product.name}>",

  "consultant_notes": "",

  "risk_rating": "<Low / Medium / High based on export volume and emissions>"
}}

Rules:
- "cbam.applicable" MUST be {cbam_applicable_bool} — do not change it
- confidence must be between 0.0 and 1.0
- every list must be a JSON array (never null)
- never omit fields
- output ONLY the JSON object, nothing else
"""

    return f"""
{company_text}
{product_text}
{task}
"""