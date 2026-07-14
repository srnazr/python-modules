*This project has been created as part of the 42 curriculum by szaarour.*

# Code Nexus: Polymorphic Data Streams in the Digital Matrix

## Description

Code Nexus introduces object-oriented design in Python through the story of a
futuristic data processing system set in Neo-Tokyo, 2087. Across three
exercises, a data processing architecture is progressively built: first
defining a shared abstract interface for different data types, then unifying
those types into a single adaptive stream router, and finally adding a
plugin-based export system built on structural typing.

This project focuses on:

- Abstract classes (`abc.ABC`, `@abstractmethod`)
- Method overriding and subtype polymorphism
- Inheritance hierarchies
- Type annotations with `typing` (`Any`, `Protocol`)
- Duck typing / structural typing
- Exception handling to protect internal state
- Designing reusable, extensible interfaces

---

# Algorithm & Design Choices

## High-level idea

Each exercise extends the previous one, simulating the workflow of a stream
engineer maintaining a cybernetic data processing cathedral.

1. **Data Processor (ex0)**
   - Defines an abstract base class, `DataProcessor`, that fixes a common
     interface (`validate`, `ingest`, `output`) without knowing which concrete
     data type it will eventually handle.
   - Three specialized subclasses (`NumericProcessor`, `TextProcessor`,
     `LogProcessor`) each override `validate` and `ingest` to enforce their
     own rules, while inheriting `output` unchanged.

2. **Data Stream (ex1)**
   - Introduces a `DataStream` class that owns a collection of registered
     processors.
   - Routes each incoming element to whichever processor can `validate` it,
     without ever checking types directly — this is polymorphism doing the
     dispatching instead of a chain of `if isinstance(...)` checks.
   - Reports running statistics across all registered processors.

3. **Data Pipeline (ex2)**
   - Adds an output side to the pipeline through an `ExportPlugin` protocol.
   - Any class that implements `process_output` can be handed to
     `DataStream.output_pipeline`, whether or not it inherits from anything —
     this is duck typing / structural typing via `typing.Protocol`.
   - Two concrete plugins (CSV and JSON) are provided as examples.

Each exercise deliberately restricts imports to `abc` and `typing` so that the
mechanics of polymorphism are handled by hand, instead of being hidden behind
a framework.

---

# Project Files Info

## ex0: `data_processor.py`

Defines the abstract `DataProcessor` class and its three subclasses. Each
subclass stores its own ingested items internally (oldest-first) and exposes
them one at a time through `output`. Includes a test scenario that validates
both correct and incorrect data, and demonstrates that calling `ingest`
without validating first raises an exception.

---

## ex1: `data_stream.py`

Builds on ex0. Introduces `DataStream`, which:

- registers any number of `DataProcessor` instances,
- routes each element of an incoming list to the first processor whose
  `validate` method accepts it,
- prints an error for any element no processor can handle,
- prints running statistics (`total processed` / `remaining`) per processor.

---

## ex2: `data_pipeline.py`

Builds on ex1. Introduces:

- `ExportPlugin`, a `Protocol` describing anything with a
  `process_output(self, data: list[tuple[int, str]]) -> None` method,
- `output_pipeline`, a `DataStream` method that pulls `nb` items from every
  registered processor and forwards them to a given plugin,
- `CSVExportPlugin` and `JSONExportPlugin`, two independent classes that
  satisfy the protocol without inheriting from it.

---

# Concepts

## What is an abstract class, and why use one?

An abstract class is a class that is not meant to be instantiated directly.
It exists to define a contract that its subclasses must follow.

```python
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    @abstractmethod
    def validate(self, data: object) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: object) -> None:
        pass
```

Trying to instantiate `DataProcessor()` directly raises a `TypeError`,
because it has unimplemented abstract methods. Only a subclass that provides
`validate` and `ingest` can be instantiated. This guarantees that every
processor in the system exposes the same interface, even though each one
behaves differently internally.

---

## What is method overriding?

Method overriding happens when a subclass provides its own implementation of
a method already defined in its parent class, using the exact same method
name (and, for abstract methods, a compatible signature).

```python
class NumericProcessor(DataProcessor):
    def validate(self, data: object) -> bool:
        return isinstance(data, (int, float))
```

When `validate` is called on a `NumericProcessor` instance, Python runs this
version instead of any placeholder in `DataProcessor`. The parent class
never needs to know how each child implements the behavior.

---

## What is polymorphism, and why does `DataStream` not check types directly?

Polymorphism means that objects of different classes can be treated through
the same interface, and each object automatically responds according to its
own class.

Instead of writing something like:

```python
if isinstance(processor, NumericProcessor):
    ...
elif isinstance(processor, TextProcessor):
    ...
```

`DataStream` simply calls `processor.validate(element)` and
`processor.ingest(element)` on whichever processor accepts the data. Every
registered processor understands these two method names, so the same two
lines of code work correctly no matter which subclass is involved. This is
what makes it possible to add a brand-new processor type later without
touching `DataStream` at all.

---

## Why does `ingest` raise an exception on invalid data?

`validate` is meant to be called first, as a safety check. If a caller skips
that check and calls `ingest` directly with data the processor cannot handle,
there is no safe way to "process" it, silently ignoring bad data would let
the internal storage become inconsistent. Raising an exception makes the
misuse visible immediately instead of corrupting the data processor's state.

---

## What is `typing.Protocol`, and how is it different from inheriting `ABC`?

`ABC` and `Protocol` both describe a contract, but they are enforced very
differently.

- With `ABC`, a class must explicitly inherit from the abstract class to be
  considered part of the hierarchy, and Python checks at instantiation time
  that every abstract method is implemented.
- With `Protocol`, a class does **not** need to inherit from anything. It
  only needs to define methods with matching names and signatures. This is
  called **structural typing**, or more informally **duck typing**: "if it
  walks like a duck and quacks like a duck, it's a duck."

```python
from typing import Protocol


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        print(",".join(value for _, value in data))
```

`CSVExportPlugin` never mentions `ExportPlugin` anywhere, yet it can be
passed to `output_pipeline(nb, plugin)` because it has the right shape. This
keeps the export system open: anyone can write a new plugin without touching
`DataStream` or importing an unrelated base class.

---

## Why type-annotate `output` as `tuple[int, str]`?

Returning a tuple lets `output` hand back two pieces of information in one
call: an integer processing rank (the position of that item within the
processor's history) and the string representation of the data itself. The
export plugins are written specifically against this `list[tuple[int, str]]`
shape, so the interface between `DataProcessor` and `ExportPlugin` stays
consistent across the whole pipeline.

---

# General Instructions

- Written for Python 3.10+
- Code must pass `flake8`
- All functions require comprehensive type annotations, checked with `mypy`
- Exception handling protects data streams from corruption
- Authorized imports: `abc`, `typing`
- All standard classes, collections, and built-in functions are authorized

---

# How to Test

Run each exercise individually.

```bash
python3 ex0/data_processor.py

python3 ex1/data_stream.py

python3 ex2/data_pipeline.py
```

Run linting and type checking before submission.

```bash
flake8 .
mypy .
```

---

# AI Usage

AI was used as a teaching assistant. It was used to:

- explain abstract classes, method overriding, and polymorphism,
- clarify the difference between `ABC` inheritance and `Protocol` structural
  typing,
- explain how to design a plugin system based on duck typing,
- improve conceptual understanding without replacing implementation.

---

# References

- https://docs.python.org/3/library/abc.html
- https://docs.python.org/3/library/typing.html#typing.Protocol
- https://docs.python.org/3/glossary.html#term-duck-typing
- https://docs.python.org/3/tutorial/classes.html#inheritance
- https://flake8.pycqa.org/
- https://mypy.readthedocs.io/

---

Author: Serena Zaarour  
Intra: szaarour     
42 Beirut