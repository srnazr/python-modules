import ex0


def main():
    print("Testing factory")
    flameling = ex0.FlameFactory().create_base()
    print(flameling.describe())
    print(flameling.attack())
    pyrodon = ex0.FlameFactory().create_evolved()
    print(pyrodon.describe())
    print(pyrodon.attack())

    print("\nTesting factory")
    aquabub = ex0.AquaFactory().create_base()
    print(aquabub.describe())
    print(aquabub.attack())
    torragon = ex0.AquaFactory().create_evolved()
    print(torragon.describe())
    print(torragon.attack())

    print("\nTesting battle")
    print(flameling.describe())
    print("   vs.")
    print(aquabub.describe())
    print("   fight!")
    print(flameling.attack())
    print(aquabub.attack())


if __name__ == "__main__":
    main()
