"""Pyrefly Bug B: @field.default decorator not recognized.

attrs allows defining default values using a decorator pattern:
    x: SomeType = field()
    @x.default
    def _default_x(self):
        return computed_value

Pyrefly errors:
1. "Object of class `dict` has no attribute `default`" - sees type annotation, not field descriptor
2. "Missing argument `a` in function..." - consequence of not recognizing default

The issue: pyrefly sees `a: dict = field()` and thinks `a` has type `dict`.
In reality, `field()` returns a field descriptor that has `.default` method.

Docs: https://www.attrs.org/en/25.4.0/examples.html#defaults
      https://www.attrs.org/en/25.4.0/init.html#defaults

Related: https://github.com/facebook/pyrefly/issues/1825
"""

from attrs import define, field, Factory


# Example from attrs docs: https://www.attrs.org/en/25.4.0/init.html#defaults
# Pyrefly errors:
#   - "Object of class `dict` has no attribute `default`"
#   - "Missing argument `a` in function `C.__init__`"
@define
class C:
    a: dict = field()
    b: list = field(factory=list)
    c: list = Factory(list)  # syntactic sugar for above
    d: int = 42

    @a.default
    def _default_a(self) -> dict[str, str]:
        return {"key": "value"}


# Verify all work at runtime
if __name__ == "__main__":
    c = C()
    print(f"C(): {c}")
