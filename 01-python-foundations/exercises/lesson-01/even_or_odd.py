def get_user_input() -> str:
    return input("Enter a number to check if it is even or odd: ")


def convert_user_input_to_int(user_input: str) -> int:
    return int(user_input)


def check_if_is_even_or_odd(value: int) -> bool:
    return value % 2 == 0


def show_result(is_even: bool) -> None:
    if is_even:
        print("The entered number is even.")
    else:
        print("The entered number is odd.")


def main():
    user_input = get_user_input()
    user_input_as_int = convert_user_input_to_int(user_input)
    is_even = check_if_is_even_or_odd(user_input_as_int)
    show_result(is_even)


main()
