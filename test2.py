"""Pyrefly issue #1825 variant: attrs class with a Factory default before a required field.

Layout (valid in attrs):
- device (Factory default "cpu")
- name (required)
- hidden_size (default)
- learning_rate (default)

Expected: attrs accepts this layout.
Actual: pyrefly reports name as "dataclass field without a default may not follow
dataclass field with a default."
"""

from attrs import define, field, Factory

@define
class ModelConfig:
    """Configuration for a model with device settings."""

    device: str = field(default=Factory(lambda: "cpu"))
    """Device to run the model on."""

    name: str
    """Name of the model."""

    hidden_size: int = 768
    """Hidden size of the model."""

    learning_rate: float = 0.001
    """Learning rate for the model."""
