"""
Module: inventory_analysis.py

Purpose:
    Represent the output of the Inventory Analytics stage.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class InventoryAnalysis:
    """Inventory Analytics result."""

    projected_inventory: float
    inventory_gap: float

    stockout_risk: str
    overstock_risk: str

    risk_severity: str