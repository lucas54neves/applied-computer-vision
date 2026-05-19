# Lesson-01 Exercise Tests Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add pytest tests that validate the lesson-01 exercises (`even_or_odd.py`, `temperature_converter.py`) produce correct results.

**Architecture:** Wrap each exercise's `main()` call in an `if __name__ == "__main__":` guard so the modules can be imported without triggering `input()`. Add one pytest file per exercise, located next to the exercise, covering pure logic functions directly and I/O functions via `monkeypatch`/`capsys`. Declare `pytest` as a dev dependency in a new `requirements-dev.txt`.

**Tech Stack:** Python 3.12, pytest, ruff/pre-commit (already configured).

**Language convention:** Code, identifiers, and commit messages are English (per `CLAUDE.md`). Contributor-facing prose files (`CONTRIBUTING.md`, `requirements-dev.txt` comments) are Portuguese, matching the existing `CONTRIBUTING.md` and `requirements.txt`.

---

### Task 1: Make exercises importable

Both exercise files end with a bare `main()` call, so importing them triggers `input()`. Add the standard `if __name__ == "__main__":` guard to both.

**Files:**
- Modify: `01-python-foundations/exercises/lesson-01/even_or_odd.py`
- Modify: `01-python-foundations/exercises/lesson-01/temperature_converter.py`

- [ ] **Step 1: Add the guard to `even_or_odd.py`**

Replace the trailing call. Find:

```python
    show_result(is_even)


main()
```

Replace with:

```python
    show_result(is_even)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Add the guard to `temperature_converter.py`**

Replace the trailing call. Find:

```python
    print(f"Temperature in Fahrenheit: {temperature_as_fahrenheit} F")


main()
```

Replace with:

```python
    print(f"Temperature in Fahrenheit: {temperature_as_fahrenheit} F")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Verify the modules import without prompting**

Run:

```bash
cd 01-python-foundations/exercises/lesson-01 && python -c "import even_or_odd, temperature_converter; print('imported OK')" && cd -
```

Expected: prints `imported OK` and returns immediately (no input prompt, no hang).

- [ ] **Step 4: Verify the scripts still run interactively**

Run:

```bash
echo "8" | python 01-python-foundations/exercises/lesson-01/even_or_odd.py
echo "100" | python 01-python-foundations/exercises/lesson-01/temperature_converter.py
```

Expected: first prints `The entered number is even.`, second prints `Temperature in Fahrenheit: 212.0 F`.

- [ ] **Step 5: Commit**

```bash
git add 01-python-foundations/exercises/lesson-01/even_or_odd.py 01-python-foundations/exercises/lesson-01/temperature_converter.py
git commit -m "refactor: guard lesson-01 exercise main() calls for importability"
```

---

### Task 2: Test `even_or_odd.py`

Add a pytest file next to the exercise. The exercise is already implemented; these tests **validate** it. Tests are expected to PASS — a failure means the exercise has a bug, which must be reported, not patched over.

No `__init__.py` or pytest config is needed: with pytest's default `prepend` import mode, the test file's directory is added to `sys.path`, so `from even_or_odd import ...` resolves because the test sits in the same directory as the exercise.

**Files:**
- Create: `01-python-foundations/exercises/lesson-01/test_even_or_odd.py`

- [ ] **Step 1: Write the test file**

Create `01-python-foundations/exercises/lesson-01/test_even_or_odd.py`:

```python
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
```

- [ ] **Step 2: Run the tests**

Run:

```bash
python -m pytest 01-python-foundations/exercises/lesson-01/test_even_or_odd.py -v
```

Expected: all 17 collected tests PASS. If any test fails, the exercise has a real bug — stop and report it instead of changing the test.

- [ ] **Step 3: Commit**

```bash
git add 01-python-foundations/exercises/lesson-01/test_even_or_odd.py
git commit -m "test: validate lesson-01 even or odd exercise"
```

---

### Task 3: Test `temperature_converter.py`

Same approach as Task 2, for the temperature converter exercise. Floating-point results are compared with `pytest.approx`.

**Files:**
- Create: `01-python-foundations/exercises/lesson-01/test_temperature_converter.py`

- [ ] **Step 1: Write the test file**

Create `01-python-foundations/exercises/lesson-01/test_temperature_converter.py`:

```python
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
```

- [ ] **Step 2: Run the tests**

Run:

```bash
python -m pytest 01-python-foundations/exercises/lesson-01/test_temperature_converter.py -v
```

Expected: all 12 collected tests PASS. If any test fails, the exercise has a real bug — stop and report it instead of changing the test.

- [ ] **Step 3: Commit**

```bash
git add 01-python-foundations/exercises/lesson-01/test_temperature_converter.py
git commit -m "test: validate lesson-01 temperature converter exercise"
```

---

### Task 4: Declare the dev dependency and document it

Add `requirements-dev.txt` pinning `pytest`, document the testing workflow in `CONTRIBUTING.md`, and run a final full verification.

**Files:**
- Create: `requirements-dev.txt`
- Modify: `CONTRIBUTING.md`

- [ ] **Step 1: Create `requirements-dev.txt`**

Create `requirements-dev.txt` at the repo root:

```
# Dependências de desenvolvimento (testes).
# Instale com: uv pip install -r requirements-dev.txt
pytest==8.4.1
```

- [ ] **Step 2: Add a "Testes" section to `CONTRIBUTING.md`**

In `CONTRIBUTING.md`, find this block (end of "Rodar manualmente", start of "Configuração"):

```
Verificar/corrigir todos os arquivos do repositório:

```bash
pre-commit run --all-files
```

## Configuração
```

Replace it with:

```
Verificar/corrigir todos os arquivos do repositório:

```bash
pre-commit run --all-files
```

## Testes

Os testes usam [pytest](https://docs.pytest.org/). Instale a dependência de
desenvolvimento (uma vez por clone):

```bash
uv pip install -r requirements-dev.txt
```

Rode todos os testes a partir da raiz do repositório:

```bash
pytest
```

## Configuração
```

- [ ] **Step 3: Run the full test suite from the repo root**

Run:

```bash
python -m pytest -v
```

Expected: pytest discovers both test files and all 29 tests PASS.

- [ ] **Step 4: Run pre-commit on all files**

Run:

```bash
pre-commit run --all-files
```

Expected: all hooks pass. If ruff auto-fixes import ordering or formatting in the new files, re-stage the changed files and run the hook again until it passes.

- [ ] **Step 5: Commit**

```bash
git add requirements-dev.txt CONTRIBUTING.md
git commit -m "build: add pytest dev dependency and document testing"
```

---

## Notes for the implementer

- Tests validate **already-implemented** exercises, so they should pass on the first run. A failing test means the exercise is wrong — report it; do not weaken the test to make it green.
- `python -m pytest` is used (rather than bare `pytest`) so the test run uses the same interpreter that has `pytest` installed.
- If `pytest` is not installed in the active environment, install it first with `uv pip install -r requirements-dev.txt` (after Task 4) or `python -m pip install pytest`.
