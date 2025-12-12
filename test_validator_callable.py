"""Control case: Callable validators (may work in pyrefly).

attrs supports validators as callable functions passed to field().
This pattern doesn't use the decorator syntax that triggers Bug C.

Docs: https://www.attrs.org/en/stable/examples.html#validators
      https://www.attrs.org/en/stable/api.html#validators

Related: https://github.com/facebook/pyrefly/issues/1825
"""

from attrs import define, field, validators


# Custom validator function
def x_smaller_than_y(instance, attribute, value):
    """Validator that checks x is smaller than y."""
    if value >= instance.y:
        raise ValueError("'x' has to be smaller than 'y'!")


# Example 1: Custom callable validator with built-in validator
@define
class CallableValidator:
    x: int = field(validator=[validators.instance_of(int), x_smaller_than_y])
    y: int


# Example 2: Multiple built-in validators as list
@define
class MultipleBuiltinValidators:
    value: int = field(
        validator=[
            validators.instance_of(int),
            validators.ge(0),
            validators.lt(100),
        ]
    )


# Verify all work at runtime
if __name__ == "__main__":
    c = CallableValidator(x=3, y=4)
    print(f"CallableValidator(3, 4): {c}")

    try:
        CallableValidator(x=4, y=3)
    except ValueError as e:
        print(f"CallableValidator(4, 3) raised: {e}")

    m = MultipleBuiltinValidators(value=50)
    print(f"MultipleBuiltinValidators(50): {m}")
