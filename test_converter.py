"""Test: Converters in attrs.

attrs supports converter functions that transform input values.

Docs: https://www.attrs.org/en/25.4.0/examples.html#conversion
      https://www.attrs.org/en/25.4.0/api.html#converters

Related: https://github.com/facebook/pyrefly/issues/1825
"""

from attrs import define, field, converters


# Example 1: Basic converter
@define
class BasicConverter:
    x: int = field(converter=int)


# Example 2: Multiple converters using list
@define
class ChainedConverters:
    value: int = field(converter=[str.strip, int])


# Example 3: Optional converter
@define
class OptionalConverter:
    count: int | None = field(
        default=None, converter=converters.optional(int)
    )


# Example 4: default_if_none converter
@define
class DefaultIfNoneConverter:
    items: list = field(
        default=None, converter=converters.default_if_none(factory=list)
    )


# Example 5: to_bool converter
@define
class BoolConverter:
    enabled: bool = field(converter=converters.to_bool)


# Example 6: Custom converter with lambda
@define
class LambdaConverter:
    names: list[str] = field(converter=lambda x: [s.upper() for s in x])


# Verify all work at runtime
if __name__ == "__main__":
    b = BasicConverter(x="42")
    print(f"BasicConverter('42'): {b}, x={b.x}")

    c = ChainedConverters(value="  123  ")
    print(f"ChainedConverters('  123  '): {c}")

    o1 = OptionalConverter(count="5")
    o2 = OptionalConverter(count=None)
    print(f"OptionalConverter('5'): {o1}")
    print(f"OptionalConverter(None): {o2}")

    d = DefaultIfNoneConverter(items=None)
    print(f"DefaultIfNoneConverter(None): {d}")

    e = BoolConverter(enabled="yes")
    print(f"BoolConverter('yes'): {e}")

    l = LambdaConverter(names=["alice", "bob"])
    print(f"LambdaConverter(['alice', 'bob']): {l}")
