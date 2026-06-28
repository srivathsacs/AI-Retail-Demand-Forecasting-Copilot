"""
Module: pipeline.py

Purpose:
    Execute the complete Prophet forecasting workflow.

Workflow:
    1. Load processed dataset
    2. Select a store/category
    3. Prepare Prophet dataset
    4. Split train/test data
    5. Train Prophet
    6. Generate forecasts
    7. Save holdout predictions

Project Stage:
    Stage 3 - Prophet Forecasting
"""

from pathlib import Path

import pandas as pd

from config import PROPHET_HOLDOUT_PREDICTIONS
from forecasting.prophet.model import ProphetModel


class ProphetPipeline:
    """
    End-to-end Prophet forecasting pipeline.
    """

    def __init__(self, data_path: str | Path) -> None:

        self.data_path = Path(data_path)
        self.model: ProphetModel | None = None

    def run(
        self,
        store_id: int,
        category: str,
        split_date: str = "2017-07-01",
    ) -> tuple[pd.DataFrame, pd.DataFrame]:

        df = pd.read_csv(self.data_path)

        series = df[
            (df["store_id"] == store_id)
            & (df["category"] == category)
        ].copy()

        prophet_df = (
            series[
                ["date", "sales", "promotion_count"]
            ]
            .rename(
                columns={
                    "date": "ds",
                    "sales": "y",
                }
            )
        )

        prophet_df["ds"] = pd.to_datetime(prophet_df["ds"])

        train_df = prophet_df[prophet_df["ds"] < split_date]

        test_df = prophet_df[prophet_df["ds"] >= split_date]

        self.model = ProphetModel()

        self.model.add_promotion_regressor()

        self.model.fit(train_df)

        future_df = test_df[
            ["ds", "promotion_count"]
        ].copy()

        forecast = self.model.predict(future_df)

        predictions = pd.DataFrame(
            {
                "date": test_df["ds"].values,
                "actual": test_df["y"].values,
                "prediction": forecast["yhat"].values,
                "lower": forecast["yhat_lower"].values,
                "upper": forecast["yhat_upper"].values,
            }
        )

        PROPHET_HOLDOUT_PREDICTIONS.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        predictions.to_csv(
            PROPHET_HOLDOUT_PREDICTIONS,
            index=False,
        )

        return forecast, test_df