from agent.llm_client import LLMClient
from agent.prompt_builder import build_prompt, build_single_product_prompt
from engine.cbam_engine import CBAMEngine


DEBUG = False

SYSTEM_PROMPT = """
You are a senior PwC regulatory consultant specializing in the EU Carbon Border Adjustment Mechanism (CBAM).

The deterministic Python rule engine has ALREADY determined:

- Product coverage
- EU destination
- CBAM applicability

Treat these values as FINAL.

Never override them.

Never infer new facts.

Use ONLY the supplied deterministic information.

Return ONLY valid JSON.
"""


class AIOrchestrator:

    def __init__(self):
        self.engine = CBAMEngine()
        self.client = LLMClient()

    def _build_context(self, product):
        """
        Build deterministic context for a single product.
        Uses is_cbam_product() so exclusion rules are respected.
        """
        context = self.engine.get_product_context(product.cn_code)

        context["product_name"]       = product.name
        context["destination"]        = product.export_destination
        context["export_quantity"]    = product.annual_export_quantity
        context["embedded_emissions"] = product.embedded_emissions

        context["eu_destination"] = self.engine.is_eu_destination(
            product.export_destination
        )

        # Authoritative flag — uses exclusion-aware is_cbam_product()
        context["covered"] = self.engine.is_cbam_product(product.cn_code)

        context["cbam_applicable"] = (
            context["covered"] and context["eu_destination"]
        )

        return context

    # -------------------------------------------------------------------------
    # BATCH: one LLM call for all products (kept for backward compat)
    # -------------------------------------------------------------------------

    def assess(self, company, products):

        print("Step 1: Building product contexts...")

        contexts = [self._build_context(p) for p in products]

        print("✓ Product contexts built")

        if DEBUG:
            print("\n========== CONTEXT SENT ==========\n")
            for context in contexts:
                print(context)
            print("\n==================================\n")

        print("Step 2: Building prompt...")

        prompt = build_prompt(company, products, contexts)

        print("✓ Prompt built")

        if DEBUG:
            print(f"Prompt length: {len(prompt)} characters")
            print("\n========== PROMPT SENT ==========\n")
            print(prompt)
            print("\n=================================\n")

        print("Step 3: Calling Ollama...")

        answer = self.client.chat(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
            format="json",
            think=False,
        )

        print("✓ Response received from Ollama")

        if DEBUG:
            print("\n========== RAW MODEL OUTPUT ==========\n")
            print(answer)
            print("\n======================================\n")

        return answer

    # -------------------------------------------------------------------------
    # PER-PRODUCT: one LLM call per product → list of (product, raw_json)
    # -------------------------------------------------------------------------

    def assess_each(self, company, products):
        """
        Run one LLM call per product.

        Returns:
            list of (Product, str)  — each str is the raw JSON from the LLM.
        """

        print(f"\nGenerating AI narrative for {len(products)} product(s)...\n")

        results = []

        for i, product in enumerate(products, start=1):
            print(f"  [{i}/{len(products)}] Assessing: {product.name} (CN {product.cn_code})...")

            context = self._build_context(product)

            prompt = build_single_product_prompt(company, product, context)

            if DEBUG:
                print(f"\n========== PROMPT [{product.name}] ==========\n")
                print(prompt)
                print("\n=============================================\n")

            raw_json = self.client.chat(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=prompt,
                format="json",
                think=False,
            )

            if DEBUG:
                print(f"\n========== RAW OUTPUT [{product.name}] ==========\n")
                print(raw_json)
                print("\n================================================\n")

            results.append((product, raw_json))

            print(f"  ✓ Done: {product.name}")

        print("\n✓ All products assessed\n")

        return results