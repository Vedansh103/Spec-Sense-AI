# 📜 Prompt Version History & Changelog

This document tracks all prompt iterations, design decisions, and reasons for refinement in SpecSense AI.

---

## 📌 Version 1.0 — Baseline Prompt
* **File:** `prompts/v1_baseline.txt`
* **Architecture:** Single-turn, zero-shot unconstrained prompt.
* **Goal:** Establish a baseline output for raw LLM performance when given unstructured technical specifications.
* **Expected Failure Modes to Test:**
  1. Output format inconsistency (free-form markdown vs. structured data).
  2. Potential hallucinations of unstated hardware specifications (e.g., assuming battery life or display refresh rates when missing).
  3. Generic recommendations rather than persona-calibrated trade-offs.
  4. Susceptibility to marketing buzzwords in raw input text.

---

## 📌 Version 2.0 — Schema-Constrained & Guardrails
* **File:** `prompts/v2_schema_constrained.txt`
* **Architecture:** Structured Output prompt with Pydantic schema validation (`src/schemas.py`).
* **Key Additions & Rationale:**
  1. **Rule 0: Domain Scope Guardrail (Adversarial Defense):** Explicitly rejects non-electronic products (apparel, food, lifestyle goods), immediately returning `buyer_risk_level = "OUT OF SCOPE"` and 0/10 scores across personas rather than hallucinating computing analogies for fabric or shoes.
  2. **Rule 1: Strict Negative Constraints & Universal Consumer Filter:** Enforces `raw_value = "NOT SPECIFIED"` and `is_missing_or_vague = true` only for omissions that directly impact daily usability, upgradeability, or extra costs. Strictly excludes internal engineering trivia (capacitor types, cooling dimensions) and obsolete legacy features across all hardware categories.
  3. **Rule 2: Everyday Analogies:** Required `everyday_analogy` for each hardware component to simplify technical specs for non-technical users.
  4. **Rule 3 & 4: Buyer Risk Index & Future-Proofing Lifespan:** Added `buyer_risk_level` ("LOW RISK", "MODERATE RISK", "HIGH RISK") and `future_proofing_years` to give consumers actionable longevity expectations.
  5. **Rule 5: Persona Calibration:** Dynamic 1-10 scoring with concrete hardware justifications for Software Developers, Competitive Gamers, and Everyday Students.
  6. **XML Input Delineation & Dynamic Schema Injection:** Structured input variables using `<product_name>` and `<raw_specifications>` tags with explicit schema specification to prevent token bleeding and guarantee 100% parseable JSON output.

---

## 📌 Planned Version 3.0 — Multi-Stage Chain with Negative Constraints
* **Goal:** 3-stage prompt pipeline (Parser $\rightarrow$ Persona Scorer $\rightarrow$ Verdict Synthesizer) for complex multi-product comparisons.
* **Goal:** 3-stage prompt pipeline (Parser $\rightarrow$ Persona Scorer $\rightarrow$ Verdict Synthesizer) with negative constraints against spec guessing.
