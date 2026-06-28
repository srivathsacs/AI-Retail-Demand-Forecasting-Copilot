"""
Module: evaluator.py

Purpose:
    Calculate forecasting performance metrics.

Project Stage:
    Stage 3 - Prophet Forecasting
"""

import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    root_mean_squared_error,
)


class ProphetEvaluator:
    """
    Calculate forecasting accuracy metrics.
    """

    def evaluate(
        self,
        actual: pd.Series,
        predicted: pd.Series,
    ) -> dict[str, float]:
        """
        Calculate MAE, RMSE and MAPE.
        """

        # Reset index so both Series align.
        actual = actual.reset_index(drop=True)
        predicted = predicted.reset_index(drop=True)

        mae = mean_absolute_error(
            actual,
            predicted,
        )

        rmse = root_mean_squared_error(
            actual,
            predicted,
        )

        # Ignore rows where actual sales are zero.
        valid_rows = actual != 0

        if valid_rows.any():
            mape = (
                (
                    (
                        actual.loc[valid_rows]
                        - predicted.loc[valid_rows]
                    ).abs()
                    / actual.loc[valid_rows]
                ).mean()
                * 100
            )
        else:
            mape = 0.0

        return {
            "MAE": mae,
            "RMSE": rmse,
            "MAPE": mape,
        }