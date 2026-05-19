# Tests for lesson-01 exercises — Design

## Goal

Add automated tests that validate the lesson-01 exercises produce correct
results. The exercises are:

- `01-python-foundations/exercises/lesson-01/even_or_odd.py`
- `01-python-foundations/exercises/lesson-01/temperature_converter.py`

## Problem

Both exercise files end with a bare `main()` call at module level. Importing
either file immediately triggers an `input()` prompt, which blocks any test
that tries to `import` the functions under test.

## Decisions

- **Importability:** wrap the `main()` call in an `if __name__ == "__main__":`
  guard. This is the only change to the exercise logic.
- **Framework:** `pytest`.
- **Test location:** alongside the exercises, inside
  `01-python-foundations/exercises/lesson-01/`.
- **Coverage:** pure logic functions *and* I/O functions (`input` wrappers,
  `show_result`, `main`), the latter via `monkeypatch` and `capsys`.
- **Dependency declaration:** a new `requirements-dev.txt` with a pinned
  `pytest`; setup documented in `CONTRIBUTING.md`.

`temperature_converter.py` is already internally consistent (`user_input()`
returns the raw `str`, `main()` converts it), so no logic cleanup is needed.

## Changes

### 1. Make exercises importable

In both `even_or_odd.py` and `temperature_converter.py`, replace the trailing:

```python
main()
```

with:

```python
if __name__ == "__main__":
    main()
```

Running `python <file>.py` still works; importing the module no longer runs
`main()`.

### 2. Test files

Two pytest files in `01-python-foundations/exercises/lesson-01/`.

Test discovery requires no `__init__.py` and no pytest config file: with the
default `prepend` import mode, pytest inserts each test file's directory onto
`sys.path`, so `from even_or_odd import ...` resolves because the test lives in
the same directory as the exercise.

#### `test_even_or_odd.py`

- `convert_user_input_to_int` — parametrized: `"4"→4`, `"-3"→-3`, `"0"→0`;
  invalid input (`"abc"`, `"1.5"`) raises `ValueError`.
- `check_if_is_even_or_odd` — parametrized: `4→True`, `7→False`, `0→True`,
  `-2→True`, `-3→False`.
- `get_user_input` — `monkeypatch` on `input`; asserts it returns the string.
- `show_result` — `capsys`; `True` prints the "even" message, `False` prints
  the "odd" message.
- `main` — `monkeypatch` input + `capsys`: `"8"` prints "even", `"7"` prints
  "odd".

#### `test_temperature_converter.py`

- `celsius_to_fahrenheit` — parametrized with `pytest.approx`: `0→32`,
  `100→212`, `-40→-40`, `37→98.6`.
- `convert_user_input` — `"0"→0.0`, `"37.5"→37.5`, `"-10"→-10.0`; invalid
  input raises `ValueError`.
- `user_input` — `monkeypatch` on `input`; asserts it returns the raw string.
- `main` — `monkeypatch` input + `capsys`: `"100"` prints `212.0 F`, `"0"`
  prints `32.0 F`.

### 3. Dev dependency

- New `requirements-dev.txt` containing a pinned `pytest`.
- `CONTRIBUTING.md` gets a short "Testes" section: install with
  `uv pip install -r requirements-dev.txt`, run with `pytest` from the repo
  root.

## Out of scope

- Any change to exercise logic beyond the `if __name__` guard.
- Test infrastructure for future lessons (added when those lessons exist).
- A pytest configuration file (not needed for discovery).

## Success criteria

- `pytest` run from the repo root discovers and passes all lesson-01 tests.
- `python even_or_odd.py` and `python temperature_converter.py` still run
  interactively.
- `pre-commit run --all-files` passes on the new and modified files.
