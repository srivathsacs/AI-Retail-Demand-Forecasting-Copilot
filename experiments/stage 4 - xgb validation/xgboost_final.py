import pandas as pd

from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error


# =====================================================
# CONFIG
# =====================================================

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

CV_INITIAL_DAYS = 1095
CV_HORIZON_DAYS = 45
CV_STEP_DAYS = 90


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


# =====================================================
# METRICS
# =====================================================

def evaluate_forecast(y_true, y_pred):

    mae = mean_absolute_error(
        y_true,
        y_pred
    )

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


# =====================================================
# CV HELPERS
# =====================================================

def create_cv_cutoffs(
    dates,
    initial_days,
    horizon_days,
    step_days
):
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


def run_cv_fold(
    df,
    cutoff_date,
    horizon_days
):

    train_df = df[
        df["date"] <= cutoff_date
    ].copy()

    test_end = (
        cutoff_date
        + pd.Timedelta(days=horizon_days)
    )

    test_df = df[
        (df["date"] > cutoff_date)
        &
        (df["date"] <= test_end)
    ].copy()

    X_train = train_df[FEATURES]
    y_train = train_df[TARGET]

    X_test = test_df[FEATURES]
    y_test = test_df[TARGET]

    model = XGBRegressor(
        **BEST_PARAMS
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    return evaluate_forecast(
        y_test,
        predictions
    )


# =====================================================
# LOAD DATA
# =====================================================

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


# =====================================================
# TIME SERIES CROSS VALIDATION
# =====================================================

cutoffs = create_cv_cutoffs(
    dates=series["date"],
    initial_days=CV_INITIAL_DAYS,
    horizon_days=CV_HORIZON_DAYS,
    step_days=CV_STEP_DAYS
)

cv_results = []

print("\n=== XGBOOST CV ===")

for fold, cutoff in enumerate(
    cutoffs,
    start=1
):

    metrics = run_cv_fold(
        df=series,
        cutoff_date=cutoff,
        horizon_days=CV_HORIZON_DAYS
    )

    cv_results.append(metrics)

    print(
        f"Fold {fold}: "
        f"MAPE={metrics['mape']:.2f}%"
    )

cv_df = pd.DataFrame(
    cv_results
)

print("\n=== AVERAGE CV METRICS ===")
print(
    f"MAE  : {cv_df['mae'].mean():.2f}"
)
print(
    f"RMSE : {cv_df['rmse'].mean():.2f}"
)
print(
    f"MAPE : {cv_df['mape'].mean():.2f}%"
)


# =====================================================
# FINAL HOLDOUT TEST
# =====================================================

split_date = "2017-07-01"

train_df = series[
    series["date"] < split_date
]

test_df = series[
    series["date"] >= split_date
]

X_train = train_df[FEATURES]
y_train = train_df[TARGET]

X_test = test_df[FEATURES]
y_test = test_df[TARGET]

model = XGBRegressor(
    **BEST_PARAMS
)

model.fit(
    X_train,
    y_train
)

predictions = model.predict(
    X_test
)

metrics = evaluate_forecast(
    y_test,
    predictions
)

print("\n=== FINAL HOLDOUT TEST ===")
print(
    f"MAE  : {metrics['mae']:.2f}"
)
print(
    f"RMSE : {metrics['rmse']:.2f}"
)
print(
    f"MAPE : {metrics['mape']:.2f}%"
)


prediction_df = pd.DataFrame({
    "date": test_df["date"].values,
    "actual": y_test.values,
    "xgb_prediction": predictions
})

prediction_df.to_csv(
    "data/xgb_holdout_predictions.csv",
    index=False
)