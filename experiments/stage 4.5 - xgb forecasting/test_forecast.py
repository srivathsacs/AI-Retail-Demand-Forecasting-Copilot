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

history_df = pd.DataFrame(
    {
        "date": pd.date_range(
            start="2024-01-01",
            periods=60,
            freq="D"
        ),
        "sales": range(100, 160),
        "promotion_count": [10] * 60,
    }
)

future_promotions_df = pd.DataFrame(
    {
        "date": pd.date_range(
            start="2024-03-01",
            periods=5,
            freq="D"
        ),
        "promotion_count": [20] * 5,
    }
)

forecaster = XGBoostForecaster(
    n_estimators=10,
    random_state=42,
)

X_dummy = pd.DataFrame(
    {
        "promotion_count": [10] * 60,
        "day_of_week": [0] * 60,
        "month": [1] * 60,
        "year": [2024] * 60,
        "lag_1": [100] * 60,
        "lag_7": [100] * 60,
        "lag_14": [100] * 60,
        "lag_28": [100] * 60,
        "rolling_mean_7": [100] * 60,
        "rolling_mean_28": [100] * 60,
    }
)

y_dummy = history_df["sales"]

forecaster.fit(
    X_dummy,
    y_dummy,
)

forecast_df = forecaster.forecast(
    history_df=history_df,
    future_promotions_df=future_promotions_df,
)

print(forecast_df)