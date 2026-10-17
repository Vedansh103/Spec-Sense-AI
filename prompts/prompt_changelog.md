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

## 📌 Planned Version 2.0 — Schema-Constrained & Pydantic Guided
* **Goal:** Enforce rigid JSON output adhering to `src/schemas.py`, introduce explicit extraction schemas, and separate specification parsing from recommendation synthesis.

---

## 📌 Planned Version 3.0 — Multi-Stage Chain with Missing-Spec Guardrails
* **Goal:** 3-stage prompt pipeline (Parser $\rightarrow$ Persona Scorer $\rightarrow$ Verdict Synthesizer) with negative constraints against spec guessing.
