def check_temperature(temp_str: str) -> None:
    print(f"Testing temperature: {temp_str}")
    try:
        temperature = int(temp_str)
    except (ValueError, TypeError):
        print(f"Error: '{temp_str}' is not a valid number\n")
        return
    if temperature < 0:
        print(f"Error: {temperature}°C is too cold for plans (min 0°C)\n")
    elif temperature > 40:
        print(f"Error: {temperature}°C is too hot for plants (max 40°C)\n")
    else:
        print(f"Temperature {temperature}°C is perfect for plants!\n")
