"""
Module: model.py

Purpose:
    Wrapper around XGBoost.

Why this file exists:
    Encapsulates XGBoost so the rest of the application does not depend
    directly on the XGBoost API.

Project Stage:
    Stage 4 - XGBoost Forecasting
"""

import pandas as pd
from xgboost import XGBRegressor


class XGBoostModel:
    """
    Wrapper class for the XGBoost forecasting model.
    """

    def __init__(
        self,
        **model_params,
    ) -> None:
        """
        Initialize an XGBoost model.
        """

        self.model = XGBRegressor(
            **model_params,
        )

    def fit(
        self,
        X_train: pd.DataFrame,
        y_train: pd.Series,
    ) -> None:
        """
        Train the XGBoost model.
        """

        self.model.fit(
            X_train,
            y_train,
        )

    def predict(
        self,
        X_test: pd.DataFrame,
    ) -> pd.Series:
        """
        Generate predictions.
        """

        return self.model.predict(
            X_test,
        )