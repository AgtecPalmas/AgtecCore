# Documentação

Entenda como fazer alterações na documentação do projeto.

## Passo a passo para contribuir

Primeiramente você deve fazer os seguintes passos:

1. Fork do projeto
2. Clonar o fork para sua máquina local
3. Iniciar um projeto com o NuvolsCore.

Siga o processo descrito na aba [Primeiros Passos](./index.md) para fazer isso.

## Rode a documentação localmente

Com o novo projeto iniciado e com todas as dependências instaladas, você deve rodar a documentação localmente. Para isso, na pasta do projeto, execute o comando `task docs`. Ou se preferir, você pode usar o comando `mkdocs serve`.

## Faça suas alterações

Faça as alterações que deseja na documentação. Para isso, basta editar os arquivos na pasta `docs`. 

## Veja o resultado das suas alterações

Para visualizar o resultado das suas alterações em tempo real, basta acessar o endereço `http://localhost:8000` no seu navegador.
> Lembre-se que o comando `task docs` ou `mkdocs serve` deve estar rodando para ver o resultado das suas alterações.

## Transcreva as alterações para seu fork

Após finalizar suas alterações na pasta `docs` do projeto iniciado com o Nuvols Core, você deve transcrever elas para a pasta `{{cookiecutter.project_slug}}/docs` do seu fork. Pois é essa pasta que contém arquivos markdown que são usados para gerar a documentação do projeto. Segue abaixo um exemplo de como fazer isso:

## Transcreva suas alterações

Na branch `desenvolvimento` do seu fork, transcreva suas alterações feitas na pasta `docs` do projeto iniciado com o Nuvols Core para a pasta `{{cookiecutter.project_slug}}/docs` do seu fork. 

## Siga o processo de commit e push

Siga o processo de commit e push descrito na aba [Primeiros Passos](./index.md#commit-suas-alteracoes) em diante para concluír a contribuição.