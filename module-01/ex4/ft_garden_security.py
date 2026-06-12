class SecurePlant:
    def __init__(self):
        self._name = ""
        self._height = 15
        self._age = 10

    def set_name(self, name: str):
        self._name = name
        print(f"Plant created: {self._name}: "
              f"{float(self._height)}cm, {self._age} days old")

    def set_height(self, height: int):
        if height < 0:
            print(f"{self._name}: Error, height can't be negative")
            print("Height update rejected")
            return
        self._height = height
        print(f"Height updated: {self._height}cm")

    def set_age(self, age: int):
        if age < 0:
            print(f"{self._name}: Error, age can't be negative")
            print("Age update rejected")
            return
        self._age = age
        print(f"Age updated: {self._age} days")

    def get_name(self) -> str:
        return self._name

    def get_height(self) -> int:
        return self._height

    def get_age(self) -> int:
        return self._age

    def __str__(self):
        return (f"Current state: {self._name}: "
                f"{float(self._height)}cm, {self._age} days old")


def main():
    print("=== Garden Security System ===")
    rose = SecurePlant()
    rose.set_name("Rose")
    rose.set_height(25)
    rose.set_age(30)

    rose.set_height(-5)
    rose.set_age(-3)

    print(rose)


if __name__ == "__main__":
    main()
