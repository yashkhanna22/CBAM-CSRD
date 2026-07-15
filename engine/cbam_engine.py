from engine.data_loader import load_cbam_rules, load_eu_countries
from engine.models import RuleCheck, ProductCBAMDecision

# ---------------------------------------------------------------------------
# Emission intensity thresholds (tCO2e per tonne of product) used as a
# practical de-minimis filter. These are indicative values for the demo;
# in production these come from Commission Implementing Regulation data.
# ---------------------------------------------------------------------------
EMISSION_THRESHOLDS = {
    "Iron and Steel":   0.0,   # No de-minimis — all quantities are in scope
    "Aluminium":        0.0,
    "Cement":           0.0,
    "Fertilisers":      0.0,
    "Electricity":      0.0,
    "Hydrogen":         0.0,
}


class CBAMEngine:
    """
    Deterministic CBAM Tool Layer.

    This class does NOT determine regulatory applicability.

    It only provides deterministic lookups that can be used
    by the Regulatory Intelligence Agent (LLM).
    """

    def __init__(self):
        self.cbam_rules = load_cbam_rules()
        self.eu_countries = load_eu_countries()

    def is_cbam_product(self, cn_code: str) -> bool:
        """
        Check whether a CN code is covered under CBAM.
        """

        cn_code = cn_code.replace(" ", "").strip()

        # Check exclusion rules first
        for rule in self.cbam_rules:

            if rule["coverage"] != "EXCLUDE":
                continue

            if rule["match_type"] == "EXACT":
                if cn_code == rule["prefix"]:
                    return False

            elif rule["match_type"] == "PREFIX":
                if cn_code.startswith(rule["prefix"]):
                    return False

        # Check inclusion rules
        for rule in self.cbam_rules:

            if rule["coverage"] != "INCLUDE":
                continue

            if rule["match_type"] == "EXACT":
                if cn_code == rule["prefix"]:
                    return True

            elif rule["match_type"] == "PREFIX":
                if cn_code.startswith(rule["prefix"]):
                    return True

        return False

    def is_eu_destination(self, country: str) -> bool:
        """
        Check whether a destination country is an EU Member State.
        Accepts either ISO codes (DE) or country names (Germany).
        """

        country = country.strip()

        if country.upper() in self.eu_countries:
            return True

        return country.title() in self.eu_countries.values()

    def get_sector(self, cn_code: str):
        """
        Return the CBAM sector for a CN code.
        """

        cn_code = cn_code.replace(" ", "").strip()

        for rule in self.cbam_rules:

            if rule["match_type"] == "EXACT":
                matched = cn_code == rule["prefix"]

            else:
                matched = cn_code.startswith(rule["prefix"])

            if matched:
                return rule["sector"]

        return None

    def get_reference(self, cn_code: str):
        """
        Return the regulatory reference associated with a CN code.
        """

        cn_code = cn_code.replace(" ", "").strip()

        for rule in self.cbam_rules:

            if rule["match_type"] == "EXACT":
                matched = cn_code == rule["prefix"]

            else:
                matched = cn_code.startswith(rule["prefix"])

            if matched:
                return rule["reference"]

        return None

    def get_product_context(self, cn_code: str):
        """
        Return complete deterministic information for a CN code.

        This method is intended to be used by the LLM during reasoning.
        """

        cn_code = cn_code.replace(" ", "").strip()

        for rule in self.cbam_rules:

            if rule["match_type"] == "EXACT":
                matched = cn_code == rule["prefix"]

            else:
                matched = cn_code.startswith(rule["prefix"])

            if matched:
                return {
                    "cn_code": cn_code,
                    "covered": rule["coverage"] == "INCLUDE",
                    "coverage": rule["coverage"],
                    "sector": rule["sector"],
                    "description": rule["description"],
                    "reference": rule["reference"],
                    "match_type": rule["match_type"],
                }

        return {
            "cn_code": cn_code,
            "covered": False,
            "coverage": "UNKNOWN",
            "sector": None,
            "description": None,
            "reference": None,
            "match_type": None,
        }

    # -------------------------------------------------------------------------
    # MAIN ENTRY POINT: 3-step rule chain
    # -------------------------------------------------------------------------

    def assess_product_cbam(self, product) -> ProductCBAMDecision:
        """
        Run the deterministic 3-step CBAM rule chain for a single product.

        Step 1 — CN Code Coverage    : Is the CN code listed in CBAM Annex I?
        Step 2 — EU Destination      : Is the export destination an EU Member State?
        Step 3 — Emission Threshold  : Are embedded emissions above the de-minimis threshold?

        Short-circuit logic: if a step fails, later steps are marked NOT EVALUATED.
        """

        cn_code = product.cn_code
        destination = product.export_destination
        embedded_emissions = getattr(product, "embedded_emissions", None)

        ctx = self.get_product_context(cn_code)
        checks: list[RuleCheck] = []

        # ------------------------------------------------------------------
        # STEP 1 — CN Code Coverage
        # Use is_cbam_product() as the authoritative check — it correctly
        # evaluates exclusion rules BEFORE inclusion rules (prefix-72 ferro
        # alloy exceptions, etc.). get_product_context() is only used for
        # display metadata (sector, description, legal reference).
        # ------------------------------------------------------------------
        covered = self.is_cbam_product(cn_code)   # <-- correct exclusion logic
        sector      = ctx.get("sector")
        description = ctx.get("description")
        reference   = ctx.get("reference")

        if covered:
            step1 = RuleCheck(
                rule="Rule 1 — CN Code Coverage (CBAM Annex I)",
                result=True,
                detail=(
                    f"CN {cn_code} is covered under CBAM Annex I "
                    f"({sector or 'Unknown sector'}). "
                    f"{description or ''}"
                ).strip(),
                rule_reference=reference,
            )
        else:
            step1 = RuleCheck(
                rule="Rule 1 — CN Code Coverage (CBAM Annex I)",
                result=False,
                detail=(
                    f"CN {cn_code} is NOT listed in CBAM Annex I "
                    f"(or is explicitly excluded). Product is outside CBAM scope."
                ),
                rule_reference=reference,
            )

        checks.append(step1)

        # Short-circuit: CN code not covered → CBAM not applicable
        if not covered:
            return ProductCBAMDecision(
                product_name=product.name,
                cn_code=cn_code,
                destination=destination,
                checks=checks + [
                    RuleCheck(
                        rule="Rule 2 — EU Destination Check",
                        result=False,
                        detail="Not evaluated — product failed Rule 1.",
                    ),
                    RuleCheck(
                        rule="Rule 3 — Emission Threshold Check",
                        result=False,
                        detail="Not evaluated — product failed Rule 1.",
                    ),
                ],
                cbam_applicable=False,
                decision_reason=(
                    f"CBAM NOT APPLICABLE: CN {cn_code} is not covered under CBAM Annex I."
                ),
                sector=sector,
                description=description,
                legal_reference=reference,
            )

        # ------------------------------------------------------------------
        # STEP 2 — EU Destination
        # ------------------------------------------------------------------
        is_eu = self.is_eu_destination(destination)

        if is_eu:
            step2 = RuleCheck(
                rule="Rule 2 — EU Destination Check",
                result=True,
                detail=(
                    f"Destination '{destination}' is confirmed as an EU Member State. "
                    f"CBAM applies to goods imported into the EU customs territory."
                ),
                rule_reference="CBAM Regulation (EU) 2023/956, Article 2",
            )
        else:
            step2 = RuleCheck(
                rule="Rule 2 — EU Destination Check",
                result=False,
                detail=(
                    f"Destination '{destination}' is NOT an EU Member State. "
                    f"CBAM only applies to imports into the EU customs territory."
                ),
                rule_reference="CBAM Regulation (EU) 2023/956, Article 2",
            )

        checks.append(step2)

        # Short-circuit: not EU destination → CBAM not applicable
        if not is_eu:
            return ProductCBAMDecision(
                product_name=product.name,
                cn_code=cn_code,
                destination=destination,
                checks=checks + [
                    RuleCheck(
                        rule="Rule 3 — Emission Threshold Check",
                        result=False,
                        detail="Not evaluated — product failed Rule 2.",
                    ),
                ],
                cbam_applicable=False,
                decision_reason=(
                    f"CBAM NOT APPLICABLE: Destination '{destination}' is not an EU Member State."
                ),
                sector=sector,
                description=description,
                legal_reference=reference,
            )

        # ------------------------------------------------------------------
        # STEP 3 — Emission Threshold
        # ------------------------------------------------------------------
        threshold = EMISSION_THRESHOLDS.get(sector, 0.0)

        if embedded_emissions is None:
            step3 = RuleCheck(
                rule="Rule 3 — Emission Threshold Check",
                result=True,   # conservative: assume in scope when unknown
                detail=(
                    "Embedded emissions not provided. "
                    "Conservatively treated as in scope pending verified data."
                ),
                rule_reference="CBAM Regulation (EU) 2023/956, Annex III",
            )
            above_threshold = True
        elif embedded_emissions > threshold:
            step3 = RuleCheck(
                rule="Rule 3 — Emission Threshold Check",
                result=True,
                detail=(
                    f"Embedded emissions {embedded_emissions} tCO₂e/t exceed the "
                    f"de-minimis threshold of {threshold} tCO₂e/t for sector '{sector}'. "
                    f"Product is within CBAM scope."
                ),
                rule_reference="CBAM Regulation (EU) 2023/956, Annex III",
            )
            above_threshold = True
        else:
            step3 = RuleCheck(
                rule="Rule 3 — Emission Threshold Check",
                result=False,
                detail=(
                    f"Embedded emissions {embedded_emissions} tCO₂e/t are at or below "
                    f"the de-minimis threshold of {threshold} tCO₂e/t for sector '{sector}'."
                ),
                rule_reference="CBAM Regulation (EU) 2023/956, Annex III",
            )
            above_threshold = False

        checks.append(step3)

        applicable = covered and is_eu and above_threshold

        if applicable:
            reason = (
                f"CBAM APPLICABLE: CN {cn_code} ({sector}) exported to {destination} (EU) "
                f"with embedded emissions {embedded_emissions} tCO₂e/t. "
                f"All three applicability rules satisfied."
            )
        else:
            reason = (
                f"CBAM NOT APPLICABLE: Embedded emissions {embedded_emissions} tCO₂e/t "
                f"do not exceed the threshold for sector '{sector}'."
            )

        return ProductCBAMDecision(
            product_name=product.name,
            cn_code=cn_code,
            destination=destination,
            checks=checks,
            cbam_applicable=applicable,
            decision_reason=reason,
            sector=sector,
            description=description,
            legal_reference=reference,
        )