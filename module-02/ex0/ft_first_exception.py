def input_temperature(temp: str) -> int:
    return int(temp)


def test_temperature() -> None:
    print("=== Garden Temperature ===")

    for stemp in ["25", "abc"]:
        print(f"Input data is '{stemp}'")
        try:
            temp = input_temperature(stemp)
            print(f"Temperature is now {temp}°C")
        except ValueError as e:
            print(f"Caught input_temperature error: {e}")

    print("All tests completed- program didn't crash!")
