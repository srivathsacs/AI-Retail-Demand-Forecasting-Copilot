"""
Module: visualizer.py

Purpose:
    Visualize XGBoost forecasting results.

Project Stage:
    Stage 4 - XGBoost Forecasting
"""

import matplotlib.pyplot as plt
import pandas as pd


class XGBoostVisualizer:
    """
    Create visualizations for XGBoost forecasts.
    """

    @staticmethod
    def plot_forecast(
        actual: pd.Series,
        predicted: pd.Series,
        dates: pd.Series,
        title: str,
    ) -> None:
        """
        Plot actual vs predicted sales.
        """

        plt.figure(figsize=(12, 6))

        plt.plot(
            dates,
            actual,
            label="Actual",
            linewidth=2,
        )

        plt.plot(
            dates,
            predicted,
            label="Prediction",
            linewidth=2,
        )

        plt.title(title)
        plt.xlabel("Date")
        plt.ylabel("Sales")
        plt.legend()

        plt.tight_layout()
        plt.show()