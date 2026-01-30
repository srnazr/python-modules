class GardenError(Exception):
    """ Base error for garden problems."""


class PlantError(GardenError):
    """Raised for problems with plants."""


class WaterError(GardenError):
    """Raised for problems with watering."""


class GardenManager:
    def __init__(self):
        self.plants = {}
        self.water_tank = 20
        self.system_open = False

    def add_plant(self, name, water_level, sunlight_hours):
        self._validate_plant_inputs(name, water_level, sunlight_hours)
        if name in self.plants:
            raise PlantError(f"Plant '{name}' already exists!")
        self.plants[name] = {
            "water": water_level,
            "sun": sunlight_hours
        }

    def water_plant(self, name, amount):
        self._validate_watering(name, amount)
        self._open_watering_system()
        try:
            self._ensure_water_available(amount)
            self.water_tank -= amount
            self.plants[name]["water"] += amount
        finally:
            self._close_watering_system()

    def check_plant_health(self, name):
        self._validate_plant_exists(name)
        water = self.plants[name]["water"]
        sun = self.plants[name]["sun"]
        self._validate_ranges(water, sun)
        return f"{name}: healthy (water: {water}, sun: {sun})"

    def _validate_plant_inputs(self, name, water_level, sunlight_hours):
        if not isinstance(name, str) or name.strip() == "":
            raise PlantError("Plant name cannot be empty!")
        if not isinstance(water_level, int):
            raise PlantError("Water level must be an integer!")
        if not isinstance(sunlight_hours, int):
            raise PlantError("Sunlight hours must be an integer!")
        self._validate_ranges(water_level, sunlight_hours)

    def _validate_ranges(self, water_level, sunlight_hours):
        if water_level < 1:
            raise PlantError(f"Water level {water_level} is too low (min 1)")
        if water_level > 10:
            raise PlantError(f"Water level {water_level} is too high (max 10)")
        if sunlight_hours < 2:
            raise PlantError(
                f"Sunlight hours {sunlight_hours} is too low (min 2)"
            )
        if sunlight_hours > 12:
            raise PlantError(
                f"Sunlight hours {sunlight_hours} is too high (max 12)"
            )

    def _validate_plant_exists(self, name):
        if name not in self.plants:
            raise PlantError(f"Unknown plant '{name}'")

    def _validate_watering(self, name, amount):
        self._validate_plant_exists(name)
        if not isinstance(amount, int):
            raise WaterError("Water amount must be an integer!")
        if amount <= 0:
            raise WaterError("Water amount must be positive!")

    def _ensure_water_available(self, amount):
        if self.water_tank < amount:
            raise WaterError("Not enough water in tank")

    def _open_watering_system(self):
        self.system_open = True

    def _close_watering_system(self):
        self.system_open = False


def test_garden_management():
    manager = GardenManager()
    print("=== Garden Management System ===")

    print("Adding plants to garden...")
    try:
        manager.add_plant("tomato", 5, 8)
        print("Added tomato successfully")
    except GardenError as e:
        print(f"Error adding plant: {e}")

    try:
        manager.add_plant("lettuce", 15, 6)
        print("Added lettuce successfully")
    except GardenError as e:
        print(f"Error adding plant: {e}")

    try:
        manager.add_plant("", 3, 6)
        print("Added empty-name plant successfully")
    except GardenError as e:
        print(f"Error adding plant: {e}")

    manager.plants["lettuce"] = {"water": 15, "sun": 6}

    print("Watering plants...")
    print("Opening watering system")
    try:
        manager.water_plant("tomato", 2)
        print("Watering tomato- success")
    except GardenError as e:
        print(f"Error watering tomato: {e}")
    finally:
        print("Closing watering system (cleanup)")

    print("Opening watering system")
    try:
        manager.water_plant("lettuce", 2)
        print("Watering lettuce- success")
    except GardenError as e:
        print(f"Error watering lettuce: {e}")
    finally:
        print("Closing watering system (cleanup)")

    print("Checking plant health...")
    try:
        print(manager.check_plant_health("tomato"))
    except GardenError as e:
        print(f"Error checking tomato: {e}")

    try:
        print(manager.check_plant_health("lettuce"))
    except GardenError as e:
        print(f"Error checking lettuce: {e}")

    print("Testing error recovery...")
    manager.water_tank = 0
    try:
        manager.water_plant("tomato", 5)
        print("Watering tomato- success")
    except GardenError as e:
        print(f"Caught GardenError: {e}")
        print("System recovered and continuing...")

    try:
        print(manager.check_plant_health("tomato"))
    except GardenError as e:
        print(f"Error checking tomato: {e}")

    print("Garden management system test complete!")


if __name__ == "__main__":
    test_garden_management()
