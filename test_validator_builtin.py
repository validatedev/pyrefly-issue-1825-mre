"""Control case: Built-in validators from attrs.validators.

attrs ships with many built-in validators. Testing if pyrefly handles them.

Docs: https://www.attrs.org/en/stable/api.html#validators

Related: https://github.com/facebook/pyrefly/issues/1825
"""

from typing import Callable

from attrs import define, field, validators


# Example 1: instance_of validator
@define
class InstanceOfValidator:
    x: int = field(validator=validators.instance_of(int))
    name: str = field(validator=validators.instance_of(str))


# Example 2: Numeric comparison validators
@define
class NumericValidators:
    age: int = field(validator=[validators.instance_of(int), validators.ge(0)])
    score: float = field(validator=[validators.ge(0.0), validators.le(100.0)])
    priority: int = field(validator=[validators.gt(0), validators.lt(10)])


# Example 3: String validators
@define
class StringValidators:
    email: str = field(validator=validators.matches_re(r"^[\w\.-]+@[\w\.-]+\.\w+$"))
    username: str = field(validator=[validators.min_len(3), validators.max_len(20)])


# Example 4: in_ validator for enums/choices
@define
class ChoiceValidator:
    status: str = field(validator=validators.in_(["pending", "active", "completed"]))
    priority: int = field(validator=validators.in_([1, 2, 3, 4, 5]))


# Example 5: optional validator
@define
class OptionalValidator:
    name: str = field(validator=validators.instance_of(str))
    nickname: str | None = field(
        default=None, validator=validators.optional(validators.instance_of(str))
    )


# Example 6: deep_iterable validator
@define
class DeepIterableValidator:
    numbers: list[int] = field(
        factory=list,
        validator=validators.deep_iterable(
            member_validator=validators.instance_of(int),
            iterable_validator=validators.instance_of(list),
        ),
    )


# Example 7: is_callable validator
@define
class CallableFieldValidator:
    callback: Callable = field(validator=validators.is_callable())


# Verify all work at runtime
if __name__ == "__main__":
    i = InstanceOfValidator(x=42, name="test")
    print(f"InstanceOfValidator: {i}")

    n = NumericValidators(age=25, score=85.5, priority=5)
    print(f"NumericValidators: {n}")

    s = StringValidators(email="user@example.com", username="johndoe")
    print(f"StringValidators: {s}")

    c = ChoiceValidator(status="active", priority=3)
    print(f"ChoiceValidator: {c}")

    o = OptionalValidator(name="John", nickname=None)
    print(f"OptionalValidator: {o}")

    d = DeepIterableValidator(numbers=[1, 2, 3])
    print(f"DeepIterableValidator: {d}")

    cb = CallableFieldValidator(callback=lambda x: x)
    print(f"CallableFieldValidator: {cb}")
