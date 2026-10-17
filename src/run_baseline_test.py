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

# Load .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("\n❌ Error: GEMINI_API_KEY not found!")
    print("Please create a .env file in the project root with:")
    print("GEMINI_API_KEY=your_actual_gemini_api_key\n")
    exit(1)

# Configure Gemini with REST transport
genai.configure(api_key=API_KEY, transport="rest")
model = genai.GenerativeModel("gemini-3.8-flash")

# Load baseline prompt template
prompt_path = Path("prompts/v1_baseline.txt")
prompt_template = prompt_path.read_text(encoding="utf-8")

# Extract the user prompt template section
# The template has [SYSTEM INSTRUCTIONS] and [USER INPUT TEMPLATE]
user_template = """Product Name: {product_name}
Raw Specifications:
{raw_specs_text}

Analyze this product and provide your recommendations."""

import sys

# Load test dataset
dataset_path = Path("evaluation/test_dataset.json")
with open(dataset_path, "r", encoding="utf-8") as f:
    test_cases = json.load(f)

# Allow selecting a specific test case from command line (e.g. python src/run_baseline_test.py TC-02 or all)
target_id = sys.argv[1].upper() if len(sys.argv) > 1 else "TC-02"

if target_id == "ALL":
    selected_cases = test_cases
else:
    selected_cases = [c for c in test_cases if c["id"] == target_id]
    if not selected_cases:
        print(f"❌ Test case {target_id} not found! Available: {[c['id'] for c in test_cases]}")
        exit(1)

all_results = []
results_file = Path("evaluation/baseline_results.json")

# Load existing results if present
if results_file.exists():
    try:
        with open(results_file, "r", encoding="utf-8") as f:
            existing = json.load(f)
            if isinstance(existing, list):
                all_results = existing
            elif isinstance(existing, dict):
                all_results = [existing]
    except Exception:
        all_results = []

for test_item in selected_cases:
    print("=" * 60)
    print(f"🚀 Running Baseline Test: v1.0 on {test_item['id']}")
    print(f"📦 Product: {test_item['name']}")
    print(f"🎯 Category: {test_item['category']}")
    print("=" * 60 + "\n")

    formatted_prompt = f"""You are a helpful product assistant. Given the product specifications below, simplify the technical terms, compare it for programming, gaming, and everyday work, and tell the user whether they should buy it.

Product Name: {test_item['name']}
Raw Specifications:
{test_item['input_text']}

Analyze this product and provide your recommendations."""

    # Execute with latency tracking
    start_time = time.perf_counter()
    response = model.generate_content(formatted_prompt)
    end_time = time.perf_counter()

    latency_ms = round((end_time - start_time) * 1000)

    # Extract token metrics
    prompt_tokens = getattr(response.usage_metadata, "prompt_token_count", "N/A")
    output_tokens = getattr(response.usage_metadata, "candidates_token_count", "N/A")
    total_tokens = getattr(response.usage_metadata, "total_token_count", "N/A")

    print("📋 [MODEL OUTPUT]:\n")
    print(response.text)
    print("\n" + "-" * 50)
    print("📊 [TELEMETRY & LOGS]:")
    print(f"⏱️  Latency: {latency_ms} ms")
    print(f"🔢 Prompt Tokens: {prompt_tokens}")
    print(f"🔢 Output Tokens: {output_tokens}")
    print(f"🔢 Total Tokens: {total_tokens}")
    print("-" * 50 + "\n")

    result_data = {
        "test_id": test_item["id"],
        "product_name": test_item["name"],
        "prompt_version": "v1.0_baseline",
        "model": "gemini-3.8-flash",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "latency_ms": latency_ms,
        "prompt_tokens": prompt_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "output_text": response.text
    }

    # Replace existing result for this test_id or append
    all_results = [r for r in all_results if r.get("test_id") != test_item["id"]]
    all_results.append(result_data)

    # Save to file after each test
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)

print(f"💾 All baseline results updated in: {results_file}")
