"""Functions to process and transform data."""

import logging

import pandas as pd
import ray
from ray.data.preprocessors import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

logger = logging.getLogger(__name__)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    return (
        ray.data.from_pandas(df)
        .map_batches(lambda df: df.dropna(), batch_format="pandas")
        .map_batches(lambda df: df[df["trip_distance"] < 1000], batch_format="pandas")
        # TODO: Move to split step as fare_amount is the target column and not included in the step
        # .map_batches(lambda df: df[df["fare_amount"] > 0], batch_format="pandas")
    ).to_pandas()


def one_hot_encode_data(column_name: str) -> pd.DataFrame:
    return OneHotEncoder([column_name])


def transform_data():
    return (
        Pipeline(
            steps=[
                ("clean_data", FunctionTransformer(clean_data, feature_names_out="one-to-one")),
                (
                    "encode_payments",
                    FunctionTransformer(
                        one_hot_encode_data, kw_args={"column_name": "payment_type"}
                    ),
                    (
                        "encode_rate_code",
                        FunctionTransformer(
                            one_hot_encode_data, kw_args={"column_name": "RatecodeID"}
                        ),
                    ),
                ),
            ]
        ),
    )
