"""Another Pyrefly issue #1825 variant: Factory default torch.device after other defaults.

Layout (valid in attrs):
- name (default)
- hidden_size (Factory default)
- device (Factory default torch.device("cpu"))
- learning_rate (Factory default)

Expected: attrs allows this layout.
Actual: pyrefly still flags device as lacking a default.
"""

import torch
from attrs import define, field, Factory


@define
class ModelConfig:
    """Configuration for a model with device settings."""

    name: str = field(default=Factory(lambda: "default_model"))
    """Name of the model."""

    hidden_size: int = field(default=Factory(lambda: 768))
    """Hidden size of the model."""

    device: torch.device = field(default=Factory(lambda: torch.device("cpu")))
    """Device to run the model on."""

    learning_rate: float = field(default=Factory(lambda: 0.001))
    """Learning rate for the model."""