from engine.cbam_engine import CBAMEngine

engine = CBAMEngine()

test_codes = [
    "72072000",  # Should be True
    "72023000",  # Should be False (Excluded)
    "76010000",  # Should be True
    "99999999",  # Should be False
]

for code in test_codes:
    print(f"{code} -> {engine.is_cbam_product(code)}")