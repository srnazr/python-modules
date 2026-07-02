This project has been created as part of the 42 curriculum by szaarour.

# Data Quest: Mastering Python Collections

## Description

Data Quest picks up where exception handling left off, moving from graceful error
recovery into Python's core data structures. Across seven exercises, a game analytics
platform is progressively built: command-line arguments become player data, lists
become score sheets, tuples become 3D coordinates, sets become achievement trackers,
dictionaries become inventories, generators become event streams, and comprehensions
become the elegant glue that ties it all together.

This project focuses on:

- Reading and processing command-line parameters (`sys.argv`)
- `list`: ordered, indexed, expandable collections
- `tuple`: ordered, immutable, hashable collections
- `set`: unordered collections of unique elements, and set algebra (union,
  intersection, difference)
- `dict`: key-value pairs and their associated methods
- `generator` functions with `yield` for on-demand, memory-efficient data streams
- `list` and `dict` comprehensions for concise data transformation

## Algorithm & Design Choices

### High-level idea

Every exercise unlocks a new collection type and layers it onto the same theme, a
game analytics platform, so each data structure is learned in a context where its
tradeoffs actually matter:

1. **Command Quest:** `sys.argv` is explored as Python's built-in list, the entry
   point for every other exercise
2. **Score Cruncher:** raw argument strings become a validated `list` of scores,
   with invalid entries filtered out via `try/except` rather than crashing the program
3. **Position Tracker:** coordinates are stored as `tuple`s because a 3D point is a
   fixed, immutable unit of data. It should never accidentally be mutated mid-calculation
4. **Achievement Hunter:** player achievements are stored as `set`s, since duplicate
   achievements make no sense and set algebra (union/intersection/difference) is the
   natural way to compare players
5. **Inventory Master:** items map naturally to quantities, so a `dict` is used, with
   `key:value` command-line parsing and percentage/aggregate calculations
6. **Stream Wizard:** `gen_event()` demonstrates that an infinite stream of data can
   be produced lazily with `yield`, without ever holding it all in memory
7. **Data Alchemist:** list and dict comprehensions replace multi-line loops with
   single, readable expressions for filtering and transforming player data

Each exercise deliberately restricts allowed built-ins and imports, forcing the
underlying collection's own methods to be understood and used correctly rather than
worked around with unrelated helpers.

## Project Files Info
**ex0: `ft_command_quest.py`**
Reads `sys.argv` and reports the program name, the number of arguments received, and
each argument individually. Introduces the list-like nature of command-line
parameters.

**ex1: `ft_score_analytics.py`**
Parses game scores from `sys.argv` into a `list`, discarding non-numeric values with
an error message via `try/except`. Computes count, total, average, max, min, and
range using `sum()`, `max()`, and `min()`.

**ex2: `ft_coordinate_system.py`**
Defines `get_player_pos()`, which repeatedly prompts for `x,y,z` input until a valid
`tuple` of floats is produced. Computes the Euclidean distance to the origin and
between two successively entered coordinate sets using `math.sqrt()`.

**ex3: `ft_achievement_tracker.py`**
Defines `gen_player_achievements()`, which randomly samples a fixed achievement pool
into a `set` for each of at least four players. Computes the union of all
achievements, the intersection shared by everyone, each player's unique achievements
(`difference`), and each player's missing achievements.

**ex4: `ft_inventory_system.py`**
Parses `item_name:quantity` pairs from `sys.argv` into a `dict`, discarding malformed
or duplicate entries. Reports the item list, total quantity, each item's percentage
share, the most/least abundant items (first-seen wins ties), and updates the
inventory with a new item via `dict.update()`.

**ex5: `ft_data_stream.py`**
Defines the infinite generator `gen_event()`, which yields random `(name, action)`
tuples on each `next()` call. Consumes 1000 events in a loop, builds a list of 10
more, then defines `consume_event()`, a generator that randomly drains that list one
element at a time via `for .. in ..`.

**ex6: `ft_data_alchemist.py`**
Builds a mixed-case list of player names, then uses list comprehensions to produce a
fully capitalized version and a filtered list of names that were already capitalized.
Builds a `dict` of random scores via dict comprehension, then a second dict
comprehension filters for scores above the average.

## Concepts

### Why use a list for command-line arguments instead of, say, individual variables?

`sys.argv` is inherently variable-length, a program might receive zero arguments or
a hundred. A list is the natural fit because it's ordered, indexed, and expandable,
letting the same code handle any number of inputs without knowing that number in
advance.

### Why are tuples the right choice for 3D coordinates instead of lists?

A coordinate like `(x, y, z)` represents a single, complete, fixed-size unit of data,
it doesn't grow or shrink. Tuples are immutable, so once a position is captured it
can't be accidentally modified mid-calculation, and their hashability means they could
later be used as dictionary keys (e.g. a position → object lookup) without extra work.

### What makes sets useful for tracking achievements, and how do union, intersection,
and difference differ?

Achievements are inherently unique: a player either has one or doesn't, and
duplicates are meaningless. Sets enforce that uniqueness automatically. `union()`
combines all distinct achievements across players, `intersection()` finds what every
player shares, and `difference()` finds what one player has that another set doesn't,
the exact operation needed to compute "achievements no one else has" or
"achievements still missing."

### Why store inventory as a dictionary rather than two parallel lists?

A dictionary ties each item name directly to its quantity as a single association,
so looking up, updating, or checking for an item is a direct key access rather than
searching two lists in lockstep and hoping their indices stay aligned. `dict.update()`
also makes adding or replacing entries a single, atomic-feeling operation.

### How do generators differ from lists, and why does that matter at scale?

A list computes and stores every element upfront; a generator computes each element
only when `next()` is called, keeping just one value in memory at a time. For an
endless or very large stream, like a live feed of game events, a list would either
run out of memory or force an artificial stopping point, while a generator can run
indefinitely with constant memory usage. This is the same principle from the
project's foreword: the right container turns a bottleneck into a non-issue.

### What do comprehensions provide beyond writing the equivalent loop by hand?

A comprehension expresses the *what* (transform this, filter that) in one line,
without the *how* (initialize an empty container, loop, conditionally append). This
makes the intent immediately visible and reduces the chance of loop-bookkeeping bugs,
while producing exactly the same result as the longer, explicit version.

## General Instructions

- Written for Python 3.10+
- Code must pass `flake8` linting
- All functions and methods require type hints, checked with `mypy`
- No file I/O, all data comes from command-line arguments or in-memory generation
- Each exercise only uses the imports/builtins explicitly authorized for it
- Invalid or erroneous inputs are handled gracefully via `try/except`, never crash
  the program
- Output format in each exercise mirrors the examples given in the subject

## How to Test

Each file is runnable directly:

```bash
python3 ex0/ft_command_quest.py hello world 42
python3 ex1/ft_score_analytics.py 1500 2300 1800 2100 1950
python3 ex2/ft_coordinate_system.py
python3 ex3/ft_achievement_tracker.py
python3 ex4/ft_inventory_system.py sword:1 potion:5 shield:2
python3 ex5/ft_data_stream.py
python3 ex6/ft_data_alchemist.py
```

Lint and type-check before submitting:

```bash
flake8 .
mypy .
```

## AI Usage

AI was used as a teaching assistant. It was used to:

- clarify the tradeoffs between Python's collection types and when each is
  appropriate.

## References

- [Python official docs: Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Python official docs: Generators](https://docs.python.org/3/howto/functional.html#generators)
- [flake8](https://flake8.pycqa.org/)
- [mypy](https://mypy-lang.org/)
- [Python `sys` module](https://docs.python.org/3/library/sys.html)

---

Author: Serena Zaarour <br>
Intra: szaarour <br>
42 Campus: Beirut