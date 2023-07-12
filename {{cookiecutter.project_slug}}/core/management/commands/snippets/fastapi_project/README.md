# Projeto FastAPI

Esse projeto foi gerado a partir do projeto Django, os dois projetos estão interligados. O módulo de autenticação (authentication) interage diretamente com as permissões do projeto Django.

> Caso você tenha criado o super usuário no projeto Django, você pode usar o mesmo usuário e senha para acessar esse projeto.

----

## Executando o projeto via Docker

```shell
docker-compose -f docker-dev.yml up -d --force-recreate --no-deps
```

## Uso

Por padrão a porta que o projeto roda é a **8181**, caso tenha algum outro container rodando na mesma porta, altere a porta no arquivo docker-dev.yml.

### Acessando o projeto no navegador

<http://localhost:8181/docs>

## Rotas

Todas as rotas estão disponíveis nas urls:  /docs ou /redoc, com Swagger or ReDoc.

## Estrutura do projeto

As partes da aplicação são:

```code
fastapi-to-do
  ├── core - app de configuração do projeto.
  │   ├── api - endpoints principais.
  │   ├── config - arquivo de configuração.
  │   |── cruds - arquivo com crud padrão a ser herdados.
  |   |── database - arquivo de configuração  do banco de dados.
  |   └── security - arquivos de configuração de seguranca.
  ├── authentication - app com todas as rotas relacionadas ao usuário.
  │   ├── api - endpoints da app.
  │   ├── cruds - cruds para interacao com o banco de dados.
  │   |── models - models da app.
  |   |── schemas - schemas a serem usados nas rotas.
  |   └── security - arquivos de configuração de seguranca.
  ├── migrations - app relacionada as migrations da aplicação.
  │   ├── versions - migrations geradas para o banco de dados.
  │   └── env - arquivo de configuração das migrations.
  ├── .env.example - arquivo com as configurações locais da aplicação.
  └── main.py - FastAPI aplicação e configuração do servidor.
```
