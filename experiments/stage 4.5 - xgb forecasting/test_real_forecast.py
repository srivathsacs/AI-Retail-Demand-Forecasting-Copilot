import pandas as pd

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(
    str(PROJECT_ROOT)
)

from src.forecasting.xgboost_model import (
    XGBoostForecaster
)

BEST_PARAMS = {
    "n_estimators": 243,
    "max_depth": 9,
    "learning_rate": 0.017951627019300122,
    "min_child_weight": 1,
    "subsample": 0.8625102672650026,
    "colsample_bytree": 0.7589658313348988,
    "gamma": 2.778301781120942,
    "random_state": 42,
}

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

df = pd.read_csv(
    "data/processed/sales_by_category.csv"
)

series = df[
    (df["store_id"] == 44)
    &
    (df["category"] == "GROCERY I")
].copy()

series["date"] = pd.to_datetime(
    series["date"]
)

series["day_of_week"] = (
    series["date"].dt.dayofweek
)

series["month"] = (
    series["date"].dt.month
)

series["year"] = (
    series["date"].dt.year
)

series = series.sort_values(
    "date"
)

series["lag_1"] = (
    series["sales"].shift(1)
)

series["lag_7"] = (
    series["sales"].shift(7)
)

series["lag_14"] = (
    series["sales"].shift(14)
)

series["lag_28"] = (
    series["sales"].shift(28)
)

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

X_train = series[FEATURES]
y_train = series["sales"]

forecaster = XGBoostForecaster(
    **BEST_PARAMS
)

forecaster.fit(
    X_train,
    y_train
)

print("MODEL TRAINED")

future_promotions_df = pd.read_csv(
    "data/future_promos/future_promotions.csv"
)

future_promotions_df["date"] = (
    pd.to_datetime(
        future_promotions_df["date"]
    )
)

forecast_df = forecaster.forecast(
    history_df=series[
        [
            "date",
            "sales",
            "promotion_count",
        ]
    ],
    future_promotions_df=future_promotions_df,
)

forecast_df.to_csv(
    "data/forecasts/store_44_grocery_i_45_day_forecast.csv",
    index=False,
)


print(
    forecast_df.head()
)

print()

print(
    forecast_df.tail()
)

print()

print(
    "TOTAL FORECAST DEMAND:",
    round(
        forecast_df["forecast"].sum(),
        2,
    ),
)