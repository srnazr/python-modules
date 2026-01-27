class Plant:
    def __init__(self, name: str, height: int, age: int):
        self.name = name
        self.height = height
        self.age = age


def main():
    plants = [Plant("Rose", 20, 25),
              Plant("Orchid", 30, 256),
              Plant("Lily", 25, 120)]
    print("=== Garden Plant Registry ===")
    for i in range(3):
        p = plants[i]
        print(f"{p.name}: {p.height}cm, {p.age} days old")


if __name__ == "__main__":
    main()
