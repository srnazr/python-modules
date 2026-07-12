*This project has been created as part of the 42 curriculum by szaarour.*

# Data Archivist: Python File Operations

## Description

Data Archivist introduces Python file handling through the story of a futuristic
digital preservation system. Across four exercises, a simple archive management
program is progressively expanded: first recovering archived text files, then
creating new archives, then mastering the three standard streams used by every
program, and finally securing all file operations using Python's context managers.

This project focuses on:

- Opening, reading, writing, and closing files
- Command-line arguments with `sys.argv`
- File objects (`typing.IO`)
- Exception handling during file operations
- The three standard streams:
  - `sys.stdin`
  - `sys.stdout`
  - `sys.stderr`
- Output buffering and `flush()`
- Context managers (`with`)
- Returning multiple values through tuples
- Writing safe, clean, and maintainable file-handling code

---

# Algorithm & Design Choices

## High-level idea

Each exercise extends the previous one, simulating the workflow of a digital
archivist responsible for preserving important information.

1. **Ancient Text Recovery**
   - Opens a file supplied through the command line.
   - Reads its contents exactly as the Unix `cat` command would.
   - Handles missing or inaccessible files without crashing.

2. **Archive Creation**
   - Reuses the recovery program.
   - Processes every line by appending the archive marker `#`.
   - Displays the transformed contents.
   - Allows the user to save the transformed archive into another file.

3. **Stream Management**
   - Introduces the three standard streams.
   - User input is obtained directly through `sys.stdin`.
   - Normal output is written to `sys.stdout`.
   - Error messages are redirected to `sys.stderr`.
   - Demonstrates output buffering with `flush()`.

4. **Vault Security**
   - Introduces Python's context manager (`with`).
   - Creates a reusable function capable of safely reading or writing files.
   - Every operation returns a tuple describing whether it succeeded and either
     the resulting file contents or the corresponding error message.

Each exercise intentionally limits the allowed functions and imports so the
fundamental mechanisms behind Python's file handling become clear instead of
being hidden behind higher-level utilities.

---

# Project Files Info

## ex0: `ft_ancient_text.py`

Reads a filename from `sys.argv`, opens the file, displays its contents, and
properly handles file-opening errors while manually closing the file.

---

## ex1: `ft_archive_creation.py`

Transforms every line by appending a `#` character, displays the modified text,
asks the user for a destination filename, and writes the transformed archive
into a new file if requested.

---

## ex2: `ft_stream_management.py`

Introduces Python's three standard streams.

Reads user input through `sys.stdin`, prints normal output through
`sys.stdout`, prints exceptions through `sys.stderr`, and demonstrates
`flush()` to ensure prompts appear immediately.

---

## ex3: `ft_vault_security.py`

Implements the reusable `secure_archive()` function using Python's
`with` statement.

Supports both reading and writing operations while automatically managing file
resources and returning a tuple:

```python
(success, result)
```

where:

- `success` is a boolean indicating whether the operation succeeded.
- `result` contains either the file contents or an error message.

---

# Concepts

## Why does `open()` return a file object instead of the file contents?

Opening a file only establishes a connection between the program and the file.
The returned file object provides methods such as:

- `read()`
- `write()`
- `readline()`
- `close()`

which allow different operations to be performed without reopening the file.

---

## Why manually call `close()`?

An opened file consumes operating system resources.

Closing it:

- releases those resources,
- ensures all buffered data is written to disk,
- prevents file corruption,
- allows other programs to safely access the file.

Exercises 0–2 intentionally avoid `with` so the importance of manually closing
files becomes clear.

---

## Why use exceptions instead of checking whether files exist?

Many things besides a missing file can prevent opening it:

- missing permissions
- invalid path
- directory instead of file
- hardware failures

Trying the operation and handling exceptions lets one piece of code correctly
handle every failure.

---

## Why use tuples to return results?

The project requires returning both

- whether the operation succeeded, and
- the associated data.

Instead of using two separate return statements, both values are grouped into a
tuple.

Example:

```python
(True, file_contents)
```

or

```python
(False, error_message)
```

which can later be accessed as

```python
result[0]
result[1]
```

or unpacked as

```python
success, data = secure_archive(...)
```

---

## Why introduce the standard streams?

Every program communicates through three standard channels:

- input
- normal output
- error output

Separating errors from normal program output makes programs easier to debug and
allows the operating system to redirect them independently.

---

## Why use a context manager?

A context manager guarantees that cleanup code always executes.

For files, this means the file is automatically closed even if an exception
occurs while reading or writing.

---

# Notes

## `with open(...)` vs `file: typing.IO = open(...)`

Both create the exact same type of object:

```python
file: typing.IO = open("file.txt", "r")
```

and

```python
with open("file.txt", "r") as file:
```

Both produce a **file object** (`typing.IO`).

The difference is resource management.

### Manual approach

```python
file = open("file.txt", "r")

try:
    data = file.read()
finally:
    file.close()
```

The programmer is responsible for calling `close()`.

---

### Context manager

```python
with open("file.txt", "r") as file:
    data = file.read()
```

Python automatically performs:

```python
file.close()
```

even if an exception occurs.

This makes `with` the preferred and safest way to work with files.

---

## Standard Streams

Every Python program automatically receives three streams.

### `sys.stdin`

Standard Input.

Usually connected to the keyboard.

Example:

```python
name = sys.stdin.readline()
```

Equivalent to:

```python
name = input()
```

except `readline()` keeps the trailing newline (`\n`).

---

### `sys.stdout`

Standard Output.

Normal program output.

Both of these write to stdout:

```python
print("Hello")
```

```python
sys.stdout.write("Hello\n")
```

The difference is that `print()` automatically adds a newline while
`write()` does not.

---

### `sys.stderr`

Standard Error.

Used exclusively for error messages.

Example:

```python
print("Error", file=sys.stderr)
```

Using stderr allows normal output and errors to be redirected separately by the
operating system.

---

## What does `flush()` do?

Python does not always display output immediately.

Instead, output is temporarily stored inside an internal buffer.

```python
sys.stdout.write("Enter filename: ")
```

may not immediately appear because no newline was printed.

Calling

```python
sys.stdout.flush()
```

forces Python to immediately send everything currently waiting in the output
buffer to the terminal.

Without `flush()`, the prompt might not appear until after the program is
already waiting for user input.

---

# General Instructions

- Written for Python 3.10+
- Code must pass `flake8`
- All functions require type hints checked with `mypy`
- Exercises 0–2 must not use the `with` statement
- Exercise 3 must use the `with` statement
- Only the authorized imports and built-in functions are used
- File operations must gracefully handle exceptions without crashing
- Output format follows the project subject examples

---

# How to Test

Run each exercise individually.

```bash
python3 ex0/ft_ancient_text.py ancient_fragment.txt

python3 ex1/ft_archive_creation.py ancient_fragment.txt

python3 ex2/ft_stream_management.py ancient_fragment.txt

python3 ex3/ft_vault_security.py
```

Run linting and type checking before submission.

```bash
flake8 .
mypy .
```

---

# AI Usage

AI was used as a teaching assistant. It was used to:

- explain Python's file objects and file I/O,
- clarify exception handling for file operations,
- explain the differences between manual file management and context managers,
- explain the purpose of `stdin`, `stdout`, `stderr`, and output buffering,
- improve conceptual understanding without replacing implementation.

---

# References

- https://docs.python.org/3/tutorial/inputoutput.html
- https://docs.python.org/3/library/functions.html#open
- https://docs.python.org/3/library/sys.html
- https://docs.python.org/3/library/io.html
- https://docs.python.org/3/reference/compound_stmts.html#with
- https://flake8.pycqa.org/
- https://mypy.readthedocs.io/

---

Author: Serena Zaarour  
Intra: szaarour  
42 Beirut