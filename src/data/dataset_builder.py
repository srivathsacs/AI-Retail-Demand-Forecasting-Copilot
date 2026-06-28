"""
Module: dataset_builder.py

Purpose:
    Build the category-level sales dataset used by the forecasting pipeline.

Why this file exists:
    The raw retail dataset stores sales at the individual item level.
    Forecasting is performed at the product category level, so this
    module aggregates item-level transactions into a daily dataset
    grouped by store and category.

Project Stage:
    Stage 1 - Dataset Construction
"""

from pathlib import Path

import duckdb


class DatasetBuilder:
    """
    Build the processed dataset used by downstream forecasting models.
    """

    def build_category_dataset(
        self,
        train_path: str,
        items_path: str,
        output_path: str,
    ) -> None:
        """
        Create a category-level daily sales dataset.

        Parameters
        ----------
        train_path : str
            Path to the raw transaction dataset.

        items_path : str
            Path to the item metadata dataset.

        output_path : str
            Location where the processed dataset will be saved.

        Raises
        ------
        FileNotFoundError
            If one or more input files do not exist.
        """

        train_file = Path(train_path)
        items_file = Path(items_path)
        output_file = Path(output_path)

        if not train_file.exists():
            raise FileNotFoundError(
                f"Training dataset not found: {train_file}"
            )

        if not items_file.exists():
            raise FileNotFoundError(
                f"Items dataset not found: {items_file}"
            )

        # Create the output directory if it does not already exist.
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # DuckDB performs the join and aggregation directly on the CSV
        # files, which is faster than loading everything into pandas.
        duckdb.sql(
            f"""
            COPY (
                SELECT
                    t.date,
                    t.store_nbr AS store_id,
                    i.family AS category,
                    SUM(t.unit_sales) AS sales,
                    SUM(
                        CASE
                            WHEN t.onpromotion = TRUE THEN 1
                            ELSE 0
                        END
                    ) AS promotion_count
                FROM '{train_file.as_posix()}' t
                JOIN '{items_file.as_posix()}' i
                    ON t.item_nbr = i.item_nbr
                GROUP BY
                    t.date,
                    t.store_nbr,
                    i.family
            )
            TO '{output_file.as_posix()}'
            WITH (
                HEADER,
                DELIMITER ','
            );
            """
        )