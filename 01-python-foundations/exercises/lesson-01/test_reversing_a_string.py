import pytest
from reversing_a_string import main, reversing_a_string


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", ""),
        ("a", "a"),
        ("ab", "ba"),
        ("hello", "olleh"),
        ("racecar", "racecar"),
        ("Python", "nohtyP"),
    ],
)
def test_reversing_a_string(text, expected):
    assert reversing_a_string(text) == expected


def test_main_prints_original_and_reversed(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _prompt: "hello")
    main()
    out = capsys.readouterr().out
    assert "string = hello" in out
    assert "reverted string = olleh" in out


def test_main_handles_single_character(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _prompt: "x")
    main()
    out = capsys.readouterr().out
    assert "string = x" in out
    assert "reverted string = x" in out
