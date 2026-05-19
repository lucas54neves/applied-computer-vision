def reversing_a_string(text: str) -> str:
    return text[::-1]


def main():
    string_to_reverse = input("What do you want to reverse? ")
    reverted_string = reversing_a_string(string_to_reverse)
    print(f"string = {string_to_reverse} | reverted string = {reverted_string}")


if __name__ == "__main__":
    main()
