# Pre-commit + Ruff Setup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Configurar linting e formatação automáticos de Python em todo o repositório via `pre-commit` + `ruff`, disparados como git hook a cada commit.

**Architecture:** O `pre-commit` é instalado globalmente via `uv` (fora do repositório). O `.pre-commit-config.yaml` na raiz declara os hooks (ruff + higiene de arquivos) com versões fixadas e funciona como manifesto das ferramentas. A config do ruff vive num `ruff.toml` dedicado na raiz, auto-descoberto por todo o repositório. As bibliotecas do curso são separadas das ferramentas de dev e ganham um `requirements.txt` vazio como ponto de partida.

**Tech Stack:** uv (gerenciador da Astral), pre-commit, ruff, Python 3.12.

---

## Notas sobre este plano

Esta tarefa é configuração de ambiente/repositório, não desenvolvimento de
código com TDD. Não há testes unitários a escrever. A "verificação" de cada
tarefa é executar comandos e confirmar a saída esperada. Cada tarefa termina
com um commit quando há arquivos versionados a salvar (a instalação de
ferramentas via `uv` não produz arquivos versionados).

## Estrutura de arquivos

- Criar: `ruff.toml` — configuração do ruff (lint + format) para todo o repo.
- Criar: `.pre-commit-config.yaml` — declaração dos hooks e versões.
- Criar: `requirements.txt` — placeholder para bibliotecas do curso.
- Criar: `CONTRIBUTING.md` — instruções de setup reproduzível.
- Modificar (automático): `01-python-foundations/exercises/lesson-01/temperature_converter.py` — será reformatado pela primeira passada do ruff.
- Sem alteração: `.gitignore` — já cobre `.ruff_cache/`.

---

### Task 1: Instalar uv, pre-commit e ruff

**Files:**
- Nenhum arquivo versionado (instalações de ferramentas no ambiente do usuário).

- [ ] **Step 1: Instalar o uv**

Run:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Expected: mensagem de sucesso indicando instalação em `~/.local/bin`.

- [ ] **Step 2: Garantir que `~/.local/bin` está no PATH da sessão**

Run:
```bash
export PATH="$HOME/.local/bin:$PATH"
uv --version
```
Expected: imprime a versão do uv (ex.: `uv 0.x.y`). Se `uv` não for
encontrado, abrir um novo shell ou recarregar o profile (`source ~/.bashrc`).

- [ ] **Step 3: Instalar o pre-commit como ferramenta global**

Run:
```bash
uv tool install pre-commit
```
Expected: mensagem confirmando `pre-commit` instalado e disponível em
`~/.local/bin`.

- [ ] **Step 4: Instalar o ruff como ferramenta global**

Run:
```bash
uv tool install ruff
```
Expected: mensagem confirmando `ruff` instalado.

- [ ] **Step 5: Verificar os dois CLIs**

Run:
```bash
pre-commit --version && ruff --version
```
Expected: imprime as versões de `pre-commit` e de `ruff`, sem erro.

---

### Task 2: Criar o `ruff.toml`

**Files:**
- Create: `ruff.toml`

- [ ] **Step 1: Criar o `ruff.toml` na raiz do repositório**

Conteúdo de `ruff.toml`:
```toml
# Configuração do ruff para todo o repositório.
# Auto-descoberta: vale para qualquer arquivo .py/.ipynb em qualquer lição.
target-version = "py312"
line-length = 88

[lint]
# E/F  -> erros e pyflakes
# I    -> ordenação de imports
# UP   -> sintaxe Python moderna (pyupgrade)
# B    -> bugs comuns (flake8-bugbear)
# SIM  -> simplificações (flake8-simplify)
select = ["E", "F", "I", "UP", "B", "SIM"]

[format]
# Padrões do ruff-format (estilo compatível com Black).
```

- [ ] **Step 2: Verificar que a config é válida**

Run:
```bash
ruff check --show-settings . > /dev/null && echo "config OK"
```
Expected: imprime `config OK` sem erro de parsing do `ruff.toml`.

- [ ] **Step 3: Commit**

```bash
git add ruff.toml
git commit -m "build: add ruff configuration"
```

---

### Task 3: Criar o `.pre-commit-config.yaml`

**Files:**
- Create: `.pre-commit-config.yaml`

- [ ] **Step 1: Criar o `.pre-commit-config.yaml` na raiz**

Conteúdo de `.pre-commit-config.yaml` (os `rev:` abaixo são valores iniciais;
o Step 2 os atualiza para as últimas versões estáveis):
```yaml
# Hooks de pre-commit do repositório. Para ativar localmente: pre-commit install
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.0
    hooks:
      - id: ruff
        args: [--fix]
        types_or: [python, pyi, jupyter]
      - id: ruff-format
        types_or: [python, pyi, jupyter]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
```

- [ ] **Step 2: Fixar os hooks nas últimas versões estáveis**

Run:
```bash
pre-commit autoupdate
```
Expected: o comando reescreve os campos `rev:` para as releases estáveis mais
recentes de `ruff-pre-commit` e `pre-commit-hooks`. Imprime linhas como
`updating ... -> vX.Y.Z`.

- [ ] **Step 3: Validar o arquivo de configuração**

Run:
```bash
pre-commit validate-config
```
Expected: sem saída de erro (config válida).

- [ ] **Step 4: Commit**

```bash
git add .pre-commit-config.yaml
git commit -m "build: add pre-commit hooks (ruff + file hygiene)"
```

---

### Task 4: Criar o `requirements.txt`

**Files:**
- Create: `requirements.txt`

- [ ] **Step 1: Criar o `requirements.txt` na raiz**

Conteúdo de `requirements.txt`:
```text
# Bibliotecas do curso de visão computacional.
# Adicione aqui as dependências conforme as lições as exigirem
# (ex.: numpy, opencv-python, matplotlib).
#
# NÃO inclua ferramentas de dev (pre-commit, ruff) neste arquivo:
# elas são instaladas globalmente via `uv tool install` e declaradas
# em .pre-commit-config.yaml.
```

- [ ] **Step 2: Commit**

```bash
git add requirements.txt
git commit -m "build: add requirements.txt placeholder for course libraries"
```

---

### Task 5: Criar o `CONTRIBUTING.md`

**Files:**
- Create: `CONTRIBUTING.md`

- [ ] **Step 1: Criar o `CONTRIBUTING.md` na raiz**

Conteúdo de `CONTRIBUTING.md`:
```markdown
# Contribuindo

Este repositório usa [pre-commit](https://pre-commit.com/) com
[ruff](https://docs.astral.sh/ruff/) para lint e formatação automáticos do
código Python a cada commit.

## Setup (uma vez por clone)

1. Instale o `uv` (gerenciador de pacotes/ferramentas da Astral):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Instale o `pre-commit` como ferramenta global:

   ```bash
   uv tool install pre-commit
   ```

3. Ative os git hooks neste repositório:

   ```bash
   pre-commit install
   ```

Pronto. A partir daí, `ruff` (lint + format) e verificações de higiene de
arquivos rodam automaticamente a cada `git commit`.

## Rodar manualmente

Verificar/corrigir todos os arquivos do repositório:

```bash
pre-commit run --all-files
```

## Configuração

- `ruff.toml` — regras de lint e formatação.
- `.pre-commit-config.yaml` — hooks e versões fixadas.
```

- [ ] **Step 2: Commit**

```bash
git add CONTRIBUTING.md
git commit -m "docs: add CONTRIBUTING with pre-commit setup instructions"
```

---

### Task 6: Ativar os hooks e rodar a primeira passada no repositório

**Files:**
- Modify (automático): `01-python-foundations/exercises/lesson-01/temperature_converter.py`

- [ ] **Step 1: Instalar o git hook**

Run:
```bash
pre-commit install
```
Expected: `pre-commit installed at .git/hooks/pre-commit`.

- [ ] **Step 2: Rodar todos os hooks em todo o repositório**

Run:
```bash
pre-commit run --all-files
```
Expected: na primeira execução o `pre-commit` baixa os ambientes dos hooks.
Os hooks `ruff` e `ruff-format` provavelmente reportam `Failed` e modificam
`temperature_converter.py` (esse arquivo tem uma linha acima de 88 colunas e
falta linha em branco antes de `main()`). Isso é esperado: os hooks corrigem
automaticamente.

- [ ] **Step 3: Revisar as mudanças automáticas**

Run:
```bash
git diff
```
Expected: alterações apenas de formatação em `temperature_converter.py`
(quebra da linha longa, linhas em branco). Confirmar que nenhuma mudança
alterou a lógica do código.

- [ ] **Step 4: Rodar os hooks de novo para confirmar que passam**

Run:
```bash
pre-commit run --all-files
```
Expected: todos os hooks reportam `Passed` (não há mais nada a corrigir).

- [ ] **Step 5: Commit das correções automáticas**

```bash
git add -A
git commit -m "style: apply ruff formatting to existing code"
```
Expected: o git hook do pre-commit roda neste commit e passa, já que os
arquivos já estão formatados.

---

## Verificação final

- [ ] `pre-commit run --all-files` termina com todos os hooks em `Passed`.
- [ ] `git log --oneline` mostra os commits das tasks 2–6.
- [ ] `git status` está limpo.
- [ ] Existem na raiz: `ruff.toml`, `.pre-commit-config.yaml`,
  `requirements.txt`, `CONTRIBUTING.md`.
