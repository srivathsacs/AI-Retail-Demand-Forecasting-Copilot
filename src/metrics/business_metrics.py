"""
Module: business_metrics.py

Purpose:
    Calculate business metrics from inventory analytics.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class BusinessMetrics:
    """Calculate business metrics."""

    current_inventory: float
    forecast_demand: float
    projected_inventory: float
    reorder_point: float
    selling_price: float
    stockout_risk: str
    overstock_risk: str
    safety_stock_breach: bool

    potential_lost_sales: float = 0.0
    revenue_risk: float = 0.0
    inventory_at_risk: float = 0.0
    recommended_order_quantity: float = 0.0
    inventory_health_score: float = 0.0

    def calculate(self) -> None:
        """Calculate business metrics."""

        self.potential_lost_sales = round(
            max(
                0,
                self.forecast_demand - self.current_inventory,
            ),
            2,
        )

        self.revenue_risk = round(
            self.potential_lost_sales * self.selling_price,
            2,
        )

        self.inventory_at_risk = round(
            max(
                0,
                self.projected_inventory - self.reorder_point,
            ),
            2,
        )

        self.recommended_order_quantity = round(
            max(
                0,
                self.reorder_point - self.current_inventory,
            ),
            2,
        )

        score = 100

        if self.stockout_risk == "CRITICAL":
            score -= 70

        elif self.stockout_risk == "HIGH":
            score -= 50

        elif self.stockout_risk == "MEDIUM":
            score -= 20

        if self.overstock_risk == "HIGH":
            score -= 30

        elif self.overstock_risk == "MEDIUM":
            score -= 15

        if self.safety_stock_breach:
            score -= 20

        self.inventory_health_score = max(
            0,
            min(
                100,
                score,
            ),
        )