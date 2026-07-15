"""
Shared data models for the AI-Native Regulatory Intelligence Platform.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Literal


# =============================================================================
# DOMAIN MODELS
# =============================================================================

@dataclass
class Company:
    name: str
    country: str
    annual_turnover: Optional[float]
    has_eu_subsidiary: bool
    has_eu_branch: bool
    is_listed_in_eu: bool


@dataclass
class Product:
    name: str
    cn_code: str
    export_destination: str
    annual_export_quantity: Optional[float]
    embedded_emissions: Optional[float]


# =============================================================================
# LEGACY MODEL
# =============================================================================

@dataclass
class AssessmentResult:
    applicable: bool
    reason: str
    triggers: List[str]
    financial_impact: dict[str, float]


# =============================================================================
# AI INPUT
# =============================================================================

@dataclass
class AssessmentInput:
    company: Company
    products: List[Product]


# =============================================================================
# CBAM RULE CHAIN (deterministic, per-product)
# =============================================================================

@dataclass
class RuleCheck:
    """
    Result of a single deterministic CBAM rule check.
    """
    rule: str                          # Human-readable rule label
    result: bool                       # True = passes / applicable
    detail: str                        # One-line explanation
    rule_reference: Optional[str] = None  # Legal citation if available


@dataclass
class ProductCBAMDecision:
    """
    Full deterministic CBAM decision for a single product.
    Contains the ordered rule chain and a final verdict.
    """
    product_name: str
    cn_code: str
    destination: str

    # Ordered rule checks (short-circuit: later checks only run if earlier pass)
    checks: List[RuleCheck] = field(default_factory=list)

    # Final verdict
    cbam_applicable: bool = False
    decision_reason: str = ""          # One-line human summary

    # Supplementary info
    sector: Optional[str] = None
    description: Optional[str] = None
    legal_reference: Optional[str] = None


# =============================================================================
# PRODUCT LEVEL OUTPUT
# =============================================================================

@dataclass
class ProductAssessment:
    """
    Product-level AI assessment.
    """

    name: str
    cn_code: str
    destination: str

    covered: bool
    applicable: bool

    sector: Optional[str]
    legal_reference: Optional[str]

    reasoning: str


# =============================================================================
# CBAM
# =============================================================================

@dataclass
class CBAMAssessment:

    applicable: bool
    confidence: float
    reasoning: str

    articles: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    missing_information: List[str] = field(default_factory=list)


# =============================================================================
# CSRD
# =============================================================================

@dataclass
class CSRDAssessment:

    applicable: bool
    confidence: float
    reasoning: str

    articles: List[str] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    missing_information: List[str] = field(default_factory=list)


# =============================================================================
# FINAL OUTPUT
# =============================================================================

@dataclass
class AssessmentOutput:
    """
    Complete structured output returned by the AI Agent.
    """

    products: List[ProductAssessment] = field(default_factory=list)

    cbam: Optional[CBAMAssessment] = None

    csrd: Optional[CSRDAssessment] = None

    executive_summary: str = ""

    consultant_notes: str = ""

    risk_rating: str = ""