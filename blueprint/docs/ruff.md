# Ruff

## Sobre

Ferramenta responsável por analisar e formatar o código do projeto, garantindo conformidade com os padrões de qualidade do Python (PEPs).

Além da análise estática, também realiza correções automáticas e organização do código.

A configuração é feita diretamente no arquivo **pyproject.toml**.

Por padrão, está configurado que o limite de caracteres por linha é de 120.

## Executar

```bash
ruff check .
ruff check . --fix
ruff format .
```

## Arquivo de configuração padrão
```toml
[tool.ruff]
line-length = 120
target-version = "py314"
extend-exclude = [
  "core",
  "docs",
  ".venv",
  "migrations",
  ".env"
]

[tool.ruff.lint]
select = ["E", "F", "I"]
ignore = ["E203", "W503"]

[tool.ruff.format]
quote-style = "double"
```

## Links
|Pip |Docs  |
| --- | --- |
|[Pip](https://pypi.org/project/ruff/)|[Doc](https://docs.astral.sh/ruff/)|
