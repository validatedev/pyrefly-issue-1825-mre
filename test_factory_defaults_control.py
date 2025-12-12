"""Control case: All fields have defaults in "correct" order.

This should pass pyrefly checks since it follows dataclass-like ordering rules.
Note: attrs DOES enforce the same rule as dataclasses: mandatory attributes
cannot follow attributes with defaults (unless using kw_only=True).

Related: https://github.com/facebook/pyrefly/issues/1825
"""

from attrs import define, field, Factory


@define
class ModelConfig:
    """Configuration where all fields have defaults in standard order."""

    # All required fields first (none in this case)
    # Then all defaulted fields
    device: str = field(default=Factory(lambda: "cpu"))
    name: str = field(default=Factory(lambda: "default_model"))
    hidden_size: int = 768
    learning_rate: float = 0.001


@define
class ModelConfig2:
    """Configuration where all fields have defaults in standard order."""

    # All required fields first (none in this case)
    # Then all defaulted fields
    device: str = field(default=Factory(lambda: "cpu"))
    hidden_size: int = 768
    name: str = field(default=Factory(lambda: "default_model"))
    learning_rate: float = 0.001


@define
class ModelConfig3:
    """Configuration where all fields have defaults in standard order."""

    # All required fields first (none in this case)
    # Then all defaulted fields
    hidden_size: int = 768
    device: str = field(default=Factory(lambda: "cpu"))
    name: str = field(default=Factory(lambda: "default_model"))
    learning_rate: float = 0.001

@define
class ModelConfig4:
    """Configuration where all fields have defaults in standard order."""
    # All required fields first (none in this case)
    # Then all defaulted fields
    hidden_size: int
    learning_rate: float = 0.001
    device: str = field(default=Factory(lambda: "cpu"))
    name: str = field(default=Factory(lambda: "default_model"))

@define
class ModelConfig5:
    """Configuration where all fields have defaults in standard order."""
    # All required fields first (none in this case)
    # Then all defaulted fields
    name: str
    hidden_size: int = 768
    device: str = field(default=Factory(lambda: "cpu")) 
    learning_rate: float = 0.001


# Verify it works at runtime
if __name__ == "__main__":
    m = ModelConfig()
    print(f"ModelConfig: {m}")
    m2 = ModelConfig2()
    print(f"ModelConfig2: {m2}")
    m3 = ModelConfig3()
    print(f"ModelConfig3: {m3}")
    m4 = ModelConfig4(hidden_size=512)
    print(f"ModelConfig4: {m4}")
    m5 = ModelConfig5(name="test_model")
    print(f"ModelConfig5: {m5}")
