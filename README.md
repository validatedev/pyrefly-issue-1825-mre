# pyrefly-issue-1825-mre

Minimum reproducible example for [Pyrefly Issue #1825](https://github.com/facebook/pyrefly/issues/1825).

## The Bug

Pyrefly incorrectly treats `attrs` classes as dataclasses (or this is expected behavior? I don't know 😕) and throws false positives when `Factory` defaults are used.

## Test Layouts (see `test*.py`)

- `test1.py`: required field followed by defaults, then `Factory` `torch.device` default.  
  - **Expected:** attrs accepts this layout.  
  - **Actual:** Pyrefly flags `device` as missing a default.

- `test2.py`: `Factory` default first, then required `name`, then other defaults.  
  - **Expected:** attrs accepts this layout.  
  - **Actual:** Pyrefly flags `name` as following a default without its own.

- `test3.py`: control — every field has a default (no errors).  
  - **Expected/Actual:** passes.

- `test4.py`: several defaults followed by `Factory` `torch.device`.  
  - **Expected:** attrs allows this layout.  
  - **Actual:** Pyrefly flags `device` as missing a default.

## Reproduction
**Expected:** No errors for any layout.  
**Actual:** Pyrefly reports `[bad-class-definition]` errors for the cases above.

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

## Current Errors
```
ERROR Dataclass field `device` without a default may not follow dataclass field with a default [bad-class-definition]
  --> test1.py:28:5
   |
28 |     device: torch.device = field(default=Factory(lambda: torch.device("cpu")))
   |     ^^^^^^
   |
ERROR Dataclass field `name` without a default may not follow dataclass field with a default [bad-class-definition]
  --> test2.py:23:5
   |
23 |     name: str
   |     ^^^^
   |
ERROR Dataclass field `device` without a default may not follow dataclass field with a default [bad-class-definition]
  --> test4.py:27:5
   |
27 |     device: torch.device = field(default=Factory(lambda: torch.device("cpu")))
   |     ^^^^^^
   |
 INFO 3 errors
```