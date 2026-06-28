"""
Module: model.py

Purpose:
    Wrapper around Meta Prophet.

Why this file exists:
    Encapsulates Prophet so the rest of the application does not depend
    directly on the Prophet API.

Project Stage:
    Stage 3 - Prophet Forecasting
"""

from prophet import Prophet
import pandas as pd


class ProphetModel:
    """
    Wrapper class for the Prophet forecasting model.
    """

    def __init__(
        self,
        yearly_seasonality: bool = True,
        weekly_seasonality: bool = True,
        seasonality_mode: str = "multiplicative",
    ) -> None:
        """
        Initialize a Prophet model.
        """

        self.model = Prophet(
            yearly_seasonality=yearly_seasonality,
            weekly_seasonality=weekly_seasonality,
            seasonality_mode=seasonality_mode,
        )

    def add_promotion_regressor(self) -> None:
        """
        Add promotion_count as an external regressor.
        """

        self.model.add_regressor("promotion_count")

    def fit(self, train_df: pd.DataFrame) -> None:
        """
        Train the Prophet model.

        Parameters
        ----------
        train_df : pd.DataFrame
            Training dataframe containing:
            - ds
            - y
            - promotion_count
        """

        self.model.fit(train_df)

    def predict(self, future_df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate forecasts.

        Parameters
        ----------
        future_df : pd.DataFrame
            Future dataframe.

        Returns
        -------
        pd.DataFrame
            Prophet forecast.
        """

        return self.model.predict(future_df)