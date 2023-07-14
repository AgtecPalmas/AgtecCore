# Flake8

## Sobre

Biblioteca responsável por analisar se os códigos do projeto estão segundo os padrões de qualidade de código do Python, as famosas PEP`s.  
  
Na raiz do projeto existe o arquivo **.flake8** que deve ser utilizado para configurar o comportamento da lib. Por padrão foi configurado que o limite de caracteres por linha é de 120.

## Executar
```python
flake8
```

## Arquivo de configuração padrão
```toml
[flake8]
max-line-length=120
exclude=.venv
```

## Links
|Pip |Docs  |
| --- | --- |
|[Pip](https://pypi.org/project/flake8/)|[Doc](https://flake8.pycqa.org/en/latest/)|
