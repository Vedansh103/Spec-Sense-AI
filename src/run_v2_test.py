import os
import sys
import json
import time
from pathlib import Path
from dotenv import load_dotenv

# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import google.generativeai as genai
from schemas import SingleProductReport

# Load environment
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ Error: GEMINI_API_KEY not found in .env!")
    exit(1)

# Configure Gemini with REST transport
genai.configure(api_key=API_KEY, transport="rest")

# Configure model for JSON output
generation_config = {
    "response_mime_type": "application/json",
    "temperature": 0.2,
    "max_output_tokens": 4096
}

# Using gemini-3.7-flash for stable JSON generation and high free-tier quota
model = genai.GenerativeModel("gemini-3.7-flash", generation_config=generation_config)

# Load prompt template
prompt_path = Path("prompts/v2_schema_constrained.txt")
prompt_text = prompt_path.read_text(encoding="utf-8")

# Load test dataset
dataset_path = Path("evaluation/test_dataset.json")
with open(dataset_path, "r", encoding="utf-8") as f:
    test_cases = json.load(f)

# Default to TC-02 (the missing-specs test) or CLI argument
target_id = sys.argv[1].upper() if len(sys.argv) > 1 else "TC-02"

if target_id == "ALL":
    selected_cases = test_cases
else:
    selected_cases = [c for c in test_cases if c["id"] == target_id]
    if not selected_cases:
        print(f"❌ Test case {target_id} not found!")
        exit(1)

all_v2_results = []
results_file = Path("evaluation/v2_results.json")

if results_file.exists():
    try:
        with open(results_file, "r", encoding="utf-8") as f:
            all_v2_results = json.load(f)
    except Exception:
        all_v2_results = []

for item in selected_cases:
    print("=" * 65)
    print(f"🚀 Running Structured Test: v2.0 on {item['id']}")
    print(f"📦 Product: {item['name']}")
    print(f"🎯 Category: {item['category']}")
    print("=" * 65 + "\n")

    # Extract clean product name (remove test case parenthetical tags like '(Heavy Duty Gaming / Creator)')
    clean_name = item["name"].split("(")[0].strip() if "(" in item["name"] else item["name"]
    schema_str = json.dumps(SingleProductReport.model_json_schema(), indent=2)
    full_prompt = (
        f"{prompt_text}\n\n"
        f"[EXACT JSON SCHEMA REQUIREMENT]\n"
        f"You MUST output valid JSON strictly matching this exact JSON schema:\n"
        f"{schema_str}\n"
    ).replace("{product_name}", clean_name).replace("{raw_specs_text}", item["input_text"])

    # Execute with latency tracking
    start_time = time.perf_counter()
    response = model.generate_content(full_prompt)
    end_time = time.perf_counter()

    latency_ms = round((end_time - start_time) * 1000)

    # Extract token metrics
    prompt_tokens = getattr(response.usage_metadata, "prompt_token_count", "N/A")
    output_tokens = getattr(response.usage_metadata, "candidates_token_count", "N/A")
    total_tokens = getattr(response.usage_metadata, "total_token_count", "N/A")

    # Validate with Pydantic
    validated_report = None
    try:
        validated_report = SingleProductReport.model_validate_json(response.text)
        validation_status = "✅ 100% Pydantic Schema Valid"
    except Exception as e:
        validation_status = f"❌ Pydantic Validation Error: {e}"

    print(f"Schema Validation: {validation_status}")
    if validated_report:
        print(f"\n📋 [STRUCTURED OUTPUT PREVIEW]:")
        print(f"• Product: {validated_report.product_name}")
        print(f"• Risk Level: {validated_report.buyer_risk_level}")
        print(f"• Future-Proofing: {validated_report.future_proofing_years}")
        print(f"• Missing Specs Flagged: {len(validated_report.missing_specifications)}")
        for m in validated_report.missing_specifications:
            print(f"   ⚠️  {m}")
        print(f"• Persona Scores:")
        for p in validated_report.persona_evaluations:
            print(f"   - {p.persona}: {p.suitability_score}/10 ({p.reasoning[:80]}...)")
    else:
        print(f"Raw response: {response.text[:300]}...")

    print("\n" + "-" * 55)
    print("📊 [TELEMETRY & LOGS]:")
    print(f"⏱️  Latency: {latency_ms} ms")
    print(f"🔢 Prompt Tokens: {prompt_tokens}")
    print(f"🔢 Output Tokens: {output_tokens}")
    print(f"🔢 Total Tokens: {total_tokens}")
    print("-" * 55 + "\n")

    result_entry = {
        "test_id": item["id"],
        "product_name": item["name"],
        "prompt_version": "v2.0_schema_constrained",
        "model": "gemini-3.7-flash",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "latency_ms": latency_ms,
        "prompt_tokens": prompt_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "validation_status": validation_status,
        "raw_json_output": json.loads(response.text)
    }

    all_v2_results = [r for r in all_v2_results if r.get("test_id") != item["id"]]
    all_v2_results.append(result_entry)

    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(all_v2_results, f, indent=2)

print(f"💾 v2 results saved to: {results_file}")
