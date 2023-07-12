# Prospector

## Sobre

Biblioteca utilizada para manter a qualidade do código.  
  
Na raiz do projeto existe o arquivo ```.prospector.yaml``` contendo a configuração padrão para validação do código.

## Executar
    prospector

## Arquivo de configuração padrão

```markdown
strictness: medium
test-warnings: true
doc-warnings: false

ignore-paths:
  - docs
  - core
  - mock_data.py

ignore-patterns:
  - (^|/)skip(this)?(/|$)

pep8:
  disable:
    - W602
    - W603
  enable:
    - W601
  options:
    max-line-length: 120

mccabe:
  run: false
```

## Links
|Pip |Docs  |
--- | --- |
|[Pip](https://pypi.org/project/prospector/)|[Doc](http://prospector.landscape.io/en/master/)|


