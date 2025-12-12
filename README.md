# pyrefly-issue-1825-mre

Minimum reproducible example for [Pyrefly Issue #1825](https://github.com/facebook/pyrefly/issues/1825).

## Summary

Pyrefly has **incomplete attrs support**, treating attrs classes as dataclasses and missing key attrs-specific features. This results in false positive errors for valid attrs code.

## Bug Categories

### Bug A: `Factory()` / `factory=` defaults not recognized

**File:** `test_factory_defaults.py`

Pyrefly doesn't recognize `Factory()` or `factory=` as valid default mechanisms. It incorrectly reports:
- `"Dataclass field without a default may not follow dataclass field with a default"`

**attrs behavior:** `Factory()` is the standard way to provide mutable defaults (lists, dicts, etc.) to avoid the classic Python mutable default argument bug.

### Bug B: `@field.default` decorator not recognized

**File:** `test_field_default_decorator.py`

Pyrefly doesn't understand that `field()` returns a descriptor with a `.default` method. It sees the type annotation instead, causing:
- `"Object of class dict has no attribute default"` (sees `dict` type, not field descriptor)
- `"Missing argument in function __init__"` (consequence of above)

**attrs behavior:** The `@field.default` decorator pattern allows computed defaults that can depend on other attributes.

### Bug C: `@field.validator` decorator not recognized

**File:** `test_field_validator_decorator.py`

Same root cause as Bug B. Pyrefly sees the type annotation instead of the field descriptor:
- `"Object of class int has no attribute validator"`

**attrs behavior:** The `@field.validator` decorator pattern allows inline validator definitions.

## Test Files

| File | Description | Pyrefly Result |
|------|-------------|----------------|
| `test_factory_defaults.py` | `Factory()` and `factory=` patterns | 3 errors (Bug A) |
| `test_factory_defaults_control.py` | Control case (standard order) | 0 errors ✓ |
| `test_field_default_decorator.py` | `@field.default` decorator | 4 errors (Bug B) |
| `test_field_validator_decorator.py` | `@field.validator` decorator | 4 errors (Bug C) |
| `test_validator_callable.py` | Callable validators (non-decorator) | 0 errors ✓ |
| `test_validator_builtin.py` | Built-in validators | 0 errors ✓ |
| `test_converter.py` | Converter functions | 0 errors ✓ |
| `test_frozen_mutable.py` | `@frozen` and `@mutable` decorators | 1 error (correct behavior) |

**Total: 12 errors** (11 false positives + 1 correct detection)

## Reproduction

```bash
# Install dependencies
uv sync

# Run the code (all tests work correctly at runtime)
uv run python test_factory_defaults.py
uv run python test_field_default_decorator.py
uv run python test_field_validator_decorator.py
# ... etc

# Run pyrefly check (shows the bugs)
uv run pyrefly check
```

## Current Errors

```
ERROR Dataclass field `device` without a default may not follow dataclass field with a default [bad-class-definition]
  --> test_factory_defaults.py:32:5
ERROR Missing argument `device` in function `ModelConfig.__init__` [missing-argument]
  --> test_factory_defaults.py:74:21
ERROR Missing argument `device` in function `AllFactoryDefaults.__init__` [missing-argument]
  --> test_factory_defaults.py:80:28
ERROR Object of class `dict` has no attribute `default` [missing-attribute]
  --> test_field_default_decorator.py:38:6
ERROR Object of class `int` has no attribute `default` [missing-attribute]
  --> test_field_default_decorator.py:50:6
ERROR Missing argument `a` in function `C.__init__` [missing-argument]
  --> test_field_default_decorator.py:59:10
ERROR Missing argument `x` in function `DependentDefault.__init__` [missing-argument]
  --> test_field_default_decorator.py:62:25
ERROR Object of class `int` has no attribute `validator` [missing-attribute]
  --> test_field_validator_decorator.py:32:6
ERROR Object of class `int` has no attribute `validator` [missing-attribute]
  --> test_field_validator_decorator.py:44:6
ERROR Object of class `int` has no attribute `validator` [missing-attribute]
  --> test_field_validator_decorator.py:57:6
ERROR Object of class `int` has no attribute `validator` [missing-attribute]
  --> test_field_validator_decorator.py:62:6
ERROR Cannot set field `value` [read-only]
  --> test_frozen_mutable.py:61:9
```

## Environment

- Python 3.14
- attrs 25.4.0
- torch 2.9.1
- pyrefly 0.45.2

## References

- [attrs documentation - Examples](https://www.attrs.org/en/stable/examples.html)
- [attrs documentation - API Reference](https://www.attrs.org/en/stable/api.html)
- [attrs documentation - Type Checking (Pyright/mypy)](https://www.attrs.org/en/stable/types.html)
- [Pyrefly Issue #1825](https://github.com/facebook/pyrefly/issues/1825)

## Root Cause Analysis

The core issue appears to be that pyrefly treats `x: int = field()` as if `x` has type `int` at class definition time. In reality:

1. **During class definition:** `field()` returns a field descriptor object with methods like `.default` and `.validator`
2. **At runtime:** After `@define` processes the class, `x` becomes an instance attribute with type `int`

Pyrefly needs to understand that within an attrs-decorated class body, `field()` returns a special descriptor, not the annotated type. This is similar to how mypy and Pyright handle attrs via plugins.
