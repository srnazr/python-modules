class Plant:
    def __init__(self, name: str, height: float, age: int):
        self.name = name
        self.height = height
        self.age = age

    def grow(self, cm: float) -> None:
        self.height += cm

    def age_p(self, days: int) -> None:
        self.age += days

    def get_info(self):
        print(f"{self.name}: {self.height:.1f}cm, {self.age} days old")


def main():
    rose = Plant("Rose", 25.0, 30)
    initial_height = rose.height
    print("=== Garden Plant Growth ===")
    rose.get_info()
    for i in range(7):
        print(f"=== Day {i+1} ===")
        rose.grow(0.8)
        rose.age_p(1)
        rose.get_info()
    growth = rose.height - initial_height
    print(f"Growth this week: {growth:.1f}cm")


if __name__ == "__main__":
    main()
