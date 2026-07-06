"""
Module: validator.py

Purpose:
    Perform time-series cross-validation for the XGBoost model.

Project Stage:
    Stage 4 - XGBoost Forecasting
"""

import pandas as pd

from config import XGBOOST_CV_METRICS

from forecasting.xgboost.evaluator import XGBoostEvaluator
from forecasting.xgboost.model import XGBoostModel


class XGBoostValidator:
    """
    Evaluate an XGBoost model using rolling time-series cross-validation.
    """

    def create_cv_cutoffs(
        self,
        dates: pd.Series,
        initial_days: int = 1095,
        horizon_days: int = 45,
        step_days: int = 90,
    ) -> list[pd.Timestamp]:
        """
        Create rolling cross-validation cutoff dates.
        """

        cutoffs = []

        current_cutoff = (
            dates.min()
            + pd.Timedelta(days=initial_days)
        )

        last_cutoff = (
            dates.max()
            - pd.Timedelta(days=horizon_days)
        )

        while current_cutoff <= last_cutoff:

            cutoffs.append(current_cutoff)

            current_cutoff += pd.Timedelta(
                days=step_days
            )

        return cutoffs

    def evaluate(
        self,
        df: pd.DataFrame,
        features: list[str],
        target: str,
        model_params: dict,
        initial_days: int = 1095,
        horizon_days: int = 45,
        step_days: int = 90,
    ) -> pd.DataFrame:
        """
        Run rolling time-series cross-validation.
        """

        evaluator = XGBoostEvaluator()

        results = []

        cutoffs = self.create_cv_cutoffs(
            dates=df["date"],
            initial_days=initial_days,
            horizon_days=horizon_days,
            step_days=step_days,
        )

        for cutoff in cutoffs:

            train_df = df[
                df["date"] <= cutoff
            ].copy()

            test_end = (
                cutoff
                + pd.Timedelta(days=horizon_days)
            )

            test_df = df[
                (df["date"] > cutoff)
                & (df["date"] <= test_end)
            ].copy()

            model = XGBoostModel(
                **model_params
            )

            model.fit(
                train_df[features],
                train_df[target],
            )

            predictions = model.predict(
                test_df[features],
            )

            metrics = evaluator.evaluate(
                actual=test_df[target],
                predicted=pd.Series(predictions),
            )

            results.append(metrics)

        metrics_df = pd.DataFrame(results)

        XGBOOST_CV_METRICS.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        metrics_df.to_csv(
            XGBOOST_CV_METRICS,
            index=False,
        )

        return metrics_df