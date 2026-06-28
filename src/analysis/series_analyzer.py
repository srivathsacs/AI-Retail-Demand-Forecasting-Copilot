import pandas as pd


class SeriesAnalyzer:

    def load_series(
        self,
        dataset_path: str,
        store_id: int,
        category: str,
    ) -> pd.DataFrame:

        df = pd.read_csv(dataset_path)

        series = df[
            (df["store_id"] == store_id)
            & (df["category"] == category)
        ].copy()

        series["date"] = pd.to_datetime(
            series["date"]
        )

        return series.sort_values("date")