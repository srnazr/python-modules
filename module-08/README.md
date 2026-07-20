*This project has been created as part of the 42 curriculum by szaarour.*

# The Matrix: Welcome to the Real World of Data Engineering

## Description

The Matrix introduces the foundational tooling every data engineer relies on
before writing a single line of pipeline code: isolated environments,
dependency management, and configuration through environment variables.
Across three exercises, a small "Zion survival kit" is built: a program that
detects and explains virtual environments, a data analysis tool that
contrasts pip and Poetry, and a configuration loader built on `.env` files.

This project focuses on:

- Python virtual environments (`venv`) and `sys.prefix` detection
- Dependency management with `pip` (`requirements.txt`) vs `Poetry`
  (`pyproject.toml`)
- Environment-based configuration with `python-dotenv`
- Separating development and production settings
- Defensive handling of missing dependencies and missing configuration
- Basic data simulation and visualization with `numpy`, `pandas`, and
  `matplotlib`

---

# Algorithm & Design Choices

## High-level idea

Each exercise stands alone but builds toward the same goal: an application
that is safe to install, run, and configure regardless of the machine it
lands on.

1. **construct.py (ex0)**
   - Detects whether the current interpreter is running inside a virtual
     environment by comparing `sys.prefix` against `sys.base_prefix`
     (and checking for `sys.real_prefix` as a fallback).
   - Prints the current Python executable path either way, so the two
     scenarios (global vs isolated) are visibly different at a glance.
   - When no virtual environment is detected, prints the exact commands
     needed to create and activate one (`python -m venv matrix_env`, then
     the platform-specific activation command).
   - When a virtual environment is detected, prints its name, its root
     path, and the resolved `site-packages` path, so the difference
     between global and isolated package locations is explicit rather than
     asserted.

2. **loading.py (ex1)**
   - Checks each required package (`pandas`, `numpy`, `matplotlib`, and
     optionally `requests`) with `importlib.util.find_spec` before
     importing it, so a missing dependency produces a clear installation
     message instead of an unhandled `ImportError`.
   - Uses `numpy` to simulate the Matrix dataset (for example, a random
     walk or noisy signal) rather than a hardcoded list, so the analysis
     step has something genuinely numerical to work with.
   - Runs a small `pandas` analysis (summary statistics) over the
     simulated data, then renders it with `matplotlib` and saves the
     result to `matrix_analysis.png`.
   - Ships both `requirements.txt` and `pyproject.toml` for the same
     dependency set, and prints installed versions for each package so the
     pip/Poetry contrast is visible in the program's own output, not just
     in the files.

3. **oracle.py (ex2)**
   - Loads `MATRIX_MODE`, `DATABASE_URL`, `API_KEY`, `LOG_LEVEL`, and
     `ZION_ENDPOINT` through `python-dotenv`, reading defaults from `.env`
     and letting real environment variables override them.
   - Prints which mode it resolved into (development or production) and
     what that implies for each setting, so the two configurations are
     distinguishable in the output rather than only in the code.
   - Validates that required variables are present and reports missing
     configuration explicitly instead of failing with a bare
     `KeyError`.
   - Ships a `.env.example` with placeholder values only; the real `.env`
     is excluded from version control through `.gitignore`.

Each exercise deliberately keeps its authorized imports narrow (`sys`,
`os`, `site` for ex0; `pandas`, `numpy`, `matplotlib`, `requests` for ex1;
`os`, `sys`, `python-dotenv` for ex2) so the mechanics stay visible instead
of being hidden behind a larger framework.

---

# Project Files Info

## ex0: `construct.py`

Detects the current environment using `sys.prefix` / `sys.base_prefix` and
prints either a "still plugged in" warning with setup instructions, or a
"welcome to the construct" confirmation with the environment's path and
`site-packages` location.

---

## ex1: `loading.py`, `requirements.txt`, `pyproject.toml`

Checks for `pandas`, `numpy`, `matplotlib`, and `requests`, reporting
`[OK]` or a missing-dependency warning for each. Simulates a Matrix dataset
with `numpy`, analyzes it with `pandas`, and saves a `matplotlib` plot to
`matrix_analysis.png`. `requirements.txt` and `pyproject.toml` describe the
same dependencies for pip and Poetry respectively.

---

## ex2: `oracle.py`, `requirements.txt`, `.env.example`, `.gitignore`

Loads `MATRIX_MODE`, `DATABASE_URL`, `API_KEY`, `LOG_LEVEL`, and
`ZION_ENDPOINT` via `python-dotenv`, with real environment variables taking
precedence over `.env`. Reports the resolved configuration, flags missing
values, and confirms that no secrets are hardcoded or committed.

---

# Concepts

## What is a virtual environment, and why does it matter?

A virtual environment is an isolated Python installation with its own
`site-packages` directory. Packages installed inside it never touch the
system-wide (global) installation.

```python
import sys

in_venv = sys.prefix != sys.base_prefix
```

When `in_venv` is `True`, the interpreter currently running is the one
inside `matrix_env`, not the system Python. This means two projects on the
same machine can depend on different, even conflicting, versions of the
same package without interfering with each other.

---

## What is the difference between pip and Poetry?

`pip` installs packages listed in `requirements.txt`, a flat list of
package names and versions with no built-in dependency resolution beyond
what's declared. `Poetry` reads `pyproject.toml`, resolves the full
dependency graph (including transitive dependencies), and locks the
resolved versions in `poetry.lock` so installs are reproducible across
machines.

```
# requirements.txt
pandas==2.1.0
numpy==1.25.0

# pyproject.toml
[tool.poetry.dependencies]
python = "^3.10"
pandas = "^2.1.0"
numpy = "^1.25.0"
```

Both describe the same dependencies, but Poetry additionally manages the
virtual environment itself and guarantees that everyone who runs
`poetry install` gets the exact same resolved versions.

---

## Why check for a package before importing it?

Importing an uninstalled package raises `ImportError` and crashes the
program immediately, with no chance to explain what went wrong.
`importlib.util.find_spec` checks whether a package is importable without
actually importing it, so the program can report a clear, specific message
per missing dependency instead of an unhandled traceback.

```python
import importlib.util

if importlib.util.find_spec("pandas") is None:
    print("[MISSING] pandas - run: pip install pandas")
```

---

## Why use environment variables instead of hardcoding configuration?

Hardcoded values like database URLs or API keys get committed to version
control by accident, and they can't change between development and
production without editing code. Environment variables, loaded through
`python-dotenv` from a `.env` file locally and from the real environment in
production, let the same code run against different configurations
depending on where it's executed.

```python
import os
from dotenv import load_dotenv

load_dotenv()
mode = os.getenv("MATRIX_MODE", "development")
```

Because `load_dotenv()` only fills in variables that aren't already set,
real environment variables (as set by a deployment system) always take
precedence over the `.env` file, which is exactly why
`MATRIX_MODE=production python oracle.py` overrides whatever `.env`
contains.

---

## Why exclude `.env` from version control?

A `.env` file holds real secrets once it's filled in: database
credentials, API keys, and connection strings. Committing it would expose
those secrets to anyone with read access to the repository, including its
full history even after the file is later deleted. `.env.example` ships
instead, with placeholder values only, so collaborators know which
variables to define without ever seeing real ones.

---

# General Instructions

- Written for Python 3.10+
- Code must pass `flake8`
- All functions require comprehensive type annotations, checked with `mypy`
  (ex1 is exempt from `flake8`/`mypy` errors caused strictly by missing
  optional imports)
- Exception handling protects data streams from corruption
- Authorized imports per exercise: `sys`, `os`, `site` (ex0); `pandas`,
  `requests`, `matplotlib`, `numpy`, `sys`, `importlib` (ex1); `os`, `sys`,
  `python-dotenv` (ex2)
- All standard classes, collections, and built-in functions are authorized
- No virtual environment is submitted in the repository; it must be
  re-creatable during review
- No real secrets are committed; `.env` is listed in `.gitignore`

---

# How to Test

Run each exercise individually, inside and outside a virtual environment.

```bash
# ex0
python3 ex0/construct.py
python3 -m venv matrix_env && source matrix_env/bin/activate
python3 ex0/construct.py

# ex1
python3 ex1/loading.py
pip install -r ex1/requirements.txt
python3 ex1/loading.py
# or, with Poetry
poetry install
poetry run python ex1/loading.py

# ex2
python3 ex2/oracle.py
cp ex2/.env.example ex2/.env
python3 ex2/oracle.py
MATRIX_MODE=production API_KEY=secret123 python3 ex2/oracle.py
```

Run linting and type checking before submission.

```bash
flake8 .
mypy .
```

---

# AI Usage

AI was used as a teaching assistant. It was used to:

- explain the mechanics of virtual environment detection (`sys.prefix` vs
  `sys.base_prefix`),
- clarify the practical differences between pip and Poetry dependency
  resolution,
- explain how `python-dotenv` resolves precedence between `.env` and real
  environment variables,
- improve conceptual understanding without replacing implementation.

---

# References

- https://docs.python.org/3/library/venv.html
- https://docs.python.org/3/library/sys.html#sys.prefix
- https://pip.pypa.io/en/stable/reference/requirements-file-format/
- https://python-poetry.org/docs/
- https://pypi.org/project/python-dotenv/
- https://flake8.pycqa.org/
- https://mypy.readthedocs.io/

---

Author: Serena Zaarour
Intra: szaarour
42 Beirut