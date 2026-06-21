This project has been created as part of the 42 curriculum by szaarour.

# Code Cultivation

## Description

The Code Cultivation project picks up where Growing Code left off, moving from
basic Python syntax into program structure and Object-Oriented Programming.
Across seven exercises, a single `Plant` class is progressively grown into a
small but complete garden management system: attributes become encapsulated,
behavior becomes inherited and specialized, and the whole thing ends up
wired together with static methods, class methods, and nested classes.

This project focuses on:

- Program entry points (`if __name__ == "__main__":`)
- Designing a class as a reusable model instead of repeating logic per object
- Instance methods that mutate state (`grow()`, `age()`)
- Constructors (`__init__`) for ready-to-use objects
- Encapsulation and validation (protected attributes, getters/setters)
- Inheritance and method overriding with `super()`
- Static methods, class methods, and nested classes

## Algorithm & Design Choices

### High-level idea

Every exercise reuses and extends the same `Plant` class from the exercise
before it, rather than starting from scratch. The class evolves in layers:

1. **Structure:** a bare script with a `__main__` entry point, no classes yet
2. **Modeling:** a `Plant` class with `name`, `height`, `age`, and `show()`
3. **Behavior:** `grow()` and `age()` methods that mutate the plant's own state
4. **Convenience:** a real constructor (`__init__`) so plants are usable the
   moment they're created
5. **Safety:** protected attributes (`_height`, `_age`) with validated
   setters/getters, so invalid data is rejected at the source
6. **Specialization:** `Flower`, `Tree`, and `Vegetable` subclasses that
   inherit the common `Plant` behavior via `super()` and add their own
   attributes and methods, with `show()` overridden (not duplicated) to add
   to the parent's output
7. **Composition & introspection:** a `Seed` subclass of `Flower`, a static
   method and a class method on `Plant`, and a nested `Stats` class per plant
   instance tracking `grow()` / `age()` / `show()` (and `produce_shade()` for
   trees) call counts, surfaced through a standalone display function

This mirrors the way real systems grow: not by rewriting from zero each time,
but by extending a stable core with new layers of responsibility.

## Project Structure & File Roles

```
ex0/ft_garden_intro.py
ex1/ft_garden_data.py
ex2/ft_plant_growth.py
ex3/ft_plant_factory.py
ex4/ft_garden_security.py
ex5/ft_plant_types.py
ex6/ft_garden_analytics.py
```

**ex0: `ft_garden_intro.py`**
No classes yet. A first runnable script using `if __name__ == "__main__":`,
storing plant info in plain variables and printing it. Also the exercise
where the shebang line is introduced.

**ex1: `ft_garden_data.py`**
Introduces the `Plant` class: `name`, `height`, `age` attributes and a
`show()` method, instantiated for at least three plants instead of handling
each one as separate variables.

**ex2: `ft_plant_growth.py`**
Adds `grow()` and `age()` instance methods so a `Plant` can evolve its own
state over time. Simulates a week of growth and reports the total increase.

**ex3: `ft_plant_factory.py`**
Adds a proper `__init__()` constructor so plants are created fully
initialized in one step. At least five plants with varying starting values,
displayed with the unchanged `show()`.

**ex4: `ft_garden_security.py`**
Encapsulates `height` and `age` behind the protected-attribute convention,
with `get_height()` / `set_height()` and `get_age()` / `set_age()`.
Negative values are rejected with an error message and the original data is
left untouched.

**ex5: `ft_plant_types.py`**
Introduces inheritance: `Flower` (color, `bloom()`), `Tree` (trunk diameter,
`produce_shade()`), and `Vegetable` (harvest season, nutritional value), all
built on top of `Plant` via `super()`. Each subclass's `show()` extends the
parent's output rather than reimplementing it.

**ex6: `ft_garden_analytics.py`**
Ties everything together: a `staticmethod` on `Plant` to check if an age is
over a year, a `classmethod` to create an "anonymous" plant, a `Seed` class
inheriting from `Flower` that tracks seed count after blooming, a nested
`Stats` class per plant tracking method-call counts, and a standalone
function (outside any class) that displays statistics for any plant type.

## General Instructions

- Written for Python 3.10+
- Code must pass `flake8` linting
- Each exercise in its own file and directory
- Naming conventions: `PascalCase` for classes, `snake_case` for functions
  and variables
- All functions and methods require type hints, checked with `mypy`
- No input validation required unless explicitly stated
- `class` and `def` don't need to be listed as "authorized" — they're core
  language keywords
- `if __name__ == "__main__":` blocks are allowed from ex0 onward for
  testing
- Programs must always run without errors

## How to Test

Each file is runnable directly:

```bash
python3 ex0/ft_garden_intro.py
python3 ex1/ft_garden_data.py
# and so on
```

Lint and type-check before submitting:

```bash
flake8 .
mypy .
```

## AI Usage

AI was used as a teaching assistant. It was used to:

- clarify OOP principles.

## References

- [Python official docs: Classes](https://docs.python.org/3/tutorial/classes.html)
- [flake8](https://flake8.pycqa.org/)
- [mypy](https://mypy-lang.org/)
- [Python: Inheritance and Composition](https://realpython.com/inheritance-composition-python/)

---

Author: Serena Zaarour <br>
Intra: szaarour <br>
42 Campus: Beirut