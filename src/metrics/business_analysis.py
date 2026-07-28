"""
Module: business_analysis.py

Purpose:
    Represent the output of the Business Metrics stage.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class BusinessAnalysis:
    """Business Metrics result."""

    potential_lost_sales: float
    revenue_risk: float
    inventory_at_risk: float
    recommended_order_quantity: float
    inventory_health_score: float