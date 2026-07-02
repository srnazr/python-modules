import random


PLAYERS = ['Alice', 'bob', 'Charlie', 'dylan', 'Emma', 'Gregory', 'john', 'kevin', 'Liam']


def main() -> None:
    print("=== Game Data Alchemist ===")

    print(f"Initial list of players: {PLAYERS}")

    all_capitalized = [name.capitalize() for name in PLAYERS]
    print(f"New list with all names capitalized: {all_capitalized}")

    only_capitalized = [name for name in PLAYERS if name[0].isupper()]
    print(f"New list of capitalized names only: {only_capitalized}")

    scores = {name: random.randint(50, 999) for name in all_capitalized}
    print(f"Score dict: {scores}")

    average = round(sum(scores.values()) / len(scores), 2)
    print(f"Score average is {average}")

    high_scores = {name: score for name, score in scores.items() if score > average}
    print(f"High scores: {high_scores}")


if __name__ == "__main__":
    main()