from typing import List, Optional
from pydantic import BaseModel, Field


class SpecificationItem(BaseModel):
    feature: str = Field(description="Name of the component or specification (e.g., Processor, RAM, GPU, Display)")
    raw_value: str = Field(description="The exact specification value stated in the input text")
    simplified_explanation: str = Field(description="Plain-English explanation of what this means for regular users")
    is_missing_or_vague: bool = Field(default=False, description="True if the spec was omitted, incomplete, or ambiguous")


class PersonaEvaluation(BaseModel):
    persona: str = Field(description="Target persona: 'Software Developer', 'Competitive Gamer', or 'Everyday / Student'")
    suitability_score: int = Field(ge=1, le=10, description="Suitability rating from 1 to 10")
    key_advantages: List[str] = Field(description="Specific hardware features that benefit this persona")
    key_bottlenecks: List[str] = Field(description="Hardware limitations or trade-offs for this persona")
    reasoning: str = Field(description="Step-by-step justification for the score")


class SingleProductReport(BaseModel):
    product_name: str = Field(description="Identified or provided product name")
    executive_summary: str = Field(description="2-3 sentence plain-English summary of the product's identity and value proposition")
    extracted_specs: List[SpecificationItem] = Field(description="List of extracted and simplified specifications")
    missing_specifications: List[str] = Field(description="Critical hardware details omitted by the seller/manufacturer")
    buyer_warnings: List[str] = Field(description="Potential risks, hidden traps (e.g., soldered RAM, low wattage GPU, poor color accuracy)")
    persona_evaluations: List[PersonaEvaluation] = Field(description="Suitability analysis across all supported personas")
    buy_if: List[str] = Field(description="Conditions under which this device is a great purchase")
    avoid_if: List[str] = Field(description="Conditions under which a buyer should skip or look for alternatives")


class ComparisonTradeoff(BaseModel):
    feature_area: str = Field(description="Area of comparison (e.g., CPU Performance, Display Quality, Portability)")
    winner: str = Field(description="Product name that wins this area, or 'Tie'")
    analysis: str = Field(description="Plain-language explanation of the real-world performance difference")


class ProductComparisonReport(BaseModel):
    products_compared: List[str] = Field(description="Names of the products being compared")
    tradeoffs: List[ComparisonTradeoff] = Field(description="Direct category-by-category trade-off breakdown")
    persona_recommendations: dict[str, str] = Field(description="Best product choice per persona (e.g., {'Coding': 'MacBook', 'Gaming': 'Asus'})")
    overall_verdict: str = Field(description="Definitive buying recommendation taking value and compromises into account")
