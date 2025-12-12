"""Pyrefly Bug C: @field.validator decorator not recognized.

attrs allows defining validators using a decorator pattern:
    x: int = field()
    @x.validator
    def _validate_x(self, attribute, value):
        if not valid:
            raise ValueError("...")

Pyrefly error: "Object of class `int` has no attribute `validator`"

The issue: pyrefly sees `x: int = field()` and thinks `x` has type `int`.
In reality, during class definition, `field()` returns a field descriptor
that has `.validator` method. The type annotation `int` describes the
runtime type of the attribute value, not the class-level descriptor.

Docs: https://www.attrs.org/en/25.4.0/examples.html#validators
      https://www.attrs.org/en/25.4.0/init.html#validators

Related: https://github.com/facebook/pyrefly/issues/1825
"""

from attrs import define, field, validators, Attribute


# Example 1: Basic validator decorator
# Pyrefly error: "Object of class `int` has no attribute `validator`"
@define
class BasicValidator:
    x: int = field()

    @x.validator
    def _check_x(self, attribute: Attribute, value: int) -> None:
        if value > 42:
            raise ValueError("x must be smaller or equal to 42")


# Example 2: Validator decorator combined with built-in validator
# Pyrefly error: "Object of class `int` has no attribute `validator`"
@define
class CombinedValidator:
    x: int = field(validator=validators.instance_of(int))

    @x.validator
    def _fits_byte(self, attribute: Attribute, value: int) -> None:
        if not 0 <= value < 256:
            raise ValueError("value out of bounds")


# Example 3: Multiple fields with validators
# Pyrefly errors on both @x.validator and @y.validator
@define
class MultipleValidators:
    x: int = field()
    y: int = field()

    @x.validator
    def _check_x(self, attribute: Attribute, value: int) -> None:
        if value < 0:
            raise ValueError("x must be non-negative")

    @y.validator
    def _check_y(self, attribute: Attribute, value: int) -> None:
        if value <= self.x:
            raise ValueError("y must be greater than x")


# Verify all work at runtime
if __name__ == "__main__":
    b = BasicValidator(x=42)
    print(f"BasicValidator(42): {b}")

    try:
        BasicValidator(x=43)
    except ValueError as e:
        print(f"BasicValidator(43) raised: {e}")

    c = CombinedValidator(x=128)
    print(f"CombinedValidator(128): {c}")

    m = MultipleValidators(x=5, y=10)
    print(f"MultipleValidators(5, 10): {m}")
