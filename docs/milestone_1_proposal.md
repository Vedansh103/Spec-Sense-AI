# 📄 Milestone 1 Proposal — SpecSense AI

**Course:** Prompt Engineering — Applied AI Mini-Project (B.Tech 5th Sem, Bennett University)  
**Total Assessment Marks for M1:** 8 Marks  
**Project Selection Route:** Self-Defined Project (Faculty Approval Track)  

---

### 1. Project Title & Prompt-Engineering Use Case (1.0 Mark)
* **Title:** SpecSense AI — Product Specification Explainer & Comparator
* **Use Case:** An applied prompt-engineering system that extracts raw, dense technical product specifications, translates them into plain-English real-world meaning, detects omitted/misleading hardware specs, and generates persona-calibrated buying recommendations.

### 2. Problem & User Context (1.0 Mark)
* **Problem:** Average consumers and students face significant information asymmetry when purchasing computers and electronics. Sellers often use technical jargon (*TDP, PCIe Gen4, IPS vs TN, sRGB*) or intentionally omit crucial specs (*GPU wattage, display nit brightness, RAM upgradeability*). Unassisted LLMs either hallucinate missing specs or generate generic advice without understanding trade-offs.
* **Context:** E-commerce listings, spec sheets, manufacturer promotional descriptions.
* **Desired Outcome:** Accurate, structured, plain-language breakdown with explicit buyer warnings for omitted specs and persona suitability scores.

### 3. Reason for Selection & Prompt Engineering Relevance (0.5 Mark)
* This problem is uniquely suited for prompt engineering rather than traditional machine learning because:
  1. No model training is needed; commercial LLMs already possess broad hardware knowledge.
  2. The primary challenge is **information extraction, hallucination prevention on missing data, and persona calibration**, which are core prompt engineering problems solved via task decomposition, negative constraints, and structured schemas.

### 4. Target Users & Stakeholders (0.5 Mark)
* **Primary Users:** Everyday consumers, college students, and non-technical professionals seeking clarity before buying hardware.
* **Secondary Users:** Tech enthusiasts and junior developers comparing multiple laptops across specific workloads (e.g., Docker, ML compilation vs. casual web browsing).

### 5. Prompt Engineering Task Definition (1.0 Mark)
* **Inputs:** Raw product spec text, copy-pasted marketing descriptions, or comparison product pairs + chosen user persona.
* **Outputs:** 
  1. Standardized Pydantic JSON specification schema.
  2. Missing-specifications risk checklist.
  3. Persona suitability score (1–10) with step-by-step reasoning.
  4. Final synthesized buying verdict ("Buy if...", "Avoid if...").

### 6. Technology / Model / Tool Approach (0.5 Mark)
* **LLM:** Google Gemini API (gemini-1.5-flash / gemini-1.5-pro) for high-context comprehension and reasoning.
* **Schema Enforcement:** Pydantic models for validated, guaranteed JSON outputs.
* **Application Framework:** Streamlit for an interactive user interface.
* **Workflow Engine:** Python-based multi-stage prompt chaining.

### 7. Existing Solutions & Identified Gap (1.0 Mark)
* **Existing Solutions:** General e-commerce filters (Amazon/Flipkart), YouTube tech reviews, and generic ChatGPT prompts.
* **The Gap:** 
  * E-commerce filters don't explain what specs mean in practice and often lack filters for critical nuances (like TGP or color gamut).
  * Generic LLM queries frequently hallucinate missing details or produce overly generic responses without structured risk checks. SpecSense AI fills this gap with explicit missing-spec detection and persona rubrics.

### 8. Research & Evidence Sources (1.0 Mark)
* IEEE / arXiv papers on structured prompt engineering, Chain-of-Thought (CoT), and schema-constrained LLM generation.
* Standardized hardware benchmarks and spec documentation (JEDEC, VESA DisplayHDR, manufacturer whitepapers).

### 9. Initial Baseline Prompt & Concept (0.5 Mark)
* Baseline zero-shot prompt defined in `prompts/v1_baseline.txt`.
* Initial benchmark test cases created in `evaluation/test_dataset.json`.

### 10. Industry / Faculty / Senior Feedback (1.0 Mark)
* *(To be updated upon faculty review and feedback discussion)*.
