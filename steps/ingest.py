"""Functions to ingest data."""

import logging
from typing import Optional

import pandas as pd
import ray

logger = logging.getLogger(__name__)


def load_data(file_path: str, cols_to_load: Optional[list[str]]) -> pd.DataFrame:
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
    return ray.data.read_parquet(paths=file_path, columns=None).to_pandas()
