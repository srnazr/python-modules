def water_plants(plant_list):
    print("Opening watering system")
    try:
        for plant in plant_list:
            if not isinstance(plant, str):
                raise ValueError(f"Cannot water {plant} - invalid plant!")
            print(f"Watering {plant}")
    except ValueError as e:
        print(f"Error: {e}")
        raise
    finally:
        print("Closing watering system (cleanup)")


def test_watering_system():
    print("=== Garden Watering System ===\n")

    print("Testing normal watering...")
    try:
        water_plants(["tomato", "lettuce", "carrots"])
        print("Watering completed successfully!\n")
    except Exception:
        pass

    print("Testing with error...")
    try:
        water_plants(["tomato", None, "carrots"])
    except Exception:
        print("\nCleanup always happens, even with errors!")


if __name__ == "__main__":
    test_watering_system()
