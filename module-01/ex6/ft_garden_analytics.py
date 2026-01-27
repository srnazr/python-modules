class Plant:
    def __init__(self, name: str, height: int, age: int):
        self.name = name
        self.height = height
        self.age = age

    def grow(self, cm: int) -> int:
        self.height += cm
        print(f"{self.name} grew {cm}cm")
        return cm

    def __str__(self) -> str:
        return f"- {self.name}: {self.height}cm"


class FloweringPlant(Plant):
    def __init__(self, name: str, height: int, age: int, color: str):
        super().__init__(name, height, age)
        self.color = color
        self.blooming = True

    def __str__(self) -> str:
        if self.blooming:
            state = " (blooming)"
        else:
            state = ""
        return f"- {self.name}: {self.height}cm, {self.color} flowers{state}"


class PrizeFlower(FloweringPlant):
    def __init__(
        self,
        name: str,
        height: int,
        age: int,
        color: str,
        prize_points: int,
    ):
        super().__init__(name, height, age, color)
        self.prize_points = prize_points

    def __str__(self) -> str:
        if self.blooming:
            state = " (blooming)"
        else:
            state = ""
        return (
            f"- {self.name}: {self.height}cm, {self.color} flowers{state}, "
            f"Prize points: {self.prize_points}"
        )


class Garden:
    def __init__(self, owner: str):
        self.owner = owner
        self.plants = []
        self.plants_added = 0
        self.total_growth = 0

    def add_plant(self, plant: Plant) -> None:
        self.plants.append(plant)
        self.plants_added += 1
        print(f"Added {plant.name} to {self.owner}'s garden")

    def grow_all(self) -> None:
        print(f"\n{self.owner} is helping all plants grow...")
        for plant in self.plants:
            self.total_growth += plant.grow(1)

    def report(self, stats_helper) -> None:
        print(f"\n=== {self.owner}'s Garden Report ===")
        print("Plants in garden:")
        for plant in self.plants:
            print(str(plant))

        counts = stats_helper.count_types(self.plants)
        print(
            f"\nPlants added: {self.plants_added}, "
            f"Total growth: {self.total_growth}cm"
        )
        print(
            "Plant types: "
            f"{counts['regular']} regular, "
            f"{counts['flowering']} flowering, "
            f"{counts['prize']} prize flowers"
        )


class GardenManager:
    class GardenStats:
        @staticmethod
        def count_types(plants) -> dict:
            regular = 0
            flowering = 0
            prize = 0
            for p in plants:
                if isinstance(p, PrizeFlower):
                    prize += 1
                elif isinstance(p, FloweringPlant):
                    flowering += 1
                else:
                    regular += 1
            return {"regular": regular, "flowering": flowering, "prize": prize}

        @staticmethod
        def score_garden(garden: Garden) -> int:
            score = 0
            for p in garden.plants:
                score += p.height
                if isinstance(p, PrizeFlower):
                    score += p.prize_points
                elif isinstance(p, FloweringPlant):
                    score += 5
            score += garden.total_growth
            return score

    def __init__(self):
        self.gardens = {}
        self.stats = GardenManager.GardenStats()

    def get_garden(self, owner: str) -> Garden:
        if owner not in self.gardens:
            self.gardens[owner] = Garden(owner)
        return self.gardens[owner]

    def add_plant_to_garden(self, owner: str, plant: Plant) -> None:
        self.get_garden(owner).add_plant(plant)

    @classmethod
    def create_garden_network(cls):
        manager = cls()
        manager.get_garden("Alice")
        manager.get_garden("Bob")
        return manager

    @staticmethod
    def validate_heights(plants) -> bool:
        for p in plants:
            if p.height < 0:
                return False
        return True

    def total_gardens(self) -> int:
        return len(self.gardens)

    def print_scores(self) -> None:
        print("Garden scores")
        for owner in self.gardens:
            g = self.gardens[owner]
            score = self.stats.score_garden(g)
            print(f"- {owner}: {score}")


def main() -> None:
    print("=== Garden Management System Demo ===\n")

    manager = GardenManager.create_garden_network()

    manager.add_plant_to_garden("Alice", Plant("Oak Tree", 100, 500))
    manager.add_plant_to_garden("Alice", FloweringPlant("Rose", 25, 30, "red"))
    manager.add_plant_to_garden(
        "Alice",
        PrizeFlower("Sunflower", 50, 45, "yellow", 10),
    )

    alice = manager.get_garden("Alice")
    alice.grow_all()
    alice.report(manager.stats)

    ok = GardenManager.validate_heights(alice.plants)
    print(f"\nHeight validation test: {ok}")

    bob = manager.get_garden("Bob")
    manager.add_plant_to_garden("Bob", Plant("Basil", 20, 40))
    manager.add_plant_to_garden("Bob", FloweringPlant("Lily", 15, 25, "white"))
    bob.grow_all()

    manager.print_scores()
    print(f"Total gardens managed: {manager.total_gardens()}")


if __name__ == "__main__":
    main()
