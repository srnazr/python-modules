from ex1 import HealingCreatureFactory
from ex1 import TransformCreatureFactory


def test_healing(factory):
    print("Testing Creature with healing capability")
    print("   base:")
    base_creature = factory.create_base()
    print(base_creature.describe())
    print(base_creature.attack())
    print(base_creature.heal())
    print("   evolved:")
    evolved_creature = factory.create_evolved()
    print(evolved_creature.describe())
    print(evolved_creature.attack())
    print(evolved_creature.heal())


def test_transform(factory):
    print("\nTesting Creature with transform capability")
    print("   base:")
    base_creature = factory.create_base()
    print(base_creature.describe())
    print(base_creature.attack())
    print(base_creature.transform())
    print(base_creature.attack())
    print(base_creature.revert())
    print("   evolved:")
    evolved_creature = factory.create_evolved()
    print(evolved_creature.describe())
    print(evolved_creature.attack())
    print(evolved_creature.transform())
    print(evolved_creature.attack())
    print(evolved_creature.revert())


def main():
    healing_factory = HealingCreatureFactory()
    test_healing(healing_factory)

    transform_factory = TransformCreatureFactory()
    test_transform(transform_factory)


if __name__ == "__main__":
    main()
