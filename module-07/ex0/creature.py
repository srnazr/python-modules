import typing
from abc import ABC, abstractmethod


class Creature(ABC):

    def __init__(self, name: str, type: str) -> None:
        self._name = name
        self._type = type

    @abstractmethod
    def attack() -> str:
        pass

    def describe(self) -> str:
        return(f"{self._name} is a {self._type} type Creature")


class Flameling(Creature):
    def attack() -> str:
        return