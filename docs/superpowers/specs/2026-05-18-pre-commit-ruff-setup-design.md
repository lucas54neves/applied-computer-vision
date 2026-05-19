# Design — Configuração de pre-commit + ruff para todo o repositório

**Data:** 2026-05-18
**Repositório:** applied-computer-vision (repositório de curso de visão computacional)

## Objetivo

Estabelecer linting e formatação automáticos de código Python em todo o
repositório usando `pre-commit` + `ruff`, aplicados via git hook a cada commit.
O setup deve valer para todas as lições, presentes e futuras.

## Contexto

- O repositório hoje contém apenas `01-python-foundations/` (um exercício:
  `temperature_converter.py`). Mais lições serão adicionadas com o tempo.
- Não existe configuração de lint/format. O `.gitignore` já cobre
  `.ruff_cache/` e artefatos Python comuns.
- O ambiente não possui `pip`, `pipx`, `uv`, `ruff` nem `pre-commit`
  instalados — apenas Python 3.12.3.

## Decisões de design

### Ferramentas como dev tooling, não como dependências do projeto

`pre-commit` e `ruff` são ferramentas de desenvolvimento, não dependências do
código do curso. Portanto **não** entram em `requirements.txt`:

- `pre-commit` é instalado globalmente (fora do repositório) via `uv`.
- `ruff` é gerenciado pelo próprio `pre-commit` num ambiente isolado; o
  `.pre-commit-config.yaml` declara a ferramenta e fixa sua versão.
- O `.pre-commit-config.yaml` funciona como o manifesto das ferramentas: quem
  clonar o repositório roda `pre-commit install` e tudo é resolvido a partir
  dele.

### Configuração do ruff em `ruff.toml`

A config do ruff fica em um `ruff.toml` dedicado na raiz, e não em
`pyproject.toml`. O repositório é um repositório de curso, não um pacote Python
distribuível; um `ruff.toml` mantém a configuração explícita sem implicar
empacotamento. O `ruff.toml` na raiz é auto-descoberto pelo ruff (CLI e editor)
e vale para todo o repositório.

## Componentes a entregar

### 1. Instalação das ferramentas (uv)

- Instalar o `uv` (gerenciador da Astral) via script oficial
  (`curl -LsSf https://astral.sh/uv/install.sh | sh`), sem sudo. Instala em
  `~/.local/bin`.
- `uv tool install pre-commit` — disponibiliza o `pre-commit` como CLI global
  isolado.
- `uv tool install ruff` — disponibiliza o `ruff` como CLI standalone, para
  execução manual e integração com o editor. (O hook do pre-commit usa sua
  própria cópia isolada; o CLI standalone é uma conveniência adicional.)

### 2. `ruff.toml` na raiz

- `target-version = "py312"`
- `line-length = 88`
- `[lint] select = ["E", "F", "I", "UP", "B", "SIM"]`
  - `E`/`F`: erros e pyflakes
  - `I`: ordenação de imports
  - `UP`: sintaxe Python moderna
  - `B`: bugs comuns (flake8-bugbear)
  - `SIM`: simplificações (flake8-simplify)

### 3. `.pre-commit-config.yaml` na raiz

- Hook `ruff-pre-commit`:
  - `ruff` com `--fix` (lint com correção automática)
  - `ruff-format` (formatação)
  - Ambos com `types_or: [python, pyi, jupyter]` para cobrir `.py` e
    notebooks `.ipynb`.
- Hook `pre-commit-hooks` (higiene de arquivos):
  - `trailing-whitespace`
  - `end-of-file-fixer`
  - `check-yaml`
  - `check-added-large-files`
  - `check-merge-conflict`
- Todas as versões fixadas em `rev:` nas releases estáveis mais recentes
  disponíveis no momento da implementação.

### 4. `requirements.txt` na raiz

- Arquivo vazio, contendo apenas um comentário-cabeçalho que explica seu
  propósito: declarar as bibliotecas do curso (numpy, opencv, matplotlib,
  etc.) à medida que as lições as exigirem.
- As ferramentas de dev (`pre-commit`, `ruff`) **não** entram neste arquivo.

### 5. `CONTRIBUTING.md` curto

- Instruções de setup reproduzível para qualquer pessoa que clone o
  repositório: instalar `uv`, rodar `uv tool install pre-commit`, rodar
  `pre-commit install`.

## Ativação e verificação

1. `pre-commit install` — registra o git hook em `.git/hooks/`.
2. `pre-commit run --all-files` — primeira passada em todo o repositório.
   Espera-se que formate/corrija o `temperature_converter.py` existente.
3. Confirmar que o `.gitignore` já cobre `.ruff_cache/` (não requer alteração).

## Fora de escopo (YAGNI)

- Verificação de tipos (mypy).
- Hooks de testes (pytest).
- CI / GitHub Actions.
- Instalação efetiva das bibliotecas de visão computacional (numpy, opencv,
  etc.) — apenas o `requirements.txt` vazio é criado como ponto de partida.

## Critérios de sucesso

- `pre-commit run --all-files` executa e termina com sucesso (após corrigir
  automaticamente o que for corrigível).
- Um `git commit` dispara os hooks automaticamente.
- A configuração se aplica a qualquer arquivo `.py`/`.ipynb` em qualquer
  diretório de lição, presente ou futuro.
- Um novo clone do repositório consegue ativar os hooks seguindo o
  `CONTRIBUTING.md`.
