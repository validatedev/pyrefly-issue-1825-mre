"""Control case: all attrs fields provide defaults, so Pyrefly should be happy."""

from attrs import define, field, Factory

@define
class ModelConfig:
    """Configuration for a model with device settings."""

    device: str = field(default=Factory(lambda: "cpu"))
    """Device to run the model on."""

    name: str = field(default=Factory(lambda: "default_model"))
    """Name of the model."""

    hidden_size: int = 768
    """Hidden size of the model."""

    learning_rate: float = 0.001
    """Learning rate for the model."""