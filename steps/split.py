"""Functions to split data into train, test and validation datasets."""

import logging

import pandas as pd
import ray

logger = logging.getLogger(__name__)


def split_data(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """
    Split data into train, validation and test datasets.

    Does not work with recipes, as they must a return a single pandas series

    Args:
    ----
        df (pd.DataFrame): Raw DataFrame

    """
    train_data, remaining_data = ray.data.from_pandas(df).train_test_split(test_size=0.2, seed=1337)
    validation_data, test_data = remaining_data.train_test_split(test_size=0.5, seed=1337)

    return {
        "train": train_data.to_pandas(),
        "valid": validation_data.to_pandas(),
        "test": test_data.to_pandas(),
    }  # pyright: ignore[reportReturnType]


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean data by removing missing values and outliers.

    Args:
    ----
        df (pd.DataFrame): Raw DataFrame

    Returns:
    -------
        pd.DataFrame: Cleaned DataFrame

    """
    logger.info("Cleaning data")
    return (
        ray.data.from_pandas(df)
        .map_batches(lambda df: df.dropna(), batch_format="pandas")
        .map_batches(lambda df: df[df["fare_amount"] > 0], batch_format="pandas")
        .map_batches(lambda df: df[df["trip_distance"] > 0], batch_format="pandas")
        .map_batches(lambda df: df[df["trip_distance"] < 1000], batch_format="pandas")
    ).to_pandas()


def filter_data(df: pd.DataFrame) -> pd.Series:
    """
    Filter data based on a condition.

    Args:
    ----
        df (pd.DataFrame): Raw DataFrame

    Returns:
    -------
        pd.Series: Filtered data

    """
    return (df["fare_amount"] > 0) & (df["trip_distance"] > 0)
