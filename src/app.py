import os
import sys
import json
import time
from pathlib import Path

# Add project root to path for imports
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.append(str(current_dir))
sys.path.append(str(project_root))

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import importlib

import schemas
importlib.reload(schemas)
from schemas import SingleProductReport, ProductComparisonReport

import ui_components
importlib.reload(ui_components)
from ui_components import render_3d_electronics_background, get_custom_css, get_fixed_navbar_html

# Page Configuration
st.set_page_config(
    page_title="SpecSense AI — 3D Hardware Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load environment & Gemini API
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

FALLBACK_MODELS = [
    "gemini-3.5-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.7-flash"
]

if API_KEY:
    genai.configure(api_key=API_KEY, transport="rest")  # type: ignore
    is_api_configured = True
else:
    is_api_configured = False

# Resilient Generation Helper with Auto-Failover
def generate_with_fallback(full_prompt: str):
    """Executes generate_content across models with automatic failover if a model's daily quota (429) is exhausted."""
    last_exception: Exception | None = None
    for model_name in FALLBACK_MODELS:
        try:
            m = genai.GenerativeModel(  # type: ignore
                model_name,
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": 0.2,
                    "max_output_tokens": 4096
                }
            )
            start_time = time.perf_counter()
            response = m.generate_content(full_prompt)
            latency_ms = round((time.perf_counter() - start_time) * 1000)
            return response, latency_ms, model_name
        except Exception as e:
            last_exception = e
            err_msg = str(e).lower()
            if "429" in err_msg or "quota" in err_msg or "rate" in err_msg or "404" in err_msg:
                continue
            else:
                raise e
    if last_exception is not None:
        raise last_exception
    raise RuntimeError("Generation failed across all fallback models.")

# Inject Three.js 3D Background, Fixed Top-Left Navbar & Cyberpunk Styling
render_3d_electronics_background()
st.markdown(get_custom_css(), unsafe_allow_html=True)
st.markdown(get_fixed_navbar_html(), unsafe_allow_html=True)

# Load prompt templates
single_prompt_template = Path("prompts/v2_schema_constrained.txt").read_text(encoding="utf-8")
comparison_prompt_template = Path("prompts/v2_comparison.txt").read_text(encoding="utf-8")

# Load benchmark test dataset
dataset_path = Path("evaluation/test_dataset.json")
test_cases = []
if dataset_path.exists():
    with open(dataset_path, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

# Helper: Gemini Single Product Analysis Pipeline
def analyze_single_product(product_name: str, raw_specs: str, primary_use: str = "College & Studies", top_priority: str = "Maximum All-Day Battery"):
    clean_name = product_name.split("(")[0].strip() if "(" in product_name else product_name
    schema_str = json.dumps(SingleProductReport.model_json_schema(), indent=2)
    
    full_prompt = (
        f"{single_prompt_template}\n\n"
        f"[EXACT JSON SCHEMA REQUIREMENT]\n"
        f"You MUST output valid JSON strictly matching this exact JSON schema:\n"
        f"{schema_str}\n"
    ).replace("{product_name}", clean_name)\
     .replace("{primary_use}", primary_use)\
     .replace("{top_priority}", top_priority)\
     .replace("{raw_specs_text}", raw_specs)

    response, latency_ms, used_model = generate_with_fallback(full_prompt)

    prompt_tokens = getattr(response.usage_metadata, "prompt_token_count", "N/A")
    output_tokens = getattr(response.usage_metadata, "candidates_token_count", "N/A")

    report = SingleProductReport.model_validate_json(response.text)
    return report, latency_ms, prompt_tokens, output_tokens, response.text

# Helper: Gemini Product Comparison Pipeline
def compare_products(prod_a_name: str, prod_a_specs: str, prod_b_name: str, prod_b_specs: str):
    schema_str = json.dumps(ProductComparisonReport.model_json_schema(), indent=2)
    
    full_prompt = (
        f"{comparison_prompt_template}\n\n"
        f"[EXACT JSON SCHEMA REQUIREMENT]\n"
        f"You MUST output valid JSON strictly matching this exact JSON schema:\n"
        f"{schema_str}\n"
    ).replace("{product_a_name}", prod_a_name)\
     .replace("{product_a_specs}", prod_a_specs)\
     .replace("{product_b_name}", prod_b_name)\
     .replace("{product_b_specs}", prod_b_specs)

    response, latency_ms, used_model = generate_with_fallback(full_prompt)

    prompt_tokens = getattr(response.usage_metadata, "prompt_token_count", "N/A")
    output_tokens = getattr(response.usage_metadata, "candidates_token_count", "N/A")

    report = ProductComparisonReport.model_validate_json(response.text)
    return report, latency_ms, prompt_tokens, output_tokens, response.text


# ==========================================
# HEADER & HERO SECTION
# ==========================================
st.markdown("""
<div class="page-hero-banner">
    <div class="page-hero-title">Precision Hardware Specification Intelligence</div>
    <div class="page-hero-desc">
        Unmask hidden manufacturer omissions, decode dense marketing hype with everyday analogies, 
        and compute objective suitability scores tailored to your workflow.
    </div>
</div>
""", unsafe_allow_html=True)

if not API_KEY:
    st.error("⚠️ GEMINI_API_KEY is not set in `.env`! Please add your key to run live analyses.")

# Navigation Tabs
tab_single, tab_compare = st.tabs([
    "🔍 Single-Product Scanner",
    "⚔️ Head-to-Head Comparator"
])


# ==========================================
# TAB 1: SINGLE PRODUCT SCANNER
# ==========================================
with tab_single:
    with st.container(border=True):
        st.markdown("### 📥 Input Hardware Specifications")
        st.write("Type or paste any raw product specification sheet, or load one of the calibrated benchmark presets below:")

        # Preset Quick Loaders
        preset_cols = st.columns(6)
        selected_preset = None

        with preset_cols[0]:
            if st.button("🍏 MacBook Air M3", use_container_width=True):
                selected_preset = next((c for c in test_cases if c["id"] == "TC-01"), None)
        with preset_cols[1]:
            if st.button("⚠️ Budget Core i5", use_container_width=True):
                selected_preset = next((c for c in test_cases if c["id"] == "TC-02"), None)
        with preset_cols[2]:
            if st.button("🚀 Gaming Fluff", use_container_width=True):
                selected_preset = next((c for c in test_cases if c["id"] == "TC-03"), None)
        with preset_cols[3]:
            if st.button("🎮 Legion Pro 5", use_container_width=True):
                selected_preset = next((c for c in test_cases if c["id"] == "TC-04"), None)
        with preset_cols[4]:
            if st.button("📱 S24 Ultra", use_container_width=True):
                selected_preset = next((c for c in test_cases if c["id"] == "TC-06"), None)
        with preset_cols[5]:
            if st.button("👕 Cotton T-Shirt", use_container_width=True):
                selected_preset = next((c for c in test_cases if c["id"] == "TC-07"), None)

        # Manage session state for inputs
        if "input_prod_name" not in st.session_state:
            st.session_state.input_prod_name = "Budget Core i5 Laptop"
        if "input_raw_specs" not in st.session_state:
            st.session_state.input_raw_specs = "Ultra-Slim 15.6 Laptop. Intel Core i5-1235U (10 cores). 8GB DDR4 RAM, 256GB SSD. 15.6-inch FHD anti-glare display. Intel Iris Xe Graphics. Windows 11."

        if selected_preset:
            st.session_state.input_prod_name = selected_preset["name"].split("(")[0].strip()
            st.session_state.input_raw_specs = selected_preset["input_text"]

        # 3-Second Personal Needs Wizard
        col_name, col_use, col_priority = st.columns([1.6, 1.2, 1.2])
        with col_name:
            prod_name_input = st.text_input("Product Name", value=st.session_state.input_prod_name, key="prod_name_field")
        with col_use:
            primary_use_input = st.selectbox(
                "🎯 Your Primary Use",
                [
                    "College & Studies",
                    "Office Work & Multitasking",
                    "Casual / Competitive Gaming",
                    "Heavy Coding & Tech",
                    "Video Editing & Content Creation"
                ],
                index=0
            )
        with col_priority:
            priority_input = st.selectbox(
                "⚡ Your Top Priority",
                [
                    "Maximum All-Day Battery",
                    "Extreme Speed & Performance",
                    "Lightweight Portability",
                    "Best Budget Value for Money"
                ],
                index=0
            )

        raw_specs_input = st.text_area(
            "Raw Manufacturer / Seller Specifications",
            value=st.session_state.input_raw_specs,
            height=130,
            key="raw_specs_field",
            help="Paste the full promotional description or specs table here."
        )

        analyze_btn = st.button("⚡ EXECUTE DEEP HARDWARE SCAN", use_container_width=True)

    if analyze_btn:
        if not prod_name_input or not raw_specs_input:
            st.warning("Please provide both a product name and specification text.")
        elif not is_api_configured:
            st.error("Gemini API key is required in .env.")
        else:
            with st.spinner("Decoding technical jargon & analyzing hardware risk..."):
                try:
                    report, latency, prompt_toks, out_toks, raw_json = analyze_single_product(
                        prod_name_input, raw_specs_input, primary_use_input, priority_input
                    )

                    # 1. Personal Match Gauge (Interactive Needs Wizard Result)
                    pm = getattr(report, "personal_match", None)
                    if pm:
                        match_pct = max(0, min(100, pm.match_percentage))
                        pct_color = "#10b981" if match_pct >= 80 else ("#f59e0b" if match_pct >= 60 else "#ef4444")
                        dial_glow = "rgba(16, 185, 129, 0.45)" if match_pct >= 80 else ("rgba(245, 158, 11, 0.45)" if match_pct >= 60 else "rgba(239, 68, 68, 0.45)")

                        fit_pills_html = "".join([f'<span class="match-pill-fit">✓ {item}</span>' for item in pm.why_it_fits])
                        tradeoff_pills_html = "".join([f'<span class="match-pill-tradeoff">⚠️ {item}</span>' for item in pm.compromises_to_know])

                        st.markdown(f"""
                        <div class="match-banner">
                            <div class="match-left">
                                <div class="match-dial-box" style="border-color: {pct_color}; box-shadow: 0 0 20px {dial_glow};">
                                    <div style="text-align: center;">
                                        <div class="match-pct-text" style="color: {pct_color};">{match_pct}%</div>
                                        <div class="match-pct-symbol">MATCH</div>
                                    </div>
                                </div>
                                <div class="match-details">
                                    <div class="match-category-tag">
                                        <span>🎯 PERSONAL MATCH GAUGE</span> • <span>FOR {primary_use_input.upper()}</span> • <span>PRIORITY: {priority_input.upper()}</span>
                                    </div>
                                    <div class="match-headline">{pm.verdict_headline}</div>
                                    <div class="match-subtext">Objective suitability calculated specifically for your daily workflow and top hardware priority.</div>
                                    <div class="match-pills-row">
                                        {fit_pills_html}
                                        {tradeoff_pills_html}
                                    </div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    # 2. Buyer Risk Index Banner
                    risk_class = "risk-low"
                    risk_icon = "🛡️"
                    if report.buyer_risk_level == "HIGH RISK":
                        risk_class = "risk-high"
                        risk_icon = "🚨"
                    elif report.buyer_risk_level == "MODERATE RISK":
                        risk_class = "risk-moderate"
                        risk_icon = "⚠️"
                    elif report.buyer_risk_level == "OUT OF SCOPE":
                        risk_class = "risk-out-of-scope"
                        risk_icon = "⛔"

                    st.markdown(f"""
                    <div class="risk-banner {risk_class}">
                        <div class="risk-badge-group">
                            <span class="risk-icon">{risk_icon}</span>
                            <div>
                                <div class="risk-micro-label">BUYER RISK INDEX</div>
                                <div class="risk-level-title">{report.buyer_risk_level}</div>
                            </div>
                        </div>
                        <div class="risk-lifespan-card">
                            <div class="risk-micro-label">ESTIMATED HARDWARE LIFESPAN</div>
                            <div class="risk-lifespan-value">⏳ {report.future_proofing_years}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # 2. Executive Summary Card
                    st.markdown(f"""
                    <div class="glass-card">
                        <h4 style="margin-top: 0; color: #00f2fe; font-family: 'Space Grotesk', sans-serif;">📋 Executive Verdict</h4>
                        <p style="font-size: 1.05rem; line-height: 1.6; color: #e2e8f0; margin: 0;">{report.executive_summary}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # 3. Missing Specifications Alert (If Any)
                    if report.missing_specifications:
                        tags_html = "".join([f'<span class="missing-tag">⚠️ {m}</span>' for m in report.missing_specifications])
                        st.markdown(f"""
                        <div class="glass-card" style="border-left: 5px solid #ef4444;">
                            <h4 style="margin-top: 0; color: #f87171; font-family: 'Space Grotesk', sans-serif;">⚠️ Critical Unstated Specifications (Buyer Traps)</h4>
                            <p style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 10px;">The seller omitted the following specs that directly affect daily usage or out-of-pocket costs:</p>
                            <div>{tags_html}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    # 4. Buyer Warnings (If Any)
                    if report.buyer_warnings:
                        warnings_html = "".join([f'<li style="margin-bottom: 6px; color: #f8fafc;"><strong>{w}</strong></li>' for w in report.buyer_warnings])
                        st.markdown(f"""
                        <div class="glass-card" style="border-left: 5px solid #f59e0b;">
                            <h4 style="margin-top: 0; color: #fbbf24; font-family: 'Space Grotesk', sans-serif; margin-bottom: 10px;">🔔 Important Fine-Print Traps & Observations</h4>
                            <ul style="line-height: 1.6; margin: 0; padding-left: 20px;">
                                {warnings_html}
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)

                    # 5. Persona Suitability Analysis
                    if report.persona_evaluations:
                        st.markdown("### 🎯 Persona Suitability Ratings")
                        p_cols = st.columns(len(report.persona_evaluations))
                        for i, p in enumerate(report.persona_evaluations):
                            score_color = "#10b981" if p.suitability_score >= 7 else ("#f59e0b" if p.suitability_score >= 4 else "#ef4444")
                            with p_cols[i]:
                                st.markdown(f"""
                                <div class="persona-card">
                                    <div>
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                            <span style="font-weight: 700; font-size: 1.1rem; color: #f8fafc;">{p.persona}</span>
                                            <span class="score-circle" style="color: {score_color};">{p.suitability_score}<span style="font-size: 1rem; opacity: 0.6;">/10</span></span>
                                        </div>
                                        <p style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.5; margin-bottom: 12px;">{p.reasoning}</p>
                                    </div>
                                    <div>
                                        <div style="font-size: 0.78rem; text-transform: uppercase; color: #34d399; font-weight: 700; margin-bottom: 4px;">KEY ADVANTAGES</div>
                                        {"".join([f'<div class="pill-advantage">✓ {a}</div>' for a in p.key_advantages])}
                                        <div style="font-size: 0.78rem; text-transform: uppercase; color: #f87171; font-weight: 700; margin-top: 8px; margin-bottom: 4px;">KEY BOTTLENECK</div>
                                        {"".join([f'<div class="pill-bottleneck">✗ {b}</div>' for b in p.key_bottlenecks])}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)

                        st.markdown("<br>", unsafe_allow_html=True)

                    # 6. Jargon Busters & Simplified Analogies
                    if report.extracted_specs:
                        st.markdown("### 💡 Jargon Busters & Everyday Analogies")
                        analogies_html = "".join([f"""
                        <div class="analogy-card">
                            <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 8px; margin-bottom: 6px;">
                                <span style="font-weight: 700; color: #f8fafc; font-size: 1.02rem;">{item.feature}</span>
                                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #00f2fe; background: rgba(0, 242, 254, 0.08); padding: 2px 8px; border-radius: 6px; border: 1px solid rgba(0, 242, 254, 0.2); word-break: break-word;">{item.raw_value}</span>
                            </div>
                            <div style="font-size: 0.92rem; color: #cbd5e1; line-height: 1.5; margin: 4px 0 8px 0;">{item.simplified_explanation}</div>
                            <div class="analogy-label">Relatable Analogy:</div>
                            <div class="analogy-text">"{item.everyday_analogy}"</div>
                        </div>
                        """ for item in report.extracted_specs])
                        st.markdown(f"""
                        <div class="glass-card">
                            {analogies_html}
                        </div>
                        """, unsafe_allow_html=True)

                    # 7. Final Buying Verdict
                    st.markdown("### ⚖️ Final Buying Verdict")
                    col_buy, col_avoid = st.columns(2)
                    with col_buy:
                        buy_items_html = "".join([f'<li style="margin-bottom: 6px;">{b}</li>' for b in report.buy_if])
                        st.markdown(f"""
                        <div class="glass-card" style="border-top: 4px solid #10b981;">
                            <h4 style="color: #34d399; margin-top: 0;">🟢 Buy If:</h4>
                            <ul style="color: #cbd5e1; line-height: 1.6; margin: 0; padding-left: 20px;">
                                {buy_items_html}
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)

                    with col_avoid:
                        avoid_items_html = "".join([f'<li style="margin-bottom: 6px;">{a}</li>' for a in report.avoid_if])
                        st.markdown(f"""
                        <div class="glass-card" style="border-top: 4px solid #ef4444;">
                            <h4 style="color: #f87171; margin-top: 0;">🔴 Avoid If:</h4>
                            <ul style="color: #cbd5e1; line-height: 1.6; margin: 0; padding-left: 20px;">
                                {avoid_items_html}
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)


                except Exception as e:
                    err_msg = str(e)
                    if "429" in err_msg or "quota" in err_msg:
                        st.error("⏳ **Gemini Free-Tier Rate Limit Reached.** All daily free request quotas have been exhausted. Please retry in a little while or configure a fresh API key in `.env`.")
                    else:
                        st.error(f"Execution Error: {e}")


# ==========================================
# TAB 2: HEAD-TO-HEAD COMPARATOR
# ==========================================
with tab_compare:
    with st.container(border=True):
        st.markdown("### ⚔️ Side-by-Side Product Comparator")
        st.write("Compare two electronic devices directly across real-world performance, display, battery, and value:")

        # Helper for safe preset lookup
        def get_tc_text(tc_id: str, fallback: str) -> str:
            return next((c["input_text"] for c in test_cases if c.get("id") == tc_id), fallback)

        # Quick comparison presets
        comp_preset_cols = st.columns(3)
        if comp_preset_cols[0].button("MacBook Air M3 vs Legion Pro 5", use_container_width=True):
            st.session_state.comp_a_name = "Apple MacBook Air 13 M3"
            st.session_state.comp_a_specs = get_tc_text("TC-01", "Apple M3 8-core CPU, 10-core GPU, 16GB RAM, 512GB SSD, 13.6 Liquid Retina 500 nits, 18-hour battery, 1.24kg.")
            st.session_state.comp_b_name = "Lenovo Legion Pro 5"
            st.session_state.comp_b_specs = get_tc_text("TC-04", "AMD Ryzen 7 7745HX, RTX 4070 8GB 140W, 32GB DDR5 RAM, 1TB SSD, 16-inch 240Hz 500 nits, 80Wh battery, 2.55kg.")

        if comp_preset_cols[1].button("Galaxy S24 Ultra vs iPad Air M2", use_container_width=True):
            st.session_state.comp_a_name = "Samsung Galaxy S24 Ultra"
            st.session_state.comp_a_specs = get_tc_text("TC-06", "Snapdragon 8 Gen 3 for Galaxy, 12GB RAM, 256GB storage, 6.8 Dynamic AMOLED 2X 2600 nits 120Hz, 5000mAh battery, S-Pen, Titanium frame.")
            st.session_state.comp_b_name = "Apple iPad Air 11-inch M2"
            st.session_state.comp_b_specs = get_tc_text("TC-05", "Apple M2 chip 8-core CPU, 10-core GPU, 8GB RAM, 128GB storage, 11-inch Liquid Retina 500 nits 60Hz, iPadOS, 28.6Wh battery, 462g.")

        if comp_preset_cols[2].button("Budget Core i5 vs Legion Pro 5", use_container_width=True):
            st.session_state.comp_a_name = "Budget Core i5 Laptop"
            st.session_state.comp_a_specs = get_tc_text("TC-02", "Ultra-Slim 15.6 Laptop. Intel Core i5-1235U (10 cores). 8GB DDR4 RAM, 256GB SSD. 15.6-inch FHD anti-glare display. Intel Iris Xe Graphics. Windows 11.")
            st.session_state.comp_b_name = "Lenovo Legion Pro 5"
            st.session_state.comp_b_specs = get_tc_text("TC-04", "AMD Ryzen 7 7745HX, RTX 4070 8GB 140W, 32GB DDR5 RAM, 1TB SSD, 16-inch 240Hz 500 nits, 80Wh battery, 2.55kg.")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("#### 📦 Product A")
            prod_a_name = st.text_input("Product A Name", value=st.session_state.get("comp_a_name", "Apple MacBook Air 13 M3"))
            prod_a_specs = st.text_area("Product A Raw Specifications", value=st.session_state.get("comp_a_specs", "Apple M3 8-core CPU, 10-core GPU, 16GB RAM, 512GB SSD, 13.6 Liquid Retina 500 nits, 18-hour battery, 1.24kg."), height=160)

        with col_b:
            st.markdown("#### 📦 Product B")
            prod_b_name = st.text_input("Product B Name", value=st.session_state.get("comp_b_name", "Lenovo Legion Pro 5"))
            prod_b_specs = st.text_area("Product B Raw Specifications", value=st.session_state.get("comp_b_specs", "AMD Ryzen 7 7745HX, RTX 4070 8GB 140W, 32GB DDR5 RAM, 1TB SSD, 16-inch 240Hz 500 nits, 80Wh battery, 2.55kg."), height=160)

        compare_btn = st.button("⚔️ GENERATE OBJECTIVE COMPARISON", use_container_width=True)

    if compare_btn:
        if not prod_a_name or not prod_a_specs or not prod_b_name or not prod_b_specs:
            st.warning("Please provide product names and specification text for both Product A and Product B.")
        elif not is_api_configured:
            st.error("Gemini API key is required in .env.")
        else:
            with st.spinner("Analyzing trade-offs and synthesizing persona verdicts..."):
                try:
                    comp_report, c_latency, c_prompt_toks, c_out_toks, c_raw_json = compare_products(prod_a_name, prod_a_specs, prod_b_name, prod_b_specs)

                    st.markdown(f"""
                    <div class="glass-card" style="border-top: 4px solid #8338ec;">
                        <h3 style="color: #a78bfa; margin-top: 0; font-family: 'Space Grotesk', sans-serif;">🏆 Overall Comparison Verdict</h3>
                        <p style="font-size: 1.1rem; line-height: 1.6; color: #f8fafc;">{comp_report.overall_verdict}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    if comp_report.tradeoffs:
                        st.markdown("### 📊 Category Trade-Off Breakdown")
                        for t in comp_report.tradeoffs:
                            winner_badge = f'<span style="background: rgba(0, 242, 254, 0.2); border: 1px solid #00f2fe; padding: 3px 8px; border-radius: 6px; font-weight: 700; color: #00f2fe;">WINNER: {t.winner}</span>'
                            st.markdown(f"""
                            <div class="glass-card" style="padding: 16px; margin-bottom: 12px;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                    <span style="font-weight: 700; font-size: 1.1rem; color: #f1f5f9;">{t.feature_area}</span>
                                    {winner_badge}
                                </div>
                                <p style="font-size: 0.95rem; color: #cbd5e1; margin: 0;">{t.analysis}</p>
                            </div>
                            """, unsafe_allow_html=True)

                    if comp_report.persona_recommendations:
                        st.markdown("### 🎯 Recommendations by Persona")
                        rec_cols = st.columns(len(comp_report.persona_recommendations))
                        for idx, (persona_name, recommended_choice) in enumerate(comp_report.persona_recommendations.items()):
                            with rec_cols[idx]:
                                st.markdown(f"""
                                <div class="persona-card" style="text-align: center; justify-content: center;">
                                    <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase;">FOR {persona_name}</div>
                                    <div style="font-size: 1.25rem; font-weight: 800; color: #00f2fe; margin-top: 8px;">{recommended_choice}</div>
                                </div>
                                """, unsafe_allow_html=True)

                except Exception as e:
                    err_msg = str(e)
                    if "429" in err_msg or "quota" in err_msg:
                        st.error("⏳ **Gemini Free-Tier Rate Limit Reached.** All daily free request quotas have been exhausted. Please retry in a little while or configure a fresh API key in `.env`.")
                    else:
                        st.error(f"Comparison Error: {e}")



