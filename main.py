"""Minimum reproducible example for pyrefly issue #1825.

This demonstrates the attrs incompatibility when using Field with lambda defaults.
Pyrefly incorrectly treats attrs classes as dataclasses and throws:
"Dataclass field without a default may not follow dataclass field with a default"
"""

import torch
from attrs import define, field, Factory


@define
class ModelConfig:
    """Configuration for a model with device settings."""

    name: str
    """Name of the model."""

    hidden_size: int = 768
    """Hidden size of the model."""

    device: torch.device = field(default=Factory(lambda: torch.device("cpu")))
    """Device to run the model on."""

    learning_rate: float = 0.001
    """Learning rate for the model."""
