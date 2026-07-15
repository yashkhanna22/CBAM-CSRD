import json
import csv
from pathlib import Path

# =============================================================================
# PATH CONFIGURATION
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

KNOWLEDGE_DIR = BASE_DIR / "knowledge"


# =============================================================================
# REFERENCE DATA LOADERS
# =============================================================================

def load_cbam_rules():
    """
    Load all CBAM Annex-I CN code rules from the CSV.
    """

    csv_path = DATA_DIR / "cbam_annex1_cn_codes.csv"

    rules = []

    with open(csv_path, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rules.append({
                "prefix": row["CN_Prefix"].strip(),
                "match_type": row["Match_Type"].strip(),
                "coverage": row["Coverage"].strip(),
                "description": row["Description"].strip(),
                "sector": row["Sector"].strip(),
                "reference": row["Reference"].strip()
            })

    return rules


def load_eu_countries():
    """
    Load EU country codes and names.
    """

    json_path = DATA_DIR / "eu_countries.json"

    with open(json_path, "r", encoding="utf-8") as file:
        return json.load(file)


# =============================================================================
# KNOWLEDGE LOADERS
# =============================================================================

def load_markdown(filename: str) -> str:
    """
    Load any markdown file from the knowledge folder.
    """

    md_path = KNOWLEDGE_DIR / filename

    with open(md_path, "r", encoding="utf-8") as file:
        return file.read()


def load_cbam_knowledge():
    """
    Load CBAM knowledge base.
    """

    return load_markdown("cbam.md")


def load_csrd_knowledge():
    """
    Load CSRD knowledge base.
    """

    return load_markdown("csrd.md")


def load_all_knowledge():
    """
    Load every markdown knowledge file.

    Returns:
        {
            "cbam": "...",
            "csrd": "...",
            ...
        }
    """

    knowledge = {}

    for file in KNOWLEDGE_DIR.glob("*.md"):
        knowledge[file.stem] = file.read_text(encoding="utf-8")

    return knowledge
