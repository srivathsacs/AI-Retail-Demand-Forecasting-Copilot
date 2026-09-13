from pydantic import BaseModel


class PredictionRequest(BaseModel):
    store_id: int
    category: str


class PredictionResponse(BaseModel):
    projected_inventory: float
    inventory_gap: float
    stockout_risk: str
    overstock_risk: str
    risk_severity: str
    recommended_order_quantity: float
    inventory_health_score: float


class RecommendationRequest(BaseModel):
    store_id: int
    category: str
    user_prompt: str | None = None


class RecommendationResponse(BaseModel):
    summary: str
    recommendation: str
    rationale: str