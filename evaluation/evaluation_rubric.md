# 📊 SpecSense AI — Evaluation Rubric & Benchmark Methodology

This rubric establishes explicit, standardized criteria to evaluate prompt versions (`v1.0 Baseline`, `v2.0 Schema`, `v3.0 Guardrails`) across our test dataset.

---

## 🎯 Scoring Criteria (1 to 5 Scale per Metric)

### 1. Factuality & Grounding (Weight: 30%)
* **Score 5:** Extracts only verifiable specs from input text. Explicitly marks omitted specs as `NOT SPECIFIED` / `UNKNOWN`. Zero hallucinations.
* **Score 3:** Accurately extracts most specs, but makes minor unsupported assumptions about standard features (e.g., assuming 60Hz display).
* **Score 1:** Hallucinates critical specifications (e.g., fabricates battery capacity, refresh rate, or display brightness).

### 2. Missing-Spec Detection & Buyer Risk Awareness (Weight: 25%)
* **Score 5:** Proactively detects and lists missing specifications (e.g., unstated GPU wattage, RAM expandability, display nit brightness) and explains the buyer risk.
* **Score 3:** Mentions general risks, but fails to identify specific omitted technical parameters.
* **Score 1:** Completely ignores missing information; presents incomplete listings as fully understood.

### 3. Persona Calibration & Reasoned Scoring (Weight: 25%)
* **Score 5:** Evaluates device suitability against realistic requirements for Developers, Gamers, and Everyday Users with step-by-step technical justification.
* **Score 3:** Scores seem reasonable, but explanations are generic (e.g., "Good for gaming because it has a GPU").
* **Score 1:** Contradictory or irrational scores (e.g., recommending a dual-core laptop with integrated graphics for AAA gaming).

### 4. Output Structure & Machine Readability (Weight: 20%)
* **Score 5:** 100% compliant with Pydantic JSON schema, completely parseable, zero trailing text or markdown wrapping errors.
* **Score 3:** Semi-structured output (e.g., valid markdown tables, but not machine-readable JSON).
* **Score 1:** Completely unstructured, free-form conversational text that cannot be consumed by an API or UI.

---

## 📈 Benchmark Scoring Formula
$$\text{Overall Score} = (0.30 \times \text{Factuality}) + (0.25 \times \text{Missing Specs}) + (0.25 \times \text{Persona Calib}) + (0.20 \times \text{Structure})$$
Maximum Score: **5.0 / 5.0**
Passing Threshold: **3.5 / 5.0**
