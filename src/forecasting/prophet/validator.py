"""
Module: validator.py

Purpose:
    Perform time-series cross-validation for the Prophet model.

Project Stage:
    Stage 3 - Prophet Forecasting
"""

from pathlib import Path

import pandas as pd
from prophet.diagnostics import (
    cross_validation,
    performance_metrics,
)

from config import PROPHET_CV_METRICS


class ProphetValidator:
    """
    Evaluate a trained Prophet model using time-series cross-validation.
    """

    def evaluate(
        self,
        model,
        initial: str = "1095 days",
        period: str = "90 days",
        horizon: str = "45 days",
    ) -> pd.DataFrame:
        """
        Run cross-validation, save the results and return the metrics.
        """

        cv_results = cross_validation(
            model=model,
            initial=initial,
            period=period,
            horizon=horizon,
        )

        metrics = performance_metrics(cv_results)

        PROPHET_CV_METRICS.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        metrics.to_csv(
            PROPHET_CV_METRICS,
            index=False,
        )

        return metrics