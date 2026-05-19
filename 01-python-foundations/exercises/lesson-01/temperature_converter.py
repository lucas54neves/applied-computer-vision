def celsius_to_fahrenheit(celsius: float) -> float:
    return celsius * 1.8 + 32


def convert_user_input(user_input: str) -> float:
    return float(user_input)


def user_input() -> str:
    return input("Insert a temperature in Celsius to convert to Fahrenheit: ")


def main():
    user_input_as_str = user_input()
    user_input_as_float = convert_user_input(user_input_as_str)
    temperature_as_fahrenheit = celsius_to_fahrenheit(user_input_as_float)
    print(f"Temperature in Fahrenheit: {temperature_as_fahrenheit} F")


if __name__ == "__main__":
    main()
