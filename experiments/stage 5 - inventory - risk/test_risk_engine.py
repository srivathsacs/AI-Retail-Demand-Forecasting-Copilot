from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(
    str(PROJECT_ROOT)
)

from src.inventory.risk_engine import (
    InventoryRisk
)


risk = InventoryRisk(
    projected_inventory=56152.35,
    inventory_gap=6152.35,
    safety_stock=50000,
)

risk.evaluate()

print(
    "Stockout Risk:",
    risk.stockout_risk
)

print(
    "Overstock Risk:",
    risk.overstock_risk
)

print(
    "Risk Severity:",
    risk.risk_severity
)