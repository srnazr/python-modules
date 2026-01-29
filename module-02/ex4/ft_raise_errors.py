def check_plant_health(plant_name, water_level, sun_hours):
    if not plant_name:
        raise ValueError("Plant name cannot be empty!\n")

    if water_level < 1:
        raise ValueError(f"Water level {water_level} is too low (min 1)\n")
    if water_level > 10:
        raise ValueError(f"Water level {water_level} is too high (max 10)\n")

    if sun_hours < 2:
        raise ValueError(f"Sunlight hours {sun_hours} is too low (min 2)\n")
    if sun_hours > 12:
        raise ValueError(f"Sunlight hours {sun_hours} is too high (max 12)\n")

    return f"Plant '{plant_name}' is healthy!\n"


def test_plant_checks():
    print("=== Garden Plant Health Checker ===\n")

    print("Testing good values...")
    try:
        result = check_plant_health("tomato", 5, 6)
        print(result)
    except ValueError as e:
        print(f"Error: {e}")

    print("Testing empty plant name...")
    try:
        check_plant_health("", 5, 6)
    except ValueError as e:
        print(f"Error: {e}")

    print("Testing bad water level...")
    try:
        check_plant_health("tomato", 15, 6)
    except ValueError as e:
        print(f"Error: {e}")

    print("Testing bad sunlight hours...")
    try:
        check_plant_health("tomato", 5, 0)
    except ValueError as e:
        print(f"Error: {e}")

    print("All error raising tests completed!")


if __name__ == "__main__":
    test_plant_checks()
