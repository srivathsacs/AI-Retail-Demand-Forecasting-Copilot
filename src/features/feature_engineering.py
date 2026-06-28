import pandas as pd


def create_calendar_features(
    df: pd.DataFrame,
) -> pd.DataFrame:

    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])

    df["day_of_week"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year

    return df


def create_lag_features(
    df: pd.DataFrame,
) -> pd.DataFrame:

    df = df.copy()

    df["lag_1"] = df["sales"].shift(1)
    df["lag_7"] = df["sales"].shift(7)
    df["lag_14"] = df["sales"].shift(14)
    df["lag_28"] = df["sales"].shift(28)

    df["rolling_mean_7"] = (
        df["sales"]
        .shift(1)
        .rolling(7)
        .mean()
    )

    df["rolling_mean_28"] = (
        df["sales"]
        .shift(1)
        .rolling(28)
        .mean()
    )

    return df