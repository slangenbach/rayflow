"""Functions to ingest data."""

import logging
from typing import Optional

import pandas as pd
import ray

from rayflow.config import init_ray
from rayflow.constants import COLS_TO_LOAD

logger = logging.getLogger(__name__)

init_ray()


def load_data(file_path: str, cols_to_load: Optional[list[str]] = None) -> pd.DataFrame:
    """
    Load data from a file or directory.

    Args:
    ----
        file_path (str): File or directory path.
        cols_to_load (Optional[list[str]], optional): Columns to load. Defaults to None.

    Returns:
    -------
        pd.DataFrame: Raw DataFrame

    """
    logger.info("Loading data from: %s (using Ray)", file_path)

    return (
        # This is ugly, yet it is unclear how to pass an argument to a function using MLflow Recipes
        ray.data.read_parquet(paths=file_path, columns=COLS_TO_LOAD)
        .map_batches(lambda df: df.dropna(), batch_format="pandas")
        .map_batches(lambda df: df[df["trip_distance"] > 0], batch_format="pandas")
        .map_batches(lambda df: df[df["trip_distance"] < 1000], batch_format="pandas")
        .map_batches(lambda df: df[df["fare_amount"] > 0], batch_format="pandas")
        .to_pandas()
    )
