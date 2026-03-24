class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error"):
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error"):
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message: str = "Unknown water error"):
        super().__init__(message)


def check_plant(plant: str) -> None:
    raise PlantError(f"The {plant} plant is wilting!")


def check_water(liters: int) -> None:
    if liters < 10:
        raise WaterError("Not enough water in the tank!")


def test_custom_errors() -> None:
    print("=== Custom Garden Errors Demo ===")

    print("Testing PlantError...")
    try:
        check_plant("tomato")
    except PlantError as e:
        print(f"Caught PlantError: {e}")

    print("Testing WaterError...")
    try:
        check_water(2)
    except WaterError as e:
        print(f"Caught WaterError: {e}")

    print("Testing catching all garden errors...")
    for action in [lambda: check_plant("tomato"), lambda: check_water(2)]:
        try:
            action()
        except GardenError as e:
            print(f"Caught GardenError: {e}")

    print("All custom error types work correctly!")
