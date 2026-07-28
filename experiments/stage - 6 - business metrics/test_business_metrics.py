from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(
    str(PROJECT_ROOT)
)

from src.metrics.business_metrics import (
    BusinessMetrics
)


metrics = BusinessMetrics(
    current_inventory=500000,
    forecast_demand=443847.65,
    projected_inventory=56152.35,
    reorder_point=345898.43,
    selling_price=1.0,
    stockout_risk="MEDIUM",
    overstock_risk="LOW",
    safety_stock_breach=False,
)

metrics.calculate()

print(
    "Potential Lost Sales:",
    metrics.potential_lost_sales
)

print(
    "Revenue Risk:",
    metrics.revenue_risk
)

print(
    "Inventory At Risk:",
    metrics.inventory_at_risk
)

print(
    "Recommended Order Quantity:",
    metrics.recommended_order_quantity
)

print(
    "Inventory Health Score:",
    metrics.inventory_health_score
)