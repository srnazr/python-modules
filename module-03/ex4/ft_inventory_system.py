import sys


def ft_get_inventory(args: list) -> dict:
    inventory = {}
    for param in args:
        if ":" not in param or param.count(":") != 1:
            print(f"Error - invalid parameter '{param}'")
            continue
        name, quantity = param.split(":")
        if name in inventory:
            print(f"Redundant item '{name}' - discarding")
            continue
        try:
            inventory[name] = int(quantity)
        except ValueError as e:
            print(f"Quantity error for '{name}': {e}")
    return inventory


def main() -> None:
    print("=== Inventory System Analysis ===")

    inventory = ft_get_inventory(sys.argv[1:])

    if not inventory:
        print("Inventory is empty!")
        return

    print(f"Got inventory: {inventory}")

    items = list(dict.keys(inventory))
    print(f"Item list: {items}")

    total = sum(dict.values(inventory))
    print(f"Total quantity of the {len(items)} items: {total}")

    for item, quantity in inventory.items():
        percentage = round(quantity / total * 100, 1)
        print(f"Item {item} represents {percentage}%")

    most = max(inventory, key=inventory.get)
    least = min(inventory, key=inventory.get)

    print(f"Item most abundant: {most} with quantity {inventory[most]}")
    print(f"Item least abundant: {least} with quantity {inventory[least]}")

    dict.update(inventory, {"magic_item": 1})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()