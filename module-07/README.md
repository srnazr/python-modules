*This project has been created as part of the 42 curriculum by szaarour.*

# DataDeck: Abstract Card Architecture for a Composable Creature Battle System

## Description

DataDeck builds a small Creature battle engine through
three exercises, each layering a new design pattern on top of the last.
Instead of hardcoding a fixed roster of Creatures with fixed behavior, the
system is built so that new families, new capabilities, and new battle
tactics can all be added later without rewriting existing code.

This project focuses on:

- Abstract classes (`abc.ABC`, `@abstractmethod`)
- The abstract factory design pattern
- Multiple inheritance and capability composition
- The abstract strategy design pattern
- Encapsulation through package-level interfaces
- Custom exceptions for invalid state combinations

---

# Algorithm & Design Choices

## High-level idea

Each exercise extends the previous one, simulating the workflow of building
a card game engine from the ground up: first the cards themselves, then the
abilities they can carry, then the tactics used to play them.

1. **Creature Factory (ex0)**
   - Defines an abstract `Creature` class that fixes a common interface
     (`attack`, `describe`) without knowing which concrete family it will
     eventually represent.
   - Four concrete Creatures (`Flameling`, `Pyrodon`, `Aquabub`, `Torragon`)
     each override `attack` with their own message.
   - An abstract `CreatureFactory` class, implemented by `FlameFactory` and
     `AquaFactory`, is the only way to obtain a Creature from outside the
     package. This is the abstract factory pattern: calling code asks a
     factory for a base or evolved Creature without ever naming the
     concrete class directly.

2. **Capabilities (ex1)**
   - Introduces `HealCapability` and `TransformCapability`, two abstract
     classes that know nothing about `Creature` at all.
   - Concrete Creatures gain a capability purely through multiple
     inheritance, for example `class Sproutling(Creature, HealCapability)`.
   - `TransformCapability` also carries a persistent `is_transformed` flag,
     so a transformed Creature's `attack` method returns a different
     message than its normal state.
   - `HealingCreatureFactory` and `TransformCreatureFactory` extend the same
     `CreatureFactory` contract from ex0 to produce these new families.

3. **Abstract Strategy (ex2)**
   - Introduces `BattleStrategy`, an abstract class with `is_valid` and
     `act`, and three concrete strategies: `NormalStrategy`,
     `AggressiveStrategy`, and `DefensiveStrategy`.
   - Each strategy checks `is_valid` against a capability, not a concrete
     Creature class, so the same `AggressiveStrategy` works for any
     Creature with `TransformCapability`, regardless of family.
   - The `battle` function in `tournament.py` runs a round robin between
     opponents without ever knowing which capability each Creature has. It
     just calls `strategy.act(creature)` and lets the strategy decide what
     that means.

---

# Project Files Info

## ex0: `battle.py`

Root-level script that instantiates `FlameFactory` and `AquaFactory`, has
each factory produce and test its base and evolved Creature, then makes two
base Creatures fight. Uses only what `ex0/__init__.py` exposes: the
factories, never the concrete Creature classes.

## ex1: `capacitor.py`

Root-level script that instantiates `HealingCreatureFactory` and
`TransformCreatureFactory`, and walks each of their base and evolved
Creatures through describe, attack, and their respective capability
(heal, or transform, attack again, revert).

## ex2: `tournament.py`

Root-level script that runs three tournaments: a basic two-opponent fight, a
fight that deliberately pairs an incompatible Creature-strategy tuple to
demonstrate the error path, and a three-opponent round robin. Contains the
`battle` function that drives all three.

---

# Concepts

## What is the abstract factory pattern, and why hide the concrete classes?

An abstract factory is a class whose whole job is producing other objects,
without the caller ever needing to know which concrete class was built.

```python
class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> "Creature":
        pass

    @abstractmethod
    def create_evolved(self) -> "Creature":
        pass
```

`ex0/__init__.py` only imports from `factory.py`, never from `creature.py`.
That means code outside the package can only ever obtain a Creature by
calling `factory.create_base()` or `factory.create_evolved()`, never by
writing `Flameling()` directly. If a fifth Fire-type Creature needed to
replace `Flameling` tomorrow, every caller of `FlameFactory` would keep
working without a single change.

---

## Why don't capabilities inherit from `Creature`?

`HealCapability` and `TransformCapability` are standalone `abc.ABC` classes
with no reference to `Creature` anywhere in their definition. A capability
describes an ability, not a kind of Creature, so tying it to `Creature`
would make it useless the day something other than a Creature needs to
heal or transform.

A Creature gains a capability purely by inheriting from both:

```python
class Sproutling(Creature, HealCapability):
    def __init__(self) -> None:
        Creature.__init__(self, "Sproutling", "Grass")
```

Each parent's `__init__` is called explicitly rather than relying on a
single `super()` chain, which keeps it obvious which attributes come from
which parent when two unrelated hierarchies meet in one class.

---

## How does a capability change `attack` without `Creature` knowing about it?

`TransformCapability` stores a persistent `is_transformed` flag in its own
`__init__`. A Creature that mixes it in reads that flag inside its own
`attack` override:

```python
def attack(self) -> str:
    if self.is_transformed:
        return f"{self._name} performs a boosted strike!"
    return f"{self._name} attacks normally."
```

`Creature` itself never mentions `is_transformed`. The state lives entirely
in the capability, and the Creature subclass is simply the place where that
state and the attack behavior meet.

---

## What is the abstract strategy pattern, and why does `tournament.py` never check capabilities directly?

A strategy is an interchangeable behavior, selected at runtime, that acts on
an object without that object needing to know which strategy was picked.

Instead of writing something like:

```python
if isinstance(creature, TransformCapability):
    ...
elif isinstance(creature, HealCapability):
    ...
```

inside the tournament code, `battle` just calls `strategy.act(creature)`.
Each strategy carries its own `isinstance` check inside `is_valid`, checking
against the *capability* class rather than any specific Creature family.
That is what lets `AggressiveStrategy` work correctly for `Shiftling`,
`Morphagon`, or any future Creature with `TransformCapability`, without
`tournament.py` being touched at all.

---

## Why raise a dedicated exception instead of failing silently?

`is_valid` returning `False` is a safe check a caller can make ahead of
time. But if `act` is called anyway on an incompatible pairing, silently
doing nothing would hide a real bug in whatever built the tournament. A
dedicated `InvalidStrategyError`, raised with the Creature's name and the
strategy involved, makes the mismatch immediately visible and lets
`tournament.py` catch it, report it, and abort that tournament cleanly
instead of continuing in a broken state.

---

# General Instructions

- Written for Python 3.10+
- Authorized imports: `abc`, `typing`
- All standard built-in types and functions are authorized
- `ex0` and `ex1` packages only expose factories at the package level, never
  concrete Creature classes
- `ex2` exposes its strategies and its exception directly, since none of
  them are concrete Creatures

---

# How to Test

Run each exercise's script from the repository root, since each depends on
the packages built in the exercises before it.

```bash
python3 battle.py

python3 capacitor.py

python3 tournament.py
```

---

# AI Usage

AI was used as a teaching assistant. It was used to:

- explain the abstract factory and abstract strategy design patterns,
- clarify how multiple inheritance can be used to compose independent
  capabilities onto a base class,
- review the exercise scenarios against the expected example output,
- improve conceptual understanding without replacing implementation.

---

# References

- https://docs.python.org/3/library/abc.html
- https://docs.python.org/3/tutorial/classes.html#inheritance
- https://en.wikipedia.org/wiki/Abstract_factory_pattern
- https://en.wikipedia.org/wiki/Strategy_pattern
- https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions

---

Author: Serena Zaarour  
Intra: szaarour     
42 Beirut