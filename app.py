"""
Streamlit application for the AI Retail Demand Forecasting Copilot.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

import requests
import streamlit as st

from config import (
    PROPHET_CATEGORY,
    PROPHET_STORE_ID,
)

FASTAPI_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AI Retail Demand Forecasting Copilot",
    page_icon="📦",
    layout="wide",
)


def run_analysis():
    response = requests.post(
        f"{FASTAPI_URL}/predict",
        json={
            "store_id": PROPHET_STORE_ID,
            "category": PROPHET_CATEGORY,
        },
        timeout=1800,
    )
    response.raise_for_status()
    return response.json()


def generate_recommendation(user_prompt):
    response = requests.post(
        f"{FASTAPI_URL}/recommend",
        json={
            "store_id": PROPHET_STORE_ID,
            "category": PROPHET_CATEGORY,
            "user_prompt": user_prompt,
        },
        timeout=300,
    )
    response.raise_for_status()
    return response.json()


if "recommendation" not in st.session_state:
    st.session_state.recommendation = None

if "analysis" not in st.session_state:
    st.session_state.analysis = None


st.title("📦 AI Retail Demand Forecasting Copilot")
st.caption("Run the analysis once, then generate multiple AI recommendations.")


col1, col2 = st.columns(2)


with col1:
    if st.button("Run Analysis", use_container_width=True):
        try:
            with st.spinner("Running forecasting pipeline..."):
                st.session_state.analysis = run_analysis()

            st.session_state.recommendation = None
            st.success("Analysis completed.")

        except requests.RequestException as exc:
            st.error(
                "Could not connect to the FastAPI backend. "
                "Make sure the API server is running."
            )
            st.caption(str(exc))


with col2:
    if st.button("Clear History", use_container_width=True):
        st.session_state.recommendation = None
        st.rerun()


if st.session_state.analysis:
    analysis = st.session_state.analysis

    st.subheader("Current Analysis")
    st.write(f"Stockout Risk: {analysis['stockout_risk']}")
    st.write(
        f"Inventory Health Score: "
        f"{analysis['inventory_health_score']:.0f}"
    )


prompt = st.text_area("Additional Instructions")


if st.button("Generate Recommendation", use_container_width=True):
    if st.session_state.analysis is None:
        st.warning("Run Analysis first.")

    else:
        try:
            with st.spinner("Generating recommendation..."):
                st.session_state.recommendation = generate_recommendation(
                    prompt.strip() or None
                )

        except requests.RequestException as exc:
            st.error("Could not generate the recommendation from FastAPI.")
            st.caption(str(exc))


st.markdown("---")


if st.session_state.recommendation is not None:
    rec = st.session_state.recommendation

    st.subheader("Executive Summary")
    st.write(rec["summary"])

    st.subheader("Recommendation")
    st.write(rec["recommendation"])

    st.subheader("Business Rationale")
    st.write(rec["rationale"])