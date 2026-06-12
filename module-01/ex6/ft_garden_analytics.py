class Plant:
    class _Stats:
        def __init__(self):
            self.grow_calls = 0
            self.age_calls = 0
            self.show_calls = 0

        def display(self):
            print(f"Stats: {self.grow_calls} grow, "
                  f"{self.age_calls} age, {self.show_calls} show")

    def __init__(self, name, height, age):
        self.name = name
        self.height = float(height)
        self.age = int(age)
        self._stats = Plant._Stats()

    @staticmethod
    def is_older_than_a_year(days):
        return days > 365

    @classmethod
    def create_anonymous(cls):
        return cls("Unknown plant", 0.0, 0)

    def grow(self, amount):
        self.height += amount
        self._stats.grow_calls += 1

    def age_plant(self, days):
        self.age += days
        self._stats.age_calls += 1

    def show(self):
        print(f"{self.name}: {self.height}cm, {self.age} days old")
        self._stats.show_calls += 1

    def display_stats(self):
        self._stats.display()


class Flower(Plant):
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age)
        self.color = color
        self.bloomed = False

    def bloom(self):
        self.bloomed = True

    def show(self):
        super().show()
        print(f"Color: {self.color}")
        if self.bloomed:
            print(f"{self.name} is blooming beautifully!")
        else:
            print(f"{self.name} has not bloomed yet")


class Tree(Plant):
    class _TreeStats(Plant._Stats):
        def __init__(self):
            super().__init__()
            self.shade_calls = 0

        def display(self):
            super().display()
            print(f"{self.shade_calls} shade")

    def __init__(self, name, height, age, trunk_diameter):
        super().__init__(name, height, age)
        self.trunk_diameter = float(trunk_diameter)
        self._stats = Tree._TreeStats()

    def produce_shade(self):
        print(f"Tree {self.name} now produces a shade of {self.height}cm long "
              f"and {self.trunk_diameter}cm wide.")
        self._stats.shade_calls += 1

    def show(self):
        super().show()
        print(f"Trunk diameter: {self.trunk_diameter}cm")


class Seed(Flower):
    def __init__(self, name, height, age, color, seeds=0):
        super().__init__(name, height, age, color)
        self.seeds = seeds

    def show(self):
        super().show()
        print(f"Seeds: {self.seeds}")


def display_statistics(plant):
    print(f"[statistics for {plant.name}]")
    plant.display_stats()


if __name__ == "__main__":
    print("=== Garden statistics ===")

    print("=== Check year-old")
    print(f"Is 30 days more than a year?-> {Plant.is_older_than_a_year(30)}")
    print(f"Is 400 days more than a year?-> {Plant.is_older_than_a_year(400)}")

    print()
    print("=== Flower")
    rose = Flower("Rose", 15.0, 10, "red")
    rose.show()
    display_statistics(rose)

    print("[asking the rose to grow and bloom]")
    rose.grow(8)
    rose.bloom()
    rose.show()
    display_statistics(rose)

    print()
    print("=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    display_statistics(oak)

    print("[asking the oak to produce shade]")
    oak.produce_shade()
    display_statistics(oak)

    print()
    print("=== Seed")
    sunflower = Seed("Sunflower", 80.0, 45, "yellow", 0)
    sunflower.show()

    print("[make sunflower grow, age and bloom]")
    sunflower.grow(30)
    sunflower.age_plant(20)
    sunflower.bloom()
    sunflower.seeds = 42
    sunflower.show()
    display_statistics(sunflower)

    print()
    print("=== Anonymous")
    anon = Plant.create_anonymous()
    anon.show()
    display_statistics(anon)
