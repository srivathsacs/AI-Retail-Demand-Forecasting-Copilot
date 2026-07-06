"""
Module: pipeline.py

Purpose:
    Execute the complete XGBoost forecasting workflow.

Workflow:
    1. Load processed dataset
    2. Select a store/category
    3. Create calendar features
    4. Create lag features
    5. Split train/test data
    6. Train XGBoost
    7. Generate holdout predictions

Project Stage:
    Stage 4 - XGBoost Forecasting
"""

from pathlib import Path

import pandas as pd

from config import (
    TRAIN_TEST_SPLIT_DATE,
    XGBOOST_CATEGORY,
    XGBOOST_HOLDOUT_PREDICTIONS,
    XGBOOST_STORE_ID,
)

from forecasting.xgboost.model import XGBoostModel


class XGBoostPipeline:
    """
    End-to-end XGBoost forecasting pipeline.
    """

    FEATURES = [
        "promotion_count",
        "day_of_week",
        "month",
        "year",
        "lag_1",
        "lag_7",
        "lag_14",
        "lag_28",
        "rolling_mean_7",
        "rolling_mean_28",
    ]

    TARGET = "sales"

    MODEL_PARAMS = {
        "n_estimators": 243,
        "max_depth": 9,
        "learning_rate": 0.017951627019300122,
        "min_child_weight": 1,
        "subsample": 0.8625102672650026,
        "colsample_bytree": 0.7589658313348988,
        "gamma": 2.778301781120942,
        "random_state": 42,
    }

    def __init__(
        self,
        data_path: str | Path,
    ) -> None:

        self.data_path = Path(data_path)
        self.model: XGBoostModel | None = None

    def run(
        self,
        store_id: int = XGBOOST_STORE_ID,
        category: str = XGBOOST_CATEGORY,
        split_date: str = TRAIN_TEST_SPLIT_DATE,
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

        df = pd.read_csv(self.data_path)

        series = df[
            (df["store_id"] == store_id)
            & (df["category"] == category)
        ].copy()

        series["date"] = pd.to_datetime(series["date"])

        series["day_of_week"] = series["date"].dt.dayofweek
        series["month"] = series["date"].dt.month
        series["year"] = series["date"].dt.year

        series = series.sort_values("date")

        series["lag_1"] = series["sales"].shift(1)
        series["lag_7"] = series["sales"].shift(7)
        series["lag_14"] = series["sales"].shift(14)
        series["lag_28"] = series["sales"].shift(28)

        series["rolling_mean_7"] = (
            series["sales"]
            .shift(1)
            .rolling(7)
            .mean()
        )

        series["rolling_mean_28"] = (
            series["sales"]
            .shift(1)
            .rolling(28)
            .mean()
        )

        series = series.dropna().copy()

        train_df = series[
            series["date"] < split_date
        ]

        test_df = series[
            series["date"] >= split_date
        ]

        self.model = XGBoostModel(
            **self.MODEL_PARAMS,
        )

        self.model.fit(
            train_df[self.FEATURES],
            train_df[self.TARGET],
        )

        predictions = self.model.predict(
            test_df[self.FEATURES],
        )

        prediction_df = pd.DataFrame(
            {
                "date": test_df["date"].values,
                "actual": test_df["sales"].values,
                "prediction": predictions,
            }
        )

        XGBOOST_HOLDOUT_PREDICTIONS.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        prediction_df.to_csv(
            XGBOOST_HOLDOUT_PREDICTIONS,
            index=False,
        )

        return prediction_df, test_df, series