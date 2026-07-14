import elements
import alchemy.potions
from ..elements import create_air


def lead_to_gold() -> str:
    air = create_air()
    fire = elements.create_fire()
    strength = alchemy.potions.strength_potion()
    return (f"Recipe trasmuting Lead to Gold: brew '{air}' and "
            f"'{strength}' mixed with '{fire}'")
