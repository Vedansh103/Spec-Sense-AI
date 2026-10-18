from typing import List, Optional
from pydantic import BaseModel, Field


class SpecificationItem(BaseModel):
    feature: str = Field(description="Name of the component or specification (e.g., Processor, RAM, GPU, Display, Battery)")
    raw_value: str = Field(description="The exact specification value stated in the input text, or 'NOT SPECIFIED'")
    simplified_explanation: str = Field(description="Plain-English explanation of what this means for regular users")
    everyday_analogy: str = Field(description="Relatable everyday analogy (e.g. RAM as desk space, SSD as filing cabinet)")
    is_missing_or_vague: bool = Field(description="True if the spec was omitted, incomplete, or ambiguous")


class PersonaEvaluation(BaseModel):
    persona: str = Field(description="Target persona: 'Software Developer', 'Competitive Gamer', or 'Everyday / Student'")
    suitability_score: int = Field(description="Suitability rating from 1 to 10")
    key_advantages: List[str] = Field(description="Specific hardware features that benefit this persona")
    key_bottlenecks: List[str] = Field(description="Hardware limitations or trade-offs for this persona")
    reasoning: str = Field(description="Step-by-step justification for the score")


class PersonalMatchEvaluation(BaseModel):
    match_percentage: int = Field(description="A calculated match score from 0 to 100 indicating how well this hardware fulfills the user's specific primary use and top priority.")
    verdict_headline: str = Field(description="Concise, punchy verdict for this user (e.g. 'Outstanding Campus Multitasker', 'Underpowered for Serious Gaming')")
    why_it_fits: List[str] = Field(description="2-3 specific points explaining how the hardware satisfies their primary use and priority")
    compromises_to_know: List[str] = Field(description="1-2 specific trade-offs or limitations this particular user should know about")


class SingleProductReport(BaseModel):
    product_name: str = Field(description="Short, concise product name (brand and model only, max 10 words, e.g. 'Apple MacBook Air 13 M3')")
    executive_summary: str = Field(description="2-3 sentence plain-English summary of the product's identity and value proposition")
    extracted_specs: List[SpecificationItem] = Field(description="List of extracted and simplified specifications with analogies")
    missing_specifications: List[str] = Field(description="Critical hardware details omitted by the seller/manufacturer")
    buyer_risk_level: str = Field(description="'LOW RISK', 'MODERATE RISK', or 'HIGH RISK' based on omitted specs and hidden limitations")
    buyer_warnings: List[str] = Field(description="Specific warnings and hidden traps (e.g., unstated screen nits, non-upgradeable RAM)")
    future_proofing_years: str = Field(description="Estimated useful lifespan before the hardware feels slow (e.g., '1-2 years', '3-4 years', '4-5+ years') with justification")
    personal_match: Optional[PersonalMatchEvaluation] = Field(default=None, description="Tailored evaluation based on the user's selected primary use and top priority")
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
