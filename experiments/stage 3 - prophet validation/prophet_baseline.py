"""
Train and evaluate a Prophet forecasting model.

Workflow:
1. Load one forecasting series
2. Create train/test split
3. Train Prophet
4. Generate forecasts
5. Evaluate using MAE, RMSE, and MAPE
"""


import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics

# Load data
df = pd.read_csv("data/processed/sales_by_category.csv")

# Select one forecasting series
series = df[
    (df["store_id"] == 44) &
    (df["category"] == "GROCERY I")
].copy()

# Prophet format
# prophet_df = series[["date", "sales"]].rename(
#     columns={
#         "date": "ds",
#         "sales": "y"
#     }
# )

prophet_df = series[
    ["date", "sales", "promotion_count"]
].rename(
    columns={
        "date": "ds",
        "sales": "y"
    }
)

prophet_df["ds"] = pd.to_datetime(prophet_df["ds"])

# Train / Test Split
split_date = "2017-07-01"

train_df = prophet_df[prophet_df["ds"] < split_date]
test_df = prophet_df[prophet_df["ds"] >= split_date]

print("Train:", train_df.shape)
print("Test :", test_df.shape)

# Train Prophet
#model = Prophet()

model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    seasonality_mode="multiplicative"
)

model.add_regressor("promotion_count")

model.fit(train_df)

cv_results = cross_validation(
    model,
    initial="1095 days",
    period="90 days",
    horizon="45 days"
)



cv_metrics = performance_metrics(cv_results)

print("\nCross Validation Metrics")
print(
    cv_metrics[
        ["horizon", "mae", "rmse", "mape"]
    ]
)

print("\nAverage CV Metrics")
print(f"MAE  : {cv_metrics['mae'].mean():.2f}")
print(f"RMSE : {cv_metrics['rmse'].mean():.2f}")
print(f"MAPE : {cv_metrics['mape'].mean() * 100:.2f}%")

print("Model trained successfully")


# Predict test period

#future = test_df[["ds"]].copy()

future = test_df[
    ["ds", "promotion_count"]
].copy()

forecast = model.predict(future)

fig2 = model.plot_components(forecast)
plt.show()

print(
    forecast[
        ["ds", "yhat", "yhat_lower", "yhat_upper"]
    ].head()
)


actual = test_df["y"].values
predicted = forecast["yhat"].values

mae = mean_absolute_error(actual, predicted)

rmse = mean_squared_error(
    actual,
    predicted
) ** 0.5

mape = (
    abs((actual - predicted) / actual).mean()
) * 100

print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"MAPE : {mape:.2f}%")


prophet_results = pd.DataFrame({
    "date": test_df["ds"].values,
    "actual": actual,
    "prophet_prediction": predicted
})

prophet_results.to_csv(
    "data/prophet_holdout_predictions.csv",
    index=False
)



# Actual vs Predicted Plot

plot_df = test_df.copy()


plot_df["forecast"] = forecast["yhat"].values
plot_df["lower"] = forecast["yhat_lower"].values
plot_df["upper"] = forecast["yhat_upper"].values

plot_df = plot_df.sort_values("ds")


plt.figure(figsize=(12, 6))

plt.plot(
    plot_df["ds"],
    plot_df["y"],
    label="Actual"
)

plt.plot(
    plot_df["ds"],
    plot_df["forecast"],
    label="Forecast"
)

plt.fill_between(
    plot_df["ds"],
    plot_df["lower"],
    plot_df["upper"],
    alpha=0.2,
    label="Prediction Interval"
)

plt.title("Store 44 - GROCERY I\nActual vs Forecast")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.legend()

plt.show()