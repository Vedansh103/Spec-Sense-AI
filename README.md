# 🔍 SpecSense AI — Product Specification Explainer & Comparator

SpecSense AI is an application that helps users understand and compare technical product specifications. It translates complex technical details into plain language and highlights how well a product fits specific use cases such as programming, gaming, or everyday work.

---

### 🚀 Key Capabilities
- **Specification Simplification:** Explains complex hardware terms (TDP, PCIe generations, color gamuts, RAM architectures) in simple terms.
- **Missing Specification Detection:** Flags critical hardware details omitted by manufacturers or sellers (e.g., undisclosed screen brightness, unstated RAM expandability).
- **Use-Case Suitability Analysis:** Evaluates devices against tailored criteria for Developers, Gamers, and General Users.
- **Product Comparison:** Side-by-side trade-off analysis highlighting pros, cons, and compromises.
- **Clear Buying Verdicts:** Actionable "Buy if..." vs. "Avoid if..." recommendations.

---

### 🛠️ Tech Stack
- **Language & Framework:** Python 3.10+, Streamlit
- **LLM Engine:** Google Gemini API
- **Schema Validation:** Pydantic
- **Version Control:** Git & GitHub

---

### 📁 Repository Structure
```text
├── docs/                # Milestone documentation, proposals & architecture
├── prompts/             # Prompt version history (v1 baseline, v2 schema, v3 guardrails)
├── evaluation/          # Benchmark test cases, evaluation rubrics, error logs
├── src/                 # Application source code & Pydantic models
│   ├── schemas.py       # Pydantic schemas for structured LLM outputs
│   └── app.py           # Streamlit application UI & pipeline
├── requirements.txt     # Project dependencies
└── README.md
```
