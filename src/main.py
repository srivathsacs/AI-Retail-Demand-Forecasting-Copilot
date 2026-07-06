"""
Module: main.py

Purpose:
    Production entry point for the AI Retail Demand Forecasting Copilot.
"""

from config import (
    CATEGORY_SALES_DATA,
    ITEMS_DATA,
    PROPHET_CATEGORY,
    PROPHET_STORE_ID,
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


def stage_4() -> None:
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


def main() -> None:

    stage_1()

    stage_3()

    stage_4()


if __name__ == "__main__":
    main()