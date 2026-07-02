import random


ACHIEVEMENTS = [
    "First Steps", "Boss Slayer", "World Savior", "Master Explorer",
    "Speed Runner", "Untouchable", "Collector Supreme", "Crafting Genius",
    "Survivor", "Unstoppable", "Strategist", "Treasure Hunter",
    "Sharp Mind", "Hidden Path Finder", "Dragon Slayer", "Legendary",
    "Pacifist", "Night Owl", "completionist", "Iron Will"
]


def gen_player_achievements() -> set:
    count = random.randint(5, 12)
    return set(random.sample(ACHIEVEMENTS, count))


def main() -> None:
    print("=== Achievement Tracker System ===")

    players = {"Alice": gen_player_achievements(),
               "Bob": gen_player_achievements(),
               "Charlie": gen_player_achievements(),
               "Dylan": gen_player_achievements()}

    for name, achievements in players.items():
        print(f"Player {name}: {achievements}")

    all_achievements = set().union(*players.values())
    print(f"\nAll distinct achievements: {all_achievements}")
    print()

    common = set.intersection(*players.values())
    print(f"Common achievements: {common}")
    print()

    for name, achievements in players.items():
        others = set.union(*[a for n, a in players.items() if n != name])
        unique = achievements.difference(others)
        print(f"Only {name} has: {unique}")
    print()

    for name, achievements in players.items():
        missing = all_achievements.difference(achievements)
        print(f"{name} is missing: {missing}")


if __name__ == "__main__":
    main()