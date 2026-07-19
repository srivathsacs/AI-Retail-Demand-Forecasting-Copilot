"""
Module: inventory_position.py

Purpose:
    Calculate projected inventory levels and inventory gaps.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class InventoryPosition:
    """Calculate inventory position metrics."""

    current_inventory: float
    forecast_demand: float
    safety_stock: float
    lead_time_days: int

    projected_inventory: float = 0.0
    inventory_gap: float = 0.0

    def calculate(self) -> None:
        """Calculate projected inventory and inventory gap."""

        self.projected_inventory = round(
            self.current_inventory - self.forecast_demand,
            2,
        )

        self.inventory_gap = round(
            self.projected_inventory - self.safety_stock,
            2,
        )