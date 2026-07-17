from ex0.creature import Creature
from .capability import HealCapability
from .capability import TransformCapability


class Sproutling(Creature, HealCapability):

    def __init__(self) -> None:
        Creature.__init__(self, "Sproutling", "Grass")

    def attack(self) -> str:
        return (f"{self._name} uses Vine Whip!")

    def heal(self, target=None) -> str:
        return (f"{self._name} heals itself for a small amount")


class Bloomelle(Creature, HealCapability):

    def __init__(self) -> None:
        Creature.__init__(self, "Bloomelle", "Grass/Fairy")

    def attack(self) -> str:
        return (f"{self._name} uses Petal Dance!")

    def heal(self, target=None) -> str:
        return (f"{self._name} heals itself and others for a large amount")


class Shiftling(Creature, TransformCapability):

    def __init__(self) -> None:
        Creature.__init__(self, "Shiftling", "Normal")
        TransformCapability.__init__(self)

    def attack(self) -> str:
        if self.is_transformed:
            return (f"{self._name} performs a boosted strike!")
        else:
            return (f"{self._name} attacks normally.")

    def transform(self) -> str:
        self.is_transformed = True
        return (f"{self._name} shifts into a sharper form!")

    def revert(self) -> str:
        self.is_transformed = False
        return (f"{self._name} returns to normal.")


class Morphagon(Creature, TransformCapability):

    def __init__(self) -> None:
        Creature.__init__(self, "Morphagon", "Normal/Dragon")
        TransformCapability.__init__(self)

    def attack(self) -> str:
        if self.is_transformed:
            return (f"{self._name} unleashes a devastating morph strike!")
        else:
            return (f"{self._name} attacks normally.")

    def transform(self) -> str:
        self.is_transformed = True
        return (f"{self._name} morphs into a dragonic battle form!")

    def revert(self) -> str:
        self.is_transformed = False
        return (f"{self._name} stabilizes its form.")
