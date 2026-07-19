"""
Module: risk_engine.py

Purpose:
    Evaluate inventory risk based on projected inventory levels.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class InventoryRisk:
    """Evaluate inventory risk levels."""

    projected_inventory: float
    inventory_gap: float
    safety_stock: float

    stockout_risk: str = ""
    overstock_risk: str = ""
    risk_severity: str = ""

    def evaluate(self) -> None:
        """Evaluate inventory risk."""

        if self.inventory_gap < -self.safety_stock:
            self.stockout_risk = "CRITICAL"

        elif self.inventory_gap < 0:
            self.stockout_risk = "HIGH"

        elif self.inventory_gap < (self.safety_stock * 0.25):
            self.stockout_risk = "MEDIUM"

        else:
            self.stockout_risk = "LOW"

        if self.projected_inventory > (self.safety_stock * 4):
            self.overstock_risk = "HIGH"

        elif self.projected_inventory > (self.safety_stock * 3):
            self.overstock_risk = "MEDIUM"

        else:
            self.overstock_risk = "LOW"

        if (
            self.stockout_risk == "CRITICAL"
            or self.overstock_risk == "HIGH"
        ):
            self.risk_severity = "HIGH"

        elif (
            self.stockout_risk == "HIGH"
            or self.overstock_risk == "MEDIUM"
        ):
            self.risk_severity = "MEDIUM"

        elif self.stockout_risk == "MEDIUM":
            self.risk_severity = "LOW"

        else:
            self.risk_severity = "MINIMAL"