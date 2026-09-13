from fastapi import FastAPI, HTTPException

from api.schemas import (
    PredictionRequest,
    PredictionResponse,
    RecommendationRequest,
    RecommendationResponse,
)
from recommendation import RecommendationEngine
from services.demand_forecasting_service import run_demand_forecasting


app = FastAPI(title="AI Retail Demand Forecasting Copilot API")


# Stores the most recent forecasting result for local API use.
_analysis_cache = None
_analysis_store_id = None
_analysis_category = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    return {"status": "ready"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    global _analysis_cache
    global _analysis_store_id
    global _analysis_category

    inventory, business = run_demand_forecasting(
        store_id=request.store_id,
        category=request.category,
    )

    _analysis_cache = (inventory, business)
    _analysis_store_id = request.store_id
    _analysis_category = request.category

    return {
        "projected_inventory": float(inventory.projected_inventory),
        "inventory_gap": float(inventory.inventory_gap),
        "stockout_risk": inventory.stockout_risk,
        "overstock_risk": inventory.overstock_risk,
        "risk_severity": inventory.risk_severity,
        "recommended_order_quantity": float(business.recommended_order_quantity),
        "inventory_health_score": float(business.inventory_health_score),
    }


@app.post("/recommend", response_model=RecommendationResponse)
def recommend(request: RecommendationRequest):
    if _analysis_cache is None:
        raise HTTPException(
            status_code=400,
            detail="Run /predict before requesting a recommendation.",
        )

    if (
        request.store_id != _analysis_store_id
        or request.category != _analysis_category
    ):
        raise HTTPException(
            status_code=400,
            detail="Requested store/category does not match the latest analysis.",
        )

    inventory, business = _analysis_cache

    recommendation = RecommendationEngine().generate(
        inventory=inventory,
        business=business,
        user_prompt=request.user_prompt,
    )

    return {
        "summary": recommendation.summary,
        "recommendation": recommendation.recommendation,
        "rationale": recommendation.rationale,
    }