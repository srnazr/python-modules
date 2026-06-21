This project has been created as part of the 42 curriculum by szaarour.

# Growing Code

## Description

The Growing Code project is an introduction to Python's fundamental syntax and
semantics, built around a series of small exercises framed as community garden
scenarios. The goal of this project is to get comfortable with the basic
building blocks of Python: expressions, variables, input/output, conditionals,
loops, recursion, and type annotations before moving on to more advanced
project structures.

This project focuses on:

- Writing single-purpose, self-contained functions (no `main` blocks)
- Reading and validating user input with `input()`
- Basic control flow: conditionals and loops
- Iterative vs. recursive problems
- Respecting `flake8` standards

## Algorithm & Design Choices

### High-level idea

Each exercise is isolated in its own file and exposes exactly one function
(two, for the recursion exercise). Every function is self-contained: it
handles its own input and output directly, with no `if __name__ ==
"__main__":` block and no top-level code. This keeps each exercise focused on
a single concept and makes them trivially importable and testable via the
provided `main.py` helper.

As the exercises progress, the concepts build on top of each other:

1. Output only (`print`)
2. Input + output (`input`, `print`)
3. Input + arithmetic + output
4. Conditionals (`if` / `else`)
5. Conditionals with a different threshold/message pattern
6. Loops: both iterative (`range`) and recursive approaches
7. Function parameters, return types, and string methods, all under strict
   type hints

## Project Structure & File Roles

```
ex0/ft_hello_garden.py
ex1/ft_garden_name.py
ex2/ft_plot_area.py
ex3/ft_harvest_total.py
ex4/ft_plant_age.py
ex5/ft_water_reminder.py
ex6/ft_count_harvest_iterative.py
ex6/ft_count_harvest_recursive.py
ex7/ft_seed_inventory.py
```

**ex0: `ft_hello_garden`**
Prints a fixed welcome message. No arguments, no input.

**ex1: `ft_garden_name`**
Asks for a garden name and echoes it back alongside a fixed status line.

**ex2: `ft_plot_area`**
Asks for a length and a width, then prints the computed rectangular area.

**ex3: `ft_harvest_total`**
Asks for three separate harvest weights and prints their sum.

**ex4: `ft_plant_age`**
Asks for a plant's age in days and reports whether it's ready to harvest
(strictly more than 60 days).

**ex5: `ft_water_reminder`**
Asks for the number of days since the last watering and reminds the user to
water if it's been more than 2 days.

**ex6: `ft_count_harvest_iterative` / `ft_count_harvest_recursive`**
Two implementations of the same behavior: count from 1 up to a given number,
printing each day, then announce harvest time. One uses `range`, the other
uses recursion.

**ex7: `ft_seed_inventory`**
The first fully type-hinted exercise. Signature is fixed:

```python
def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
```

Capitalizes the seed type and prints a unit-specific message for `"packets"`,
`"grams"`, or `"area"`. Any other unit prints `"Unknown unit type"` only.
Type hints are checked with `mypy`.

## How to Test

A `main.py` helper is provided to import and run each exercise function
without needing to write any driver code yourself.

```bash
python3 main.py
```

Place it in the same folder as the exercise file(s) you want to test, and
follow the prompts.

## AI Usage

AI was used as a teaching assistant. It was used to:

- talk through flake8/mypy errors
- help set up falke8

## References

- [Python official docs](https://docs.python.org/3/)
- [flake8](https://flake8.pycqa.org/)
- [W3S](https://www.w3schools.com/python/)
- [GeeksforGeeks](https://www.geeksforgeeks.org/python/python-programming-language-tutorial/)

---

Author: Serena Zaarour <br>
Intra: szaarour <br>
42 Campus: Beirut