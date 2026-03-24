def garden_operations():
    print("Testing ValueErrror...")
    try:
        int("abc")
    except ValueError as e:
        print(f"Caught ValueError: {e}\n")
    print("Testing ZeroDivisionError...")
    try:
        42 / 0
    except ZeroDivisionError as e:
        print(f"Caught ZeroDivisionError: {e}\n")
    print("Testing FileNotFoundError...")
    try:
        open("missing.txt", "r")
    except FileNotFoundError:
        print("Caught FileNotFoundError: No such file 'missing.txt'\n")
    print("Testing KeyError...")
    try:
        plants = {"rose": 25, "tulip": 15}
        print(plants["orchid"])
    except KeyError as e:
        print(f"Caught KeyError: {e}\n")
    print("Testing multiple errors together...")
    try:
        int("abc")
        42 / 0
    except (ValueError, ZeroDivisionError):
        print("Caught an error, but program continues!\n")


def test_error_types() -> None:
    print("=== Garden Error Types Demo ===")
    garden_operations()
    print("All error types tested successfully!")
