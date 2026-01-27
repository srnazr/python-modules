class SecurePlant:
    def __init__(self):
        self.name = ""
        self.height = 0
        self.age = 0

    def set_name(self, name: str):
        self.name = name
        print(f"Plant created: {self.name}")

    def set_height(self, height: int):
        if height < 0:
            self.print_error("height", height, "cm")
            return
        self.height = height
        print(f"Height updated: {self.height}cm [OK]")

    def set_age(self, age: int):
        if age < 0:
            self.print_error("age", age, "day(s)")
            return
        self.age = age
        print(f"Age updated: {self.age} day(s) [OK]")

    def get_name(self) -> str:
        return self.name

    def get_height(self) -> int:
        return self.height

    def get_age(self) -> int:
        return self.age

    def __str__(self):
        return f"Current plant: {self.name} ({self.height}cm, {self.age}days)"

    def print_error(self, att: str, val: int, unit: str) -> None:
        print(f"\nInvalid operation attempted: {att} {val}{unit} [REJECTED]")
        print(f"Security: Negative {att} rejected\n")


def main():
    print("=== Garden Security System ===")
    rose = SecurePlant()
    rose.set_name("Rose")
    rose.set_height(25)
    rose.set_age(30)

    rose.set_height(-5)

    print(rose.__str__())


if __name__ == "__main__":
    main()
