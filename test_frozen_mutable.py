"""Test: @frozen and @mutable decorators.

attrs provides @frozen for immutable classes and @mutable as an alias for @define.
Testing if pyrefly recognizes these decorators.

Docs: https://www.attrs.org/en/stable/api.html#attrs.frozen
      https://www.attrs.org/en/stable/api.html#attrs.mutable
      https://www.attrs.org/en/stable/examples.html#immutability

Related: https://github.com/facebook/pyrefly/issues/1825
"""

from attrs import frozen, mutable, field, evolve, Factory


# Example 1: @frozen decorator (immutable class)
@frozen
class ImmutableConfig:
    name: str
    value: int = 42
    items: list = field(factory=list)


# Example 2: @mutable decorator (same as @define)
@mutable
class MutableConfig:
    name: str
    value: int = 42
    items: list = field(factory=list)


# Example 3: @frozen with Factory defaults
# May trigger Bug A if pyrefly doesn't recognize @frozen
@frozen
class FrozenWithFactory:
    required: str
    optional: str = field(default=Factory(lambda: "default"))
    items: list = field(factory=list)


# Example 4: Using evolve() with frozen classes
@frozen
class Point:
    x: int
    y: int


# Example 5: Nested frozen classes
@frozen
class Rectangle:
    top_left: Point
    bottom_right: Point


# Verify all work at runtime
if __name__ == "__main__":
    ic = ImmutableConfig(name="test")
    print(f"ImmutableConfig: {ic}")

    try:
        ic.value = 100  # Should raise FrozenInstanceError
    except Exception as e:
        print(f"Modifying frozen instance raised: {type(e).__name__}")

    mc = MutableConfig(name="test")
    mc.value = 100  # Should work
    print(f"MutableConfig (modified): {mc}")

    fc = FrozenWithFactory(required="test")
    print(f"FrozenWithFactory: {fc}")

    p1 = Point(x=0, y=0)
    p2 = evolve(p1, x=10)
    print(f"Original: {p1}, Evolved: {p2}")

    r = Rectangle(top_left=Point(0, 10), bottom_right=Point(10, 0))
    print(f"Rectangle: {r}")
