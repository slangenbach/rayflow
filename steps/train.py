"""Functions to train a model."""

from typing import Optional, Self

import pandas as pd
import ray
from ray.train import ScalingConfig
from ray.train.lightgbm.lightgbm_trainer import LightGBMTrainer
from sklearn.base import BaseEstimator, RegressorMixin

from rayflow.config import init_ray

init_ray()


class RayTrainer(BaseEstimator, RegressorMixin):
    """Sklearn-learn compatible LightGBM trainer for Ray."""

    def __init__(self) -> None:  # noqa: D107
        self.params = {"objective": "binary", "metric": ["binary_logloss"]}
        self.scaling_config = ScalingConfig(num_workers=4)
        self.trainer: None
        self.checkpoint = None

    def fit(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> Self:  # noqa: D102
        if y is not None:
            X = X.copy()
            X["fare_amount"] = y

        data = ray.data.from_pandas(X)

        self.trainer = LightGBMTrainer(
            datasets={"train": data},
            scaling_config=self.scaling_config,
            label_column="fare_amount",
            params=self.params,
        )

        result = self.trainer.fit()
        self.checkpoint = result.checkpoint

        return self

    def predict(self, X: pd.DataFrame) -> pd.Series:  # noqa: D102
        # data = ray.data.from_pandas(X)
        model = self.trainer.get_model(checkpoint=self.checkpoint)
        predictions = model.predict(X)

        return pd.Series(predictions)


def train_model() -> RayTrainer:
    """Train a model."""
    return RayTrainer()
