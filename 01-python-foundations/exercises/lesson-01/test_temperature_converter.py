import pytest
from temperature_converter import (
    celsius_to_fahrenheit,
    convert_user_input,
    main,
    user_input,
)


@pytest.mark.parametrize(
    ("celsius", "expected"),
    [(0, 32), (100, 212), (-40, -40), (37, 98.6)],
)
def test_celsius_to_fahrenheit(celsius, expected):
    assert celsius_to_fahrenheit(celsius) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("text", "expected"),
    [("0", 0.0), ("37.5", 37.5), ("-10", -10.0)],
)
def test_convert_user_input_parses_valid_numbers(text, expected):
    assert convert_user_input(text) == pytest.approx(expected)


@pytest.mark.parametrize("text", ["abc", ""])
def test_convert_user_input_rejects_non_numbers(text):
    with pytest.raises(ValueError):
        convert_user_input(text)


def test_user_input_returns_raw_string(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _prompt: "37.5")
    assert user_input() == "37.5"


def test_main_reports_boiling_point(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _prompt: "100")
    main()
    assert "212.0 F" in capsys.readouterr().out


def test_main_reports_freezing_point(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _prompt: "0")
    main()
    assert "32.0 F" in capsys.readouterr().out
