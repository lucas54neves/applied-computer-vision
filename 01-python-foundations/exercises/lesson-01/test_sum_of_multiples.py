import pytest
from sum_of_multiples import (
    if_it_is_a_multiple_of_3,
    if_it_is_a_multiple_of_5,
    main,
    sum_of_multiples,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [(3, True), (6, True), (9, True), (1, False), (5, False), (10, False)],
)
def test_if_it_is_a_multiple_of_3(value, expected):
    assert if_it_is_a_multiple_of_3(value) is expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [(5, True), (10, True), (15, True), (1, False), (3, False), (7, False)],
)
def test_if_it_is_a_multiple_of_5(value, expected):
    assert if_it_is_a_multiple_of_5(value) is expected


def test_sum_of_multiples():
    assert sum_of_multiples() == 233168


def test_main_prints_expected_sum(capsys):
    main()
    out = capsys.readouterr().out
    assert "233168" in out
    assert "multiples of 3 or 5" in out
