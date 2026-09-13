from config import (
    CATEGORY_SALES_DATA,
    CURRENT_INVENTORY,
    ITEMS_DATA,
    LEAD_TIME_DAYS,
    SAFETY_STOCK,
    SELLING_PRICE,
    TRAIN_DATA,
)
from data.dataset_builder import DatasetBuilder
from forecasting.prophet.pipeline import ProphetPipeline
from forecasting.xgboost.pipeline import XGBoostPipeline
from inventory import InventoryAnalysis, InventoryPosition, InventoryRisk
from metrics import BusinessAnalysis, BusinessMetrics


def build_dataset():
    DatasetBuilder().build_category_dataset(
        train_path=str(TRAIN_DATA),
        items_path=str(ITEMS_DATA),
        output_path=str(CATEGORY_SALES_DATA),
    )


def run_demand_forecasting(
    store_id: int,
    category: str,
):
    build_dataset()

    ProphetPipeline(CATEGORY_SALES_DATA).run(
        store_id=store_id,
        category=category,
    )

    predictions, _, _ = XGBoostPipeline(CATEGORY_SALES_DATA).run(
        store_id=store_id,
        category=category,
    )

    forecast_demand = predictions["prediction"].sum()

    position = InventoryPosition(
        current_inventory=CURRENT_INVENTORY,
        forecast_demand=forecast_demand,
        safety_stock=SAFETY_STOCK,
        lead_time_days=LEAD_TIME_DAYS,
    )
    position.calculate()

    risk = InventoryRisk(
        projected_inventory=position.projected_inventory,
        inventory_gap=position.inventory_gap,
        safety_stock=SAFETY_STOCK,
    )
    risk.evaluate()

    inventory = InventoryAnalysis(
        projected_inventory=position.projected_inventory,
        inventory_gap=position.inventory_gap,
        stockout_risk=risk.stockout_risk,
        overstock_risk=risk.overstock_risk,
        risk_severity=risk.risk_severity,
    )

    daily = forecast_demand / 45
    reorder_point = daily * LEAD_TIME_DAYS + SAFETY_STOCK

    bm = BusinessMetrics(
        current_inventory=CURRENT_INVENTORY,
        forecast_demand=forecast_demand,
        projected_inventory=inventory.projected_inventory,
        reorder_point=reorder_point,
        selling_price=SELLING_PRICE,
        stockout_risk=inventory.stockout_risk,
        overstock_risk=inventory.overstock_risk,
        safety_stock_breach=inventory.projected_inventory < SAFETY_STOCK,
    )
    bm.calculate()

    business = BusinessAnalysis(
        potential_lost_sales=bm.potential_lost_sales,
        revenue_risk=bm.revenue_risk,
        inventory_at_risk=bm.inventory_at_risk,
        recommended_order_quantity=bm.recommended_order_quantity,
        inventory_health_score=bm.inventory_health_score,
    )

    return inventory, business