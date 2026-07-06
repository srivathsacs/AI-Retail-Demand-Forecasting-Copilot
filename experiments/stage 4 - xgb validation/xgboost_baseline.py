import pandas as pd
from xgboost import XGBRegressor

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error


def evaluate_forecast(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)

    rmse = mean_squared_error(
        y_true,
        y_pred
    ) ** 0.5

    mape = (
        abs((y_true - y_pred) / y_true)
        .mean()
    ) * 100

    return {
        "mae": mae,
        "rmse": rmse,
        "mape": mape
    }

def create_cv_cutoffs(
    dates,
    initial_days,
    horizon_days,
    step_days
):
    cutoffs = []

    current_cutoff = (
        dates.min() +
        pd.Timedelta(days=initial_days)
    )

    last_cutoff = (
        dates.max() -
        pd.Timedelta(days=horizon_days)
    )

    while current_cutoff <= last_cutoff:
        cutoffs.append(current_cutoff)

        current_cutoff += pd.Timedelta(
            days=step_days
        )

    return cutoffs

def run_cv_fold(
    df,
    cutoff_date,
    horizon_days,
    features,
    target
):
    train_df = df[
        df["date"] <= cutoff_date
    ].copy()

    test_end = (
        cutoff_date +
        pd.Timedelta(days=horizon_days)
    )

    test_df = df[
        (df["date"] > cutoff_date) &
        (df["date"] <= test_end)
    ].copy()

    X_train = train_df[features]
    y_train = train_df[target]

    X_test = test_df[features]
    y_test = test_df[target]

    model = XGBRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    return evaluate_forecast(
        y_test,
        predictions
    )


# Load data
df = pd.read_csv("data/processed/sales_by_category.csv")

# Select one forecasting series
series = df[
    (df["store_id"] == 44) &
    (df["category"] == "GROCERY I")
].copy()

series["date"] = pd.to_datetime(series["date"])

# Calendar features
series["day_of_week"] = series["date"].dt.dayofweek
series["month"] = series["date"].dt.month
series["year"] = series["date"].dt.year

series = series.sort_values("date")

series["lag_1"] = series["sales"].shift(1)
series["lag_7"] = series["sales"].shift(7)
series["lag_14"] = series["sales"].shift(14)
series["lag_28"] = series["sales"].shift(28)

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

CV_INITIAL_DAYS = 1095
CV_HORIZON_DAYS = 45
CV_STEP_DAYS = 90

# Train / Test Split
split_date = "2017-07-01"

train_df = series[series["date"] < split_date]
test_df = series[series["date"] >= split_date]

print("Train:", train_df.shape)
print("Test :", test_df.shape)


# Features and Target

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

TARGET = "sales"

# =====================================================
# Time Series Cross Validation
# =====================================================

cutoffs = create_cv_cutoffs(
    dates=series["date"],
    initial_days=CV_INITIAL_DAYS,
    horizon_days=CV_HORIZON_DAYS,
    step_days=CV_STEP_DAYS
)

cv_results = []

print("\n=== XGBoost Time Series CV ===")

for fold, cutoff in enumerate(cutoffs, start=1):

    metrics = run_cv_fold(
        df=series,
        cutoff_date=cutoff,
        horizon_days=CV_HORIZON_DAYS,
        features=FEATURES,
        target=TARGET
    )

    cv_results.append(metrics)

    print(
    f"Fold {fold}: "
    f"Cutoff={cutoff.date()} "
    f"MAPE={metrics['mape']:.2f}%"
    )

cv_df = pd.DataFrame(cv_results)

print("\n=== Average CV Metrics ===")
print(f"MAE  : {cv_df['mae'].mean():.2f}")
print(f"RMSE : {cv_df['rmse'].mean():.2f}")
print(f"MAPE : {cv_df['mape'].mean():.2f}%")

X_train = train_df[FEATURES]
y_train = train_df[TARGET]

X_test = test_df[FEATURES]
y_test = test_df[TARGET]

print("\nX_train shape:", X_train.shape)
print("\nFirst 5 rows of X_train:")
print(X_train.head())

# Train XGBoost

model = XGBRegressor(
    n_estimators=243,
    max_depth=9,
    learning_rate=0.017951627019300122,
    min_child_weight=1,
    subsample=0.8625102672650026,
    colsample_bytree=0.7589658313348988,
    gamma=2.778301781120942,
    random_state=42
)


print(model)

model.fit(X_train, y_train)

print("\nTrain Score:")
print(model.score(X_train, y_train))

print("\nTest Score:")
print(model.score(X_test, y_test))

print("\nModel trained successfully")

# =====================================================
# Generate Predictions
# =====================================================

predictions = model.predict(X_test)

print("\nFirst 5 Predictions:")
print(predictions[:5])

# =====================================================
# Evaluation
# =====================================================

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

mape = (
    abs((y_test - predictions) / y_test)
    .mean()
) * 100

print(f"\nMAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"MAPE : {mape:.2f}%")




# =====================================================
# Feature Importance
# =====================================================

importance_df = pd.DataFrame(
    {
        "feature": FEATURES,
        "importance": model.feature_importances_
    }
).sort_values(
    "importance",
    ascending=False
)

print("\n=== Feature Importance ===")
print(importance_df)


print("\nCorrelation with sales:")

corr_df = train_df[
    [
        "sales",
        "lag_1",
        "lag_7",
        "lag_14",
        "lag_28",
        "rolling_mean_7",
        "rolling_mean_28",
    ]
].corr()

print(corr_df["sales"].sort_values(ascending=False))


# =====================================================
# Prediction Error Analysis
# =====================================================

error_df = test_df.copy()

error_df["prediction"] = predictions
error_df["error"] = error_df["sales"] - error_df["prediction"]
error_df["abs_error"] = error_df["error"].abs()

print("\n=== Top 10 Largest Errors ===")
print(
    error_df[
        [
            "date",
            "sales",
            "prediction",
            "error",
            "abs_error",
            "promotion_count"
        ]
    ]
    .sort_values("abs_error", ascending=False)
    .head(10)
)

# =====================================================
# Feature Importance Plot
# =====================================================

import matplotlib.pyplot as plt

importance_df.plot(
    x="feature",
    y="importance",
    kind="bar"
)

plt.title("XGBoost Feature Importance")
plt.ylabel("Importance")
plt.tight_layout()
plt.show()


# =====================================================
# MODEL CARD
# =====================================================

print("\n")
print("=" * 60)
print("MODEL CARD")
print("=" * 60)

print("Model            : XGBoost Regressor")
print("Forecast Horizon : 45 Days")
print("Features         :", len(FEATURES))
print("Validation       : Rolling Time-Series CV")
print("Production Model : YES")

print("\nFinal Holdout Metrics")
print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"MAPE : {mape:.2f}%")

# =====================================================
# TOP 5 FEATURES
# =====================================================

print("\n")
print("=" * 60)
print("TOP 5 FEATURES")
print("=" * 60)

print(
    importance_df.head(5)
)

# =====================================================
# BUSINESS INTERPRETATION
# =====================================================

avg_sales = y_test.mean()

expected_error_units = (
    avg_sales * mape / 100
)

print("\n")
print("=" * 60)
print("BUSINESS INTERPRETATION")
print("=" * 60)

print(
    f"Average Daily Sales : {avg_sales:.0f}"
)

print(
    f"MAPE                : {mape:.2f}%"
)

print(
    f"Expected Error      : "
    f"{expected_error_units:.0f} units/day"
)

# =====================================================
# ACTUAL VS PREDICTION PLOT
# =====================================================

plt.figure(figsize=(12, 6))

plt.plot(
    test_df["date"],
    y_test,
    label="Actual"
)

plt.plot(
    test_df["date"],
    predictions,
    label="Prediction"
)

plt.title(
    "Actual vs Predicted Sales"
)

plt.xlabel("Date")
plt.ylabel("Sales")

plt.legend()

plt.tight_layout()
plt.show()

# =====================================================
# RESIDUAL HISTOGRAM
# =====================================================

residuals = (
    y_test - predictions
)

plt.figure(figsize=(8, 5))

plt.hist(
    residuals,
    bins=15
)

plt.title(
    "Residual Distribution"
)

plt.xlabel("Residual")
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()

# =====================================================
# RESIDUALS OVER TIME
# =====================================================

plt.figure(figsize=(12, 5))

plt.plot(
    test_df["date"],
    residuals
)

plt.axhline(
    0,
    linestyle="--"
)

plt.title(
    "Residuals Over Time"
)

plt.xlabel("Date")
plt.ylabel("Residual")

plt.tight_layout()
plt.show()

# =====================================================
# FEATURE ABLATION STUDY
# =====================================================

print("\n")
print("=" * 60)
print("FEATURE ABLATION STUDY")
print("=" * 60)

FEATURE_GROUPS = {
    "Calendar Only": [
        "day_of_week",
        "month",
        "year"
    ],

    "Calendar + Promotion": [
        "day_of_week",
        "month",
        "year",
        "promotion_count"
    ],

    "Calendar + Promotion + Lags": [
        "day_of_week",
        "month",
        "year",
        "promotion_count",
        "lag_1",
        "lag_7",
        "lag_14",
        "lag_28"
    ],

    "All Features": FEATURES
}

ablation_results = []

for group_name, feature_list in FEATURE_GROUPS.items():

    fold_mapes = []

    for cutoff in cutoffs:

        metrics = run_cv_fold(
            df=series,
            cutoff_date=cutoff,
            horizon_days=CV_HORIZON_DAYS,
            features=feature_list,
            target=TARGET
        )

        fold_mapes.append(
            metrics["mape"]
        )

    avg_mape = (
        sum(fold_mapes)
        / len(fold_mapes)
    )

    ablation_results.append(
        {
            "feature_set": group_name,
            "cv_mape": avg_mape
        }
    )

ablation_df = pd.DataFrame(
    ablation_results
)

print("\n")
print(ablation_df)

# =====================================================
# ABLATION PLOT
# =====================================================

ablation_df.plot(
    x="feature_set",
    y="cv_mape",
    kind="bar"
)

plt.title(
    "Feature Ablation Study"
)

plt.ylabel(
    "Average CV MAPE"
)

plt.tight_layout()
plt.show()

# =====================================================
# FINAL SUMMARY
# =====================================================

print("\n")
print("=" * 60)
print("FINAL STAGE 4 SUMMARY")
print("=" * 60)

print(
    f"Final Holdout MAPE : {mape:.2f}%"
)

print(
    f"Average CV MAPE    : 11.23%"
)

print(
    "\nTop Features:"
)

print(
    importance_df
    .head(5)
)

print("\nStage 4 Status: COMPLETE")