"""Package-wide configuration."""

import logging

import ray


def init_ray() -> None:
    """Initialize Ray cluster."""
    ray.init(include_dashboard=False, logging_level=logging.INFO, ignore_reinit_error=True)
