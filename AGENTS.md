# Agent Instructions

Instructions for AI agents (Claude Code and others) working in this repository.
`CLAUDE.md` is a symlink to this file.

## Project

Learning repository for an applied computer vision course. Code is organized by
lesson (e.g. `01-python-foundations/`), and the repository grows as lessons are
added.

## Conventions

- **Language: English.** Everything you create — source code, comments,
  identifiers, documentation, commit messages, and pull request titles/bodies —
  must be written in English, unless the user explicitly requests otherwise.

## Tooling

- Linting and formatting use [`pre-commit`](https://pre-commit.com/) with
  [`ruff`](https://docs.astral.sh/ruff/). See `CONTRIBUTING.md` for setup.
- Ruff configuration lives in `ruff.toml`; hooks are declared in
  `.pre-commit-config.yaml`.
- Run `pre-commit run --all-files` to lint/format the whole repository.
