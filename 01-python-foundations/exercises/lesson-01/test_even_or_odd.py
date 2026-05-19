import pytest
from even_or_odd import (
    check_if_is_even_or_odd,
    convert_user_input_to_int,
    get_user_input,
    main,
    show_result,
)


@pytest.mark.parametrize(
    ("text", "expected"),
    [("4", 4), ("-3", -3), ("0", 0), ("100", 100)],
)
def test_convert_user_input_to_int_parses_valid_integers(text, expected):
    assert convert_user_input_to_int(text) == expected


@pytest.mark.parametrize("text", ["abc", "1.5", ""])
def test_convert_user_input_to_int_rejects_non_integers(text):
    with pytest.raises(ValueError):
        convert_user_input_to_int(text)


@pytest.mark.parametrize(
    ("value", "expected"),
    [(4, True), (7, False), (0, True), (-2, True), (-3, False)],
)
def test_check_if_is_even_or_odd(value, expected):
    assert check_if_is_even_or_odd(value) is expected


def test_get_user_input_returns_entered_string(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _prompt: "42")
    assert get_user_input() == "42"


def test_show_result_prints_even_message(capsys):
    show_result(True)
    assert capsys.readouterr().out.strip() == "The entered number is even."


def test_show_result_prints_odd_message(capsys):
    show_result(False)
    assert capsys.readouterr().out.strip() == "The entered number is odd."


def test_main_reports_even(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _prompt: "8")
    main()
    assert "even" in capsys.readouterr().out


def test_main_reports_odd(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _prompt: "7")
    main()
    assert "odd" in capsys.readouterr().out
