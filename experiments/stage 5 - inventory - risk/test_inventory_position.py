from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(
    str(PROJECT_ROOT)
)

from src.inventory.inventory_position import (
    InventoryPosition
)


inventory = InventoryPosition(
    current_inventory=500000,
    forecast_demand=443847.65,
    safety_stock=50000,
    lead_time_days=30,
)

inventory.calculate()

print(
    "Projected Inventory:",
    inventory.projected_inventory
)

print(
    "Inventory Gap:",
    inventory.inventory_gap
)