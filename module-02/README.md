This project has been created as part of the 42 curriculum by szaarour.

# Garden Guardian

## Description

Garden Guardian picks up where Code Cultivation left off, moving from Object-Oriented
Programming into resilient data pipeline engineering. Across five exercises, a smart
agriculture monitoring system is progressively hardened against real-world failures:
sensor data is validated, different error types are identified and caught, custom
exception hierarchies are defined, and resources are always cleaned up even when
things go wrong.

This project focuses on:

- Basic exception handling with `try/except` blocks
- Catching and raising specific built-in exceptions (`ValueError`, `ZeroDivisionError`,
  `FileNotFoundError`, `TypeError`)
- Designing custom exception class hierarchies with inheritance
- The `finally` block for resource cleanup

## Algorithm & Design Choices

### High-level idea

Every exercise builds on the previous one, rather than starting from scratch. The
exception-handling skill grows in layers:

1. **First catch:** a simple `try/except` around `int()` that prevents a bad sensor
   reading from crashing the program
2. **Raising:** `input_temperature()` is upgraded to actively reject out-of-range
   values by raising `ValueError` itself, not just catching what Python raises
3. **Multiple types:** a single `try/except` block demonstrates that Python uses
   different exception classes for different failure modes, and that all of them can
   be caught together without calling `type()`
4. **Custom errors:** a small hierarchy (`GardenError` → `PlantError` / `WaterError`)
   shows how inheritance makes error handling composable — catching the parent catches
   all children
5. **Cleanup:** the `finally` block guarantees the watering system is closed whether
   or not a `PlantError` was raised, mirroring how real resource management works

This mirrors the way production systems are hardened: not by avoiding errors, but by
handling them at the right level of specificity and always leaving the system in a
clean state.

## Project Structure & File Roles

```
ex0/ft_first_exception.py
ex1/ft_raise_exception.py
ex2/ft_different_errors.py
ex3/ft_custom_errors.py
ex4/ft_finally_block.py
```

**ex0: `ft_first_exception.py`**
The first `try/except`. `input_temperature()` converts a string to an integer and
`test_temperature()` shows that a bad input is caught gracefully and the program
keeps running.

**ex1: `ft_raise_exception.py`**
Extends ex0 by adding range validation inside `input_temperature()`. Valid strings
that produce out-of-range temperatures (e.g. `"100"`, `"-50"`) now trigger a
manually raised `ValueError` with a descriptive message.

**ex2: `ft_different_errors.py`**
A single `try/except` block catches four distinct exception types raised by
`garden_operations()`: `ValueError`, `ZeroDivisionError`, `FileNotFoundError`, and
`TypeError`. Demonstrates how Python's exception hierarchy lets multiple types be
caught in one clause without using `type()`.

**ex3: `ft_custom_errors.py`**
Defines a three-class hierarchy: `GardenError(Exception)` as the base, with
`PlantError(GardenError)` and `WaterError(GardenError)` as specializations. Shows
how catching the parent class automatically handles all child exceptions.

**ex4: `ft_finally_block.py`**
Introduces the `finally` block. `water_plant()` raises a `PlantError` for
non-capitalized plant names; `test_watering_system()` catches it and returns early,
but the `finally` block always closes the watering system regardless.

## Concepts

### Why does Python have different types of errors?

Python uses a class hierarchy for exceptions so that different failure causes can be
handled at different levels of specificity. A `ZeroDivisionError` tells you *why* the
operation failed, not just *that* it failed. This lets you catch only what you know how
to handle (e.g. retry on `FileNotFoundError`) while letting unexpected errors propagate
up. It also makes code self-documenting: the exception name communicates intent without
needing a comment.

### How can you catch multiple error types with a single `try` block?

By passing a tuple of exception classes to `except`:

```python
except (ValueError, ZeroDivisionError, FileNotFoundError, TypeError) as e:
    print(f"Caught {e.__class__.__name__}: {e}")
```

`e.__class__.__name__` gives the class/error name as a string.

### When should you create your own error types instead of using built-in ones?

When the built-in names are too generic for the domain. `ValueError` tells Python
programmers that a value was invalid; `PlantError` tells your teammates (and future
you) that a plant-specific contract was violated. Custom types also let callers be
selective: code that only cares about watering problems can catch `WaterError` and let
`PlantError` propagate, without any extra branching.

### How does inheritance help organize different types of errors?

Inheriting from a shared base (`GardenError`) means callers can choose their level of
specificity. Catch `PlantError` to handle only plant failures. Catch `GardenError` to
handle any garden-related failure in one clause. Let unknown errors propagate as
`Exception`. The hierarchy is a decision tree baked into the class structure.

### Why is it important to clean up resources even when errors happen?

Uncleaned resources (open files, database connections, hardware locks, network sockets)
can corrupt state, exhaust system limits, or block other processes long after your
program has crashed. In an agricultural context, an unclosed irrigation valve could
flood a field. The `finally` block decouples cleanup from success: it runs whether the
`try` succeeded, an exception was caught, or even if the function returned early.

## General Instructions

- Written for Python 3.10+
- Code must pass `flake8` linting
- Each exercise in its own file and directory
- All functions and methods require type hints, checked with `mypy`
- `type()` is not permitted for identifying exceptions — use `e.__class__.__name__`
- The `TypeError` in ex2 is intentional and will produce a `mypy` warning by design
- Programs must always run without errors

## How to Test

Each file is runnable directly:

```bash
python3 ex0/ft_first_exception.py
python3 ex1/ft_raise_exception.py
python3 ex2/ft_different_errors.py
python3 ex3/ft_custom_errors.py
python3 ex4/ft_finally_block.py
```

Lint and type-check before submitting:

```bash
flake8 .
mypy .
```

## AI Usage

AI was used as a teaching assistant. It was used to:

- clarify exception handling concepts and the Python exception hierarchy.

## References

- [Python official docs: Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
- [flake8](https://flake8.pycqa.org/)
- [mypy](https://mypy-lang.org/)
- [Python Built-in Exceptions](https://docs.python.org/3/library/exceptions.html)

---

Author: Serena Zaarour <br>
Intra: szaarour <br>
42 Campus: Beirut