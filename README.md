# pyrefly-issue-1825-mre

Minimum reproducible example for [Pyrefly Issue #1825](https://github.com/facebook/pyrefly/issues/1825).

## The Bug

Pyrefly incorrectly treats `attrs` classes as dataclasses and throws a false positive error when using `Field` with lambda defaults:

```
ERROR Dataclass field `device` without a default may not follow dataclass field with a default [bad-class-definition]
```

## Reproduction
**Expected:** No error — this is valid `attrs` usage per [attrs documentation](https://www.attrs.org/en/stable/init.html#defaults).

**Actual:** Pyrefly reports `[bad-class-definition]` error.

## Setup

```bash
# Install dependencies
uv sync

# Run the code (works correctly)
uv run python main.py

# Run pyrefly check (shows the bug)
uv run pyrefly check
```

## Environment

- Python 3.14
- attrs 25.4.0
- torch 2.9.1
- pyrefly 0.45.2
