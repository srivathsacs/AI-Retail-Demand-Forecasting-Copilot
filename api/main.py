from fastapi import FastAPI

from api.schemas import PredictionRequest, PredictionResponse
from services.demand_forecasting_service import run_demand_forecasting


app = FastAPI(title="AI Retail Demand Forecasting Copilot API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    return {"status": "ready"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    inventory, business = run_demand_forecasting(
        store_id=request.store_id,
        category=request.category,
    )

    return {
        "projected_inventory": float(inventory.projected_inventory),
        "inventory_gap": float(inventory.inventory_gap),
        "stockout_risk": inventory.stockout_risk,
        "overstock_risk": inventory.overstock_risk,
        "risk_severity": inventory.risk_severity,
        "recommended_order_quantity": float(business.recommended_order_quantity),
        "inventory_health_score": float(business.inventory_health_score),
    }