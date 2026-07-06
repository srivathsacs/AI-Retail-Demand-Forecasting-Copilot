import pandas as pd
import optuna

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

N_TRIALS = 30


# =====================================================
# METRICS
# =====================================================

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


# =====================================================
# DATA
# =====================================================

df = pd.read_csv(
    "data/processed/sales_by_category.csv"
)

series = df[
    (df["store_id"] == 44) &
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

series = series.sort_values("date")

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

cutoffs = create_cv_cutoffs(
    dates=series["date"],
    initial_days=CV_INITIAL_DAYS,
    horizon_days=CV_HORIZON_DAYS,
    step_days=CV_STEP_DAYS
)

print(f"\nCV Folds: {len(cutoffs)}")


# =====================================================
# OPTUNA OBJECTIVE
# =====================================================

def objective(trial):

    params = {

        "n_estimators": trial.suggest_int(
            "n_estimators",
            100,
            500
        ),

        "max_depth": trial.suggest_int(
            "max_depth",
            3,
            10
        ),

        "learning_rate": trial.suggest_float(
            "learning_rate",
            0.01,
            0.30,
            log=True
        ),

        "min_child_weight": trial.suggest_int(
            "min_child_weight",
            1,
            10
        ),

        "subsample": trial.suggest_float(
            "subsample",
            0.6,
            1.0
        ),

        "colsample_bytree": trial.suggest_float(
            "colsample_bytree",
            0.6,
            1.0
        ),

        "gamma": trial.suggest_float(
            "gamma",
            0.0,
            5.0
        ),

        "random_state": 42,
    }

    fold_mapes = []

    for cutoff in cutoffs:

        train_df = series[
            series["date"] <= cutoff
        ].copy()

        test_end = (
            cutoff +
            pd.Timedelta(
                days=CV_HORIZON_DAYS
            )
        )

        test_df = series[
            (series["date"] > cutoff) &
            (series["date"] <= test_end)
        ].copy()

        X_train = train_df[FEATURES]
        y_train = train_df[TARGET]

        X_test = test_df[FEATURES]
        y_test = test_df[TARGET]

        model = XGBRegressor(
            **params
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

        fold_mapes.append(
            metrics["mape"]
        )

    return sum(fold_mapes) / len(
        fold_mapes
    )


# =====================================================
# RUN OPTUNA
# =====================================================

study = optuna.create_study(
    direction="minimize"
)

study.optimize(
    objective,
    n_trials=N_TRIALS
)


# =====================================================
# RESULTS
# =====================================================

print("\n=== BEST CV MAPE ===")
print(
    f"{study.best_value:.2f}%"
)

print("\n=== BEST PARAMETERS ===")
print(
    study.best_params
)

print("\n=== TOP 5 TRIALS ===")

trials_df = (
    study.trials_dataframe()
    .sort_values("value")
)

print(
    trials_df[
        [
            "number",
            "value"
        ]
    ]
    .head(5)
)