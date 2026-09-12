"""
Streamlit application for the AI Retail Demand Forecasting Copilot.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

import streamlit as st

from config import (
    CATEGORY_SALES_DATA,
    CURRENT_INVENTORY,
    ITEMS_DATA,
    LEAD_TIME_DAYS,
    PROPHET_CATEGORY,
    PROPHET_STORE_ID,
    SAFETY_STOCK,
    SELLING_PRICE,
    TRAIN_DATA,
    XGBOOST_CATEGORY,
    XGBOOST_STORE_ID,
)
from data.dataset_builder import DatasetBuilder
from forecasting.prophet.pipeline import ProphetPipeline
from forecasting.xgboost.pipeline import XGBoostPipeline
from inventory import InventoryAnalysis, InventoryPosition, InventoryRisk
from metrics import BusinessAnalysis, BusinessMetrics
from recommendation import RecommendationEngine

st.set_page_config(page_title="AI Retail Demand Forecasting Copilot", page_icon="📦", layout="wide")

@st.cache_data(show_spinner=False)
def build_dataset():
    DatasetBuilder().build_category_dataset(
        train_path=str(TRAIN_DATA),
        items_path=str(ITEMS_DATA),
        output_path=str(CATEGORY_SALES_DATA),
    )

@st.cache_resource(show_spinner=False)
def run_analysis():
    build_dataset()

    ProphetPipeline(CATEGORY_SALES_DATA).run(
        store_id=PROPHET_STORE_ID,
        category=PROPHET_CATEGORY,
    )

    predictions, _, _ = XGBoostPipeline(CATEGORY_SALES_DATA).run(
        store_id=XGBOOST_STORE_ID,
        category=XGBOOST_CATEGORY,
    )

    forecast_demand = predictions["prediction"].sum()

    position = InventoryPosition(
        current_inventory=CURRENT_INVENTORY,
        forecast_demand=forecast_demand,
        safety_stock=SAFETY_STOCK,
        lead_time_days=LEAD_TIME_DAYS,
    )
    position.calculate()

    risk = InventoryRisk(
        projected_inventory=position.projected_inventory,
        inventory_gap=position.inventory_gap,
        safety_stock=SAFETY_STOCK,
    )
    risk.evaluate()

    inventory = InventoryAnalysis(
        projected_inventory=position.projected_inventory,
        inventory_gap=position.inventory_gap,
        stockout_risk=risk.stockout_risk,
        overstock_risk=risk.overstock_risk,
        risk_severity=risk.risk_severity,
    )

    daily = forecast_demand / 45
    reorder_point = daily * LEAD_TIME_DAYS + SAFETY_STOCK

    bm = BusinessMetrics(
        current_inventory=CURRENT_INVENTORY,
        forecast_demand=forecast_demand,
        projected_inventory=inventory.projected_inventory,
        reorder_point=reorder_point,
        selling_price=SELLING_PRICE,
        stockout_risk=inventory.stockout_risk,
        overstock_risk=inventory.overstock_risk,
        safety_stock_breach=inventory.projected_inventory < SAFETY_STOCK,
    )
    bm.calculate()

    business = BusinessAnalysis(
        potential_lost_sales=bm.potential_lost_sales,
        revenue_risk=bm.revenue_risk,
        inventory_at_risk=bm.inventory_at_risk,
        recommended_order_quantity=bm.recommended_order_quantity,
        inventory_health_score=bm.inventory_health_score,
    )

    return inventory, business

if "recommendation" not in st.session_state:
    st.session_state.recommendation = None
if "inventory" not in st.session_state:
    st.session_state.inventory = None
if "business" not in st.session_state:
    st.session_state.business = None

st.title("📦 AI Retail Demand Forecasting Copilot")
st.caption("Run the analysis once, then generate multiple AI recommendations.")

col1, col2 = st.columns(2)

with col1:
    if st.button("Run Analysis", use_container_width=True):
        with st.spinner("Running forecasting pipeline..."):
            inv, biz = run_analysis()
            st.session_state.inventory = inv
            st.session_state.business = biz
        st.success("Analysis completed.")

with col2:
    if st.button("Clear History", use_container_width=True):
        st.session_state.recommendation = None
        st.rerun()

if st.session_state.inventory:
    st.subheader("Current Analysis")
    st.write(f"Stockout Risk: {st.session_state.inventory.stockout_risk}")
    st.write(f"Inventory Health Score: {st.session_state.business.inventory_health_score:.0f}")

prompt = st.text_area("Additional Instructions")

if st.button("Generate Recommendation", use_container_width=True):
    if st.session_state.inventory is None:
        st.warning("Run Analysis first.")
    else:
        with st.spinner("Generating recommendation..."):
            st.session_state.recommendation = RecommendationEngine().generate(
                inventory=st.session_state.inventory,
                business=st.session_state.business,
                user_prompt=prompt.strip() or None,
            )

st.markdown("---")

if st.session_state.recommendation is not None:
    rec = st.session_state.recommendation

    st.subheader("Executive Summary")
    st.write(rec.summary)

    st.subheader("Recommendation")
    st.write(rec.recommendation)

    st.subheader("Business Rationale")
    st.write(rec.rationale)
