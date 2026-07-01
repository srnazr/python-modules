import math

def ft_get_player_coord() -> tuple[float, float, float]:
    while True:
        coords = input("Enter new coordinates as floats in format 'x,y,z': ")
        sep  = coords.split(",")
        if len(sep) != 3:
            print("Invalid syntax")
            continue
        try:
            x = float(sep[0])
            y = float(sep[1])
            z = float(sep[2])
            return (x, y, z)
        except ValueError as e:
            param = str(e).split("'")[1]
            print(f"Error on parameter '{param}': {e}")

def main() -> None:
    print("=== Game Coordinate System ===")

    print("Get a first set of coordinates")
    pos1 = ft_get_player_coord()
    print(f"Got a first tuple: {pos1}")
    print(f"It includes: X={pos1[0]}, Y={pos1[1]}, Z={pos1[2]}")

    dist_center = math.sqrt(pos1[0] ** 2 + pos1[1] ** 2 + pos1[2] ** 2)
    print(f"Distance to center: {round(dist_center, 4)}")

    print("Get a second set of coordinates")
    pos2 = ft_get_player_coord()

    dist = math.sqrt(
        (pos2[0] - pos1[0]) ** 2
        + (pos2[1] - pos1[1]) ** 2
        + (pos2[2] - pos1[2]) ** 2
    )
    print(f"Distance between the 2 sets of coordinates: {round(dist, 4)}")


if __name__ == "__main__":
    main()