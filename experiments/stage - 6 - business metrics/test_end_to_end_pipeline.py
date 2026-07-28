from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(
    str(PROJECT_ROOT)
)

from src.inventory.inventory_position import (
    InventoryPosition
)

from src.inventory.risk_engine import (
    InventoryRisk
)

from src.metrics.business_metrics import (
    BusinessMetrics
)


# ----------------------------------
# INPUTS
# ----------------------------------

current_inventory = 500000

forecast_demand = 443847.65

safety_stock = 50000

lead_time_days = 30

selling_price = 1.0


# ----------------------------------
# INVENTORY POSITION
# ----------------------------------

inventory = InventoryPosition(
    current_inventory=current_inventory,
    forecast_demand=forecast_demand,
    safety_stock=safety_stock,
    lead_time_days=lead_time_days,
)

inventory.calculate()


# ----------------------------------
# RISK ENGINE
# ----------------------------------

risk = InventoryRisk(
    projected_inventory=inventory.projected_inventory,
    inventory_gap=inventory.inventory_gap,
    safety_stock=safety_stock,
)

risk.evaluate()


# ----------------------------------
# BUSINESS METRICS
# ----------------------------------

daily_demand = forecast_demand / 45

lead_time_demand = (
    daily_demand
    * lead_time_days
)

reorder_point = (
    lead_time_demand
    + safety_stock
)

metrics = BusinessMetrics(
    current_inventory=current_inventory,
    forecast_demand=forecast_demand,
    projected_inventory=inventory.projected_inventory,
    reorder_point=reorder_point,
    selling_price=selling_price,
    stockout_risk=risk.stockout_risk,
    overstock_risk=risk.overstock_risk,
    safety_stock_breach=(
        inventory.projected_inventory
        < safety_stock
    ),
)

metrics.calculate()


# ----------------------------------
# RESULTS
# ----------------------------------

print("\nINVENTORY POSITION")
print("------------------")

print(
    "Projected Inventory:",
    inventory.projected_inventory,
)

print(
    "Inventory Gap:",
    inventory.inventory_gap,
)

print("\nRISK ENGINE")
print("-----------")

print(
    "Stockout Risk:",
    risk.stockout_risk,
)

print(
    "Overstock Risk:",
    risk.overstock_risk,
)

print(
    "Risk Severity:",
    risk.risk_severity,
)

print("\nBUSINESS METRICS")
print("----------------")

print(
    "Potential Lost Sales:",
    metrics.potential_lost_sales,
)

print(
    "Revenue Risk:",
    metrics.revenue_risk,
)

print(
    "Inventory At Risk:",
    metrics.inventory_at_risk,
)

print(
    "Recommended Order Quantity:",
    metrics.recommended_order_quantity,
)

print(
    "Inventory Health Score:",
    metrics.inventory_health_score,
)