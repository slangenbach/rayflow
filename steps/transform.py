"""Functions to process and transform data."""

import logging
from typing import Self

import pandas as pd
import ray
from pandas import DataFrame
from ray.data.preprocessors import OneHotEncoder, StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from rayflow.config import init_ray

logger = logging.getLogger(__name__)
init_ray()


class RayEncoder(BaseEstimator, TransformerMixin):
    """Sklearn-compatible one-hot encoder for Ray."""

    def __init__(self, columns: list[str]) -> None:  # noqa: D107
        super().__init__()
        self.columns = columns
        self.encoder = OneHotEncoder(columns=self.columns)

    def fit(self, X: pd.DataFrame, y=None) -> Self:  # noqa: D102
        data = ray.data.from_pandas(X)
        self.encoder.fit(data)

        return self

    def transform(self, X: pd.DataFrame) -> DataFrame:  # noqa: D102
        data = ray.data.from_pandas(X)
        transformed_data = self.encoder.transform(data)

        return transformed_data.to_pandas()


class RayScaler(BaseEstimator, TransformerMixin):
    """Sklearn-compatible scaler for Ray."""

    def __init__(self, columns: list[str]) -> None:  # noqa: D107
        super().__init__()
        self.columns = columns
        self.scaler = StandardScaler(columns=self.columns)

    def fit(self, X: pd.DataFrame, y=None) -> Self:  # noqa: D102
        data = ray.data.from_pandas(X)
        self.scaler.fit(data)

        return self

    def transform(self, X: pd.DataFrame) -> DataFrame:  # noqa: D102
        data = ray.data.from_pandas(X)
        transformed_data = self.scaler.transform(data)

        return transformed_data.to_pandas()


def transform_data() -> Pipeline:
    """Create a pipeline to transform data."""
    return Pipeline(
        steps=[
            (
                "encoder",
                ColumnTransformer(
                    transformers=[
                        ("payment_encoder", RayEncoder(columns=["payment_type"]), ["payment_type"]),
                        ("ratecode_encoder", RayEncoder(columns=["RatecodeID"]), ["RatecodeID"]),
                        (
                            "trip_distance_scaler",
                            RayScaler(columns=["trip_distance"]),
                            ["trip_distance"],
                        ),
                    ],
                    remainder="passthrough",
                ),
            ),
        ]
    )
