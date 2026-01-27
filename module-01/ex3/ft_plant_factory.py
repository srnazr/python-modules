class Plant:
    def __init__(self, name: str, height: int, age: int):
        self.name = name
        self.height = height
        self.age = age

    def __str__(self) -> str:
        return f"{self.name} ({self.height}cm, {self.age} days)"

    def create_plants(info: list[tuple[str, int, int]]) -> list["Plant"]:
        plants = []
        for name, height, age in info:
            plants.append(Plant(name, height, age))
        return plants


def main():
    plant_info = [
        ("Rose", 25, 30),
        ("Oak", 200, 365),
        ("Cactus", 5, 90),
        ("Sunflower", 80, 45),
        ("Fern", 15, 120),
    ]
    plants = Plant.create_plants(plant_info)
    print("=== Plant Factory Output ===")
    for p in plants:
        print(f"Created: {p}")
    print("Object-Oriented Garden Systems")
    print(f"\nTotal plants created: {len(plants)}")


if __name__ == "__main__":
    main()
