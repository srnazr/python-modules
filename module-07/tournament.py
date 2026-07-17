from ex0 import FlameFactory
from ex0 import AquaFactory
from ex1 import HealingCreatureFactory
from ex1 import TransformCreatureFactory
from ex2 import NormalStrategy
from ex2 import AggressiveStrategy
from ex2 import DefensiveStrategy
from ex2 import InvalidStrategyError


def battle(opponents):
    print("*** Tournament ***")
    print(str(len(opponents)) + " opponents involved")
    print()

    fighters = []
    for factory, strategy in opponents:
        creature = factory.create_base()
        fighters.append((creature, strategy))

    index_one = 0
    while index_one < len(fighters):
        index_two = index_one + 1
        while index_two < len(fighters):
            creature_one, strategy_one = fighters[index_one]
            creature_two, strategy_two = fighters[index_two]

            print("* Battle *")
            line = (creature_one.describe() + " vs. " +
                    creature_two.describe() + " now fight!")
            print(line)

            try:
                strategy_one.act(creature_one)
                strategy_two.act(creature_two)
            except InvalidStrategyError as error:
                print("Battle error, aborting tournament: " + str(error))
                return

            print()
            index_two = index_two + 1
        index_one = index_one + 1


def main():
    flame_factory = FlameFactory()
    aqua_factory = AquaFactory()
    healing_factory = HealingCreatureFactory()
    transform_factory = TransformCreatureFactory()

    normal_strategy = NormalStrategy()
    aggressive_strategy = AggressiveStrategy()
    defensive_strategy = DefensiveStrategy()

    print("Tournament 0 (basic)")
    tournament_zero = [
        (flame_factory, normal_strategy),
        (healing_factory, defensive_strategy),
    ]
    battle(tournament_zero)
    print()

    print("Tournament 1 (error)")
    tournament_one = [
        (flame_factory, aggressive_strategy),
        (healing_factory, defensive_strategy),
    ]
    battle(tournament_one)
    print()

    print("Tournament 2 (multiple)")
    tournament_two = [
        (aqua_factory, normal_strategy),
        (healing_factory, defensive_strategy),
        (transform_factory, aggressive_strategy),
    ]
    battle(tournament_two)


if __name__ == "__main__":
    main()
