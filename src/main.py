"""
Module: main.py

Purpose:
    Production entry point for the AI Retail Demand Forecasting Copilot.
"""

from config import (
    CATEGORY_SALES_DATA,
    CURRENT_INVENTORY,
    ITEMS_DATA,
    LEAD_TIME_DAYS,
    PROPHET_CATEGORY,
    PROPHET_STORE_ID,
    SAFETY_STOCK,
    SELLING_PRICE,
    TRAIN_DATA,
    XGBOOST_CATEGORY,
    XGBOOST_STORE_ID,
)

from data.dataset_builder import DatasetBuilder

from forecasting.prophet.evaluator import ProphetEvaluator
from forecasting.prophet.pipeline import ProphetPipeline
from forecasting.prophet.validator import ProphetValidator
from forecasting.prophet.visualizer import ProphetVisualizer

from forecasting.xgboost.evaluator import XGBoostEvaluator
from forecasting.xgboost.pipeline import XGBoostPipeline
from forecasting.xgboost.validator import XGBoostValidator
from forecasting.xgboost.visualizer import XGBoostVisualizer

from inventory import (
    InventoryAnalysis,
    InventoryPosition,
    InventoryRisk,
)

from metrics import (
    BusinessAnalysis,
    BusinessMetrics,
)


def stage_1() -> None:
    """Build the processed dataset."""

    print("\n========== Stage 1 : Dataset Construction ==========")

    builder = DatasetBuilder()

    builder.build_category_dataset(
        train_path=str(TRAIN_DATA),
        items_path=str(ITEMS_DATA),
        output_path=str(CATEGORY_SALES_DATA),
    )

    print("✓ Dataset created successfully.")


def stage_3() -> None:
    """Run the Prophet forecasting pipeline."""

    print("\n========== Stage 3 : Prophet Forecasting ==========")

    pipeline = ProphetPipeline(CATEGORY_SALES_DATA)

    forecast, test_df = pipeline.run(
        store_id=PROPHET_STORE_ID,
        category=PROPHET_CATEGORY,
    )

    validator = ProphetValidator()

    cv_metrics = validator.evaluate(
        pipeline.model.model
    )

    print("\nAverage Cross Validation Metrics")

    print(f"MAE  : {cv_metrics['mae'].mean():.2f}")
    print(f"RMSE : {cv_metrics['rmse'].mean():.2f}")
    print(f"MAPE : {cv_metrics['mape'].mean() * 100:.2f}%")

    evaluator = ProphetEvaluator()

    results = evaluator.evaluate(
        actual=test_df["y"],
        predicted=forecast["yhat"],
    )

    print("\nHoldout Metrics")

    print(f"MAE  : {results['MAE']:.2f}")
    print(f"RMSE : {results['RMSE']:.2f}")
    print(f"MAPE : {results['MAPE']:.2f}%")

    ProphetVisualizer.plot_components(
        pipeline.model.model,
        forecast,
    )

    ProphetVisualizer.plot_forecast(
        test_df=test_df,
        forecast=forecast,
        title=f"Store {PROPHET_STORE_ID} - {PROPHET_CATEGORY}",
    )


def stage_4():
    """Run the XGBoost forecasting pipeline."""

    print("\n========== Stage 4 : XGBoost Forecasting ==========")

    pipeline = XGBoostPipeline(CATEGORY_SALES_DATA)

    predictions, test_df, series = pipeline.run(
        store_id=XGBOOST_STORE_ID,
        category=XGBOOST_CATEGORY,
    )

    validator = XGBoostValidator()

    cv_metrics = validator.evaluate(
        df=series,
        features=pipeline.FEATURES,
        target=pipeline.TARGET,
        model_params=pipeline.MODEL_PARAMS,
    )

    print("\nAverage Cross Validation Metrics")

    print(f"MAE  : {cv_metrics['MAE'].mean():.2f}")
    print(f"RMSE : {cv_metrics['RMSE'].mean():.2f}")
    print(f"MAPE : {cv_metrics['MAPE'].mean():.2f}%")

    evaluator = XGBoostEvaluator()

    results = evaluator.evaluate(
        actual=predictions["actual"],
        predicted=predictions["prediction"],
    )

    print("\nHoldout Metrics")

    print(f"MAE  : {results['MAE']:.2f}")
    print(f"RMSE : {results['RMSE']:.2f}")
    print(f"MAPE : {results['MAPE']:.2f}%")

    XGBoostVisualizer.plot_forecast(
        actual=predictions["actual"],
        predicted=predictions["prediction"],
        dates=predictions["date"],
        title=f"Store {XGBOOST_STORE_ID} - {XGBOOST_CATEGORY}",
    )

    return predictions


def stage_5(forecast_demand: float) -> InventoryAnalysis:
    """Run the Inventory Analytics stage."""

    print("\n========== Stage 5 : Inventory Analytics ==========")

    inventory = InventoryPosition(
        current_inventory=CURRENT_INVENTORY,
        forecast_demand=forecast_demand,
        safety_stock=SAFETY_STOCK,
        lead_time_days=LEAD_TIME_DAYS,
    )

    inventory.calculate()

    risk = InventoryRisk(
        projected_inventory=inventory.projected_inventory,
        inventory_gap=inventory.inventory_gap,
        safety_stock=SAFETY_STOCK,
    )

    risk.evaluate()

    analysis = InventoryAnalysis(
        projected_inventory=inventory.projected_inventory,
        inventory_gap=inventory.inventory_gap,
        stockout_risk=risk.stockout_risk,
        overstock_risk=risk.overstock_risk,
        risk_severity=risk.risk_severity,
    )

    print(f"Projected Inventory : {analysis.projected_inventory:.2f}")
    print(f"Inventory Gap       : {analysis.inventory_gap:.2f}")
    print(f"Stockout Risk       : {analysis.stockout_risk}")
    print(f"Overstock Risk      : {analysis.overstock_risk}")
    print(f"Risk Severity       : {analysis.risk_severity}")

    return analysis


def stage_6(
    analysis: InventoryAnalysis,
    forecast_demand: float,
) -> BusinessAnalysis:
    """Run the Business Metrics stage."""

    print("\n========== Stage 6 : Business Metrics ==========")

    daily_demand = forecast_demand / 45

    lead_time_demand = (
        daily_demand
        * LEAD_TIME_DAYS
    )

    reorder_point = (
        lead_time_demand
        + SAFETY_STOCK
    )

    metrics = BusinessMetrics(
        current_inventory=CURRENT_INVENTORY,
        forecast_demand=forecast_demand,
        projected_inventory=analysis.projected_inventory,
        reorder_point=reorder_point,
        selling_price=SELLING_PRICE,
        stockout_risk=analysis.stockout_risk,
        overstock_risk=analysis.overstock_risk,
        safety_stock_breach=(
            analysis.projected_inventory
            < SAFETY_STOCK
        ),
    )

    metrics.calculate()

    business = BusinessAnalysis(
        potential_lost_sales=metrics.potential_lost_sales,
        revenue_risk=metrics.revenue_risk,
        inventory_at_risk=metrics.inventory_at_risk,
        recommended_order_quantity=metrics.recommended_order_quantity,
        inventory_health_score=metrics.inventory_health_score,
    )

    print(f"Potential Lost Sales      : {business.potential_lost_sales:.2f}")
    print(f"Revenue Risk              : {business.revenue_risk:.2f}")
    print(f"Inventory At Risk         : {business.inventory_at_risk:.2f}")
    print(f"Recommended Order Quantity: {business.recommended_order_quantity:.2f}")
    print(f"Inventory Health Score    : {business.inventory_health_score:.0f}")

    return business


def main() -> None:

    stage_1()

    stage_3()

    predictions = stage_4()

    forecast_demand = predictions["prediction"].sum()

    inventory = stage_5(forecast_demand)

    business = stage_6(
        inventory,
        forecast_demand,
    )

    _ = business


if __name__ == "__main__":
    main()