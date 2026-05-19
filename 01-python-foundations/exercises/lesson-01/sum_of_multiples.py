S_0 = 1
S_N = 999


def if_it_is_a_multiple_of_3(value) -> bool:
    return value % 3 == 0


def if_it_is_a_multiple_of_5(value) -> bool:
    return value % 5 == 0


def sum_of_multiples() -> int:
    _sum = 0
    for i in range(S_0, S_N + 1, 1):
        if if_it_is_a_multiple_of_3(i) or if_it_is_a_multiple_of_5(i):
            _sum += i
    return _sum


def main():
    _sum = sum_of_multiples()
    print(f"Sum from {S_0} to {S_N} of all multiples of 3 or 5 is {_sum}")


if __name__ == "__main__":
    main()
