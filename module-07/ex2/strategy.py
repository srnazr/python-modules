from abc import ABC, abstractmethod
from ex0.creature import Creature
from ex1.capability import HealCapability
from ex1.capability import TransformCapability
from .exception import InvalidStrategyError


class BattleStrategy(ABC):
    strategy_name = "battle"

    @abstractmethod
    def is_valid(self, creature):
        pass

    @abstractmethod
    def act(self, creature):
        pass

    def check_valid(self, creature):
        if not self.is_valid(creature):
            message = (f"Invalid Creature '{creature._name}' for this"
                       f"{self.strategy_name} strategy")
            raise InvalidStrategyError(message)


class NormalStrategy(BattleStrategy):
    strategy_name = "normal"

    def is_valid(self, creature):
        if isinstance(creature, Creature):
            return True
        return False

    def act(self, creature):
        self.check_valid(creature)
        print(creature.attack())


class AggressiveStrategy(BattleStrategy):

    strategy_name = "agressive"

    def is_valid(self, creature):
        if isinstance(creature, TransformCapability):
            return True
        return False

    def act(self, creature):
        self.check_valid(creature)
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())


class DefensiveStrategy(BattleStrategy):

    strategy_name = "defensive"

    def is_valid(self, creature):
        if isinstance(creature, HealCapability):
            return True
        return False

    def act(self, creature):
        self.check_valid(creature)
        print(creature.attack())
        print(creature.heal())
