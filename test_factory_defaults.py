"""Pyrefly Bug A: Factory() and factory= defaults not recognized.

attrs allows Factory() for mutable default values. Pyrefly incorrectly reports
"Dataclass field without a default may not follow dataclass field with a default"
even when Factory() provides a valid default.

Key issue: Pyrefly doesn't recognize Factory() as providing a default value.
- Factory() is a valid default mechanism for mutable types
- field(factory=list) is syntactic sugar for field(default=Factory(list))
- attrs enforces the same ordering as dataclasses (mandatory before defaults)
  UNLESS using kw_only=True

Docs: https://www.attrs.org/en/stable/api.html#attrs.Factory
      https://www.attrs.org/en/stable/examples.html#defaults

Related: https://github.com/facebook/pyrefly/issues/1825
"""

import torch
from attrs import define, field, Factory


# Example 1: Factory default - pyrefly doesn't recognize it as a default
# Pyrefly error: "Dataclass field `device` without a default may not follow..."
# This is false positive - Factory() IS a valid default
@define
class ModelConfig:
    """Configuration for a model with device settings."""

    name: str
    hidden_size: int = 768
    device: torch.device = field(default=Factory(lambda: torch.device("cpu")))
    learning_rate: float = 0.001


# Example 2: Required kw_only field after Factory default
# attrs allows kw_only required fields after defaults (see docs link above)
# This is VALID attrs code but pyrefly may not recognize Factory as a default
# see https://www.attrs.org/en/25.4.0/examples.html#keyword-only-attributes
@define
class ModelConfigReordered:
    """attrs allows required kw_only fields after defaults."""

    device: str = field(default=Factory(lambda: "cpu"))
    name: str = field(kw_only=True)  # Required kw_only field after default - VALID in attrs!
    hidden_size: int = 768
    learning_rate: float = 0.001


# Example 3: All fields use Factory (still fails in pyrefly)
# Pyrefly error: "Dataclass field `device` without a default may not follow..."
@define
class AllFactoryDefaults:
    """All fields use Factory defaults."""

    device: torch.device = field(default=Factory(lambda: torch.device("cpu")))
    name: str = field(default=Factory(lambda: "default_model"))
    hidden_size: int = field(default=Factory(lambda: 768))
    learning_rate: float = field(default=Factory(lambda: 0.001))


# Example 4: Using factory= shorthand (same issue)
@define
class FactoryShorthand:
    """Using factory= argument instead of default=Factory()."""

    items: list = field(factory=list)
    mapping: dict = field(factory=dict)
    name: str = "default"


# Verify all work at runtime
if __name__ == "__main__":
    m1 = ModelConfig(name="test")
    print(f"ModelConfig: {m1}")

    m2 = ModelConfigReordered(name="test")
    print(f"ModelConfigReordered: {m2}")

    m3 = AllFactoryDefaults()
    print(f"AllFactoryDefaults: {m3}")

    m4 = FactoryShorthand()
    print(f"FactoryShorthand: {m4}")
