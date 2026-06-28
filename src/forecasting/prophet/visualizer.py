"""
Module: visualizer.py

Purpose:
    Visualize Prophet forecasts and model components.

Project Stage:
    Stage 3 - Prophet Forecasting
"""

import matplotlib.pyplot as plt
import pandas as pd


class ProphetVisualizer:
    """
    Create visualizations for Prophet forecasts.
    """

    @staticmethod
    def plot_components(model, forecast: pd.DataFrame) -> None:
        """
        Display Prophet trend and seasonality components.
        """

        model.plot_components(forecast)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_forecast(
        test_df: pd.DataFrame,
        forecast: pd.DataFrame,
        title: str,
    ) -> None:
        """
        Plot actual vs forecast with prediction intervals.
        """

        plot_df = test_df.copy()

        plot_df["forecast"] = forecast["yhat"].values
        plot_df["lower"] = forecast["yhat_lower"].values
        plot_df["upper"] = forecast["yhat_upper"].values

        # Sort by date before plotting.
        plot_df = plot_df.sort_values("ds").reset_index(drop=True)

        plt.figure(figsize=(12, 6))

        plt.plot(
            plot_df["ds"],
            plot_df["y"],
            label="Actual",
            linewidth=2,
        )

        plt.plot(
            plot_df["ds"],
            plot_df["forecast"],
            label="Forecast",
            linewidth=2,
        )

        plt.fill_between(
            plot_df["ds"],
            plot_df["lower"],
            plot_df["upper"],
            alpha=0.2,
            label="Prediction Interval",
        )

        plt.title(title)
        plt.xlabel("Date")
        plt.ylabel("Sales")
        plt.legend()

        plt.tight_layout()
        plt.show()