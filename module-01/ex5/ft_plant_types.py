class Plant:
    def __init__(self, name: str, height: int, age: int):
        self.name = name
        self.height = height
        self.age = age


class Flower(Plant):
    def __init__(self, name: str, height: int, age: int, color: str):
        super().__init__(name, height, age)
        self.color = color

    def bloom(self) -> None:
        print(f"{self.name} is blooming beautifully!\n")

    def __str__(self) -> str:
        return (
            f"{self.name} (Flower): {self.height}cm, "
            f"{self.age} days, {self.color} color"
        )


class Tree(Plant):
    def __init__(self, name: str, height: int, age: int, diam: int):
        super().__init__(name, height, age)
        self.trunk_diameter = diam

    def produce_shade(self) -> None:
        shade = self.trunk_diameter * 1.5
        print(
            f"{self.name} provides {shade} square meters of shade\n"
        )

    def __str__(self) -> str:
        return (
            f"{self.name} (Tree): {self.height}cm, "
            f"{self.age} days, {self.trunk_diameter}cm diameter"
        )


class Vegetable(Plant):
    def __init__(
        self,
        name: str,
        height: int,
        age: int,
        harvest_season: str,
        nutritional_value: str,
    ):
        super().__init__(name, height, age)
        self.harvest_season = harvest_season
        self.nutritional_value = nutritional_value

    def __str__(self) -> str:
        return (
            f"{self.name} (Vegetable): {self.height}cm, "
            f"{self.age} days, {self.harvest_season} harvest"
        )

    def describe_nutrition(self) -> None:
        print(
            f"{self.name} is rich in {self.nutritional_value}\n"
        )


def main() -> None:
    print("=== Garden Plant Types ===\n")

    flowers = [
        Flower("Rose", 25, 30, "red"),
        Flower("Tulip", 35, 20, "yellow"),
    ]
    trees = [
        Tree("Oak", 500, 1825, 50),
        Tree("Pine", 650, 2500, 40),
    ]
    vegetables = [
        Vegetable("Tomato", 80, 90, "summer", "vitamin C"),
        Vegetable("Carrot", 30, 70, "spring", "beta-carotene"),
    ]

    for flower in flowers:
        print(flower)
        flower.bloom()

    for tree in trees:
        print(tree)
        tree.produce_shade()

    for vegetable in vegetables:
        print(vegetable)
        vegetable.describe_nutrition()


if __name__ == "__main__":
    main()
