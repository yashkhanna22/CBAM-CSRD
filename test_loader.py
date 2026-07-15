from engine.data_loader import (
    load_cbam_knowledge,
    load_csrd_knowledge,
    load_cbam_rules,
    load_eu_countries,
)

print("CBAM Rules:", len(load_cbam_rules()))
print("EU Countries:", len(load_eu_countries()))

print(load_cbam_knowledge()[:200])
print(load_csrd_knowledge()[:200])