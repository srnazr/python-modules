from .dark_spellbook import dark_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    allowed = dark_spell_allowed_ingredients()
    lowered = ingredients.lower()
    is_valid = False
    for item in allowed:
        if item in lowered:
            is_valid = True
    if is_valid:
        return (f"{ingredients}- VALID")
    return (f"{ingredients}- INVALID")