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

- `ruff.toml` — regras de lint e formatação.
- `.pre-commit-config.yaml` — hooks e versões fixadas.
