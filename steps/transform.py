"""Functions to process and transform data."""

import logging

import pandas as pd
import ray

from rayflow.config import COLS_TO_DROP

logger = logging.getLogger(__name__)

# https://docs.ray.io/en/latest/data/api/preprocessor.html#preprocessor-ref
# https://docs.ray.io/en/latest/data/api/doc/ray.data.preprocessors.OneHotEncoder.html#ray.data.preprocessors.OneHotEncoder


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineer features.

    Args:
    ----
        df (pd.DataFrame): Processed DataFrame

    Returns:
    -------
        pd.DataFrame: DataFrame with engineered features

    """
    return df.drop(columns=COLS_TO_DROP)


def transform_data(df):
    return ray.data.from_pandas(df).map(engineer_features).to_pandas()
