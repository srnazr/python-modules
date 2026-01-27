class Plant:
    def __init__(self, name: str, height: int, age: int):
        self.name = name
        self.height = height
        self.age = age

    def grow(self, cm: int) -> None:
        self.height += cm

    def age_p(self, days: int) -> None:
        self.age += 1

    def get_info(self):
        print(f"{self.name}: {self.height}cm, {self.age} days old")


def main():
    i = 0
    orchid = Plant("Orchid", 1, 10)
    initial_height = orchid.height
    print("=== Day 1 ===")
    orchid.get_info()
    for i in range(6):
        orchid.grow(1)
        orchid.age_p(1)
    print(f"=== Day {i + 1} ===")
    orchid.get_info()
    growth = orchid.height - initial_height
    print(f"Growth this week: +{growth}cm")


if __name__ == "__main__":
    main()
