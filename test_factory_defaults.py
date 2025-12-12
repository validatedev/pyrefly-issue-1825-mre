"""Pyrefly Bug A: `torch.device` + `default=Factory(...)` not recognized as a default.

In this repository, pyrefly reports a dataclass-style ordering error when a field
uses `default=Factory(...)` and the factory callable produces a `torch.device`.
This then cascades into missing-argument errors at call sites.

Notes:
- `Factory()` is a valid attrs default mechanism.
- attrs enforces the same ordering rule as dataclasses (mandatory before defaults),
  unless using `kw_only=True`.
- In this repo, `field(factory=list)` / `field(factory=dict)` works and does not
  trigger Bug A; the failing cases are specifically the ones returning `torch.device`.
- This MRE only tests torch; the underlying issue may be specific to `torch.device`
  (or more generally to factories that return opaque / third-party types).

Docs: https://www.attrs.org/en/stable/api.html#attrs.Factory
      https://www.attrs.org/en/stable/examples.html#defaults

Related: https://github.com/facebook/pyrefly/issues/1825
"""

import torch
from attrs import define, field, Factory


# Example 1: torch.device Factory default - pyrefly doesn't recognize it as a default
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
# This is VALID attrs code; it is included to show that ordering rules can be relaxed
# for required keyword-only attributes.
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
# This is false positive - Factory() IS a valid default
@define
class AllFactoryDefaults:
    """All fields use Factory defaults."""

    device: torch.device = field(default=Factory(lambda: torch.device("cpu")))
    name: str = field(default=Factory(lambda: "default_model"))
    hidden_size: int = field(default=Factory(lambda: 768))
    learning_rate: float = field(default=Factory(lambda: 0.001))


# Example 4: Using factory= shorthand (works fine)
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
