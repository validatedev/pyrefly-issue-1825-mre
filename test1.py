"""Pyrefly issue #1825: attrs class with a torch.device Factory default.

Layout (valid in attrs):
- name (required)
- hidden_size (default)
- device (Factory default torch.device("cpu"))
- learning_rate (default)

Expected: attrs accepts this layout.
Actual: pyrefly reports device as "dataclass field without a default may not follow
dataclass field with a default" even though a default is provided.
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
