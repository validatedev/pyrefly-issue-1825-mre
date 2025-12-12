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


# Verify it works at runtime
if __name__ == "__main__":
    m = ModelConfig()
    print(f"ModelConfig: {m}")
