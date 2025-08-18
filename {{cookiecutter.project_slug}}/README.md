# Projeto {{ cookiecutter.project_name }}

    {{ cookiecutter.description }}

## Cliente

> {{ cookiecutter.client_name}}

## Dados do Projeto

> **Data da Criação** : {{ cookiecutter.created_date_project }}  
> **Django Version** : {{ cookiecutter.django_version }}  
> **Python Version**: {{ cookiecutter.python_version }}  
> **PostgreSQL Version** : {{ cookiecutter.postgresql_version }}

## Analista Responsável

> {{ cookiecutter.author_name }}  
> {{ cookiecutter.email }}

### Gerando a nova Secret Key

Para gerar uma nova SecretKey a ser utilizada no arquivo .env execute o comando a seguir (com o virtualenv ativado)

```shell
python contrib/secret_gen.py  
```

## Docker

### Como utilizar

Caso deseje desenvolver utilizando a tecnologia de containers (Docker) listamos abaixo os comandos para executar no
projeto

> Para usuários Windows é necessário garantir que o WSL2 esteja configurado e tenha instalado o Docker Desktop

### Criando a imagem e executando o container

```shell
docker-compose up -d
```

### Executando em ambiente de desenvolvimento

```shell
docker-compose --f docker-dev.yml up -d
```

### Forçando a geração da nova imagem e container

```shell
docker-compose -f docker-dev.yml up -d --force-recreate --no-deps
```

### Mostrando as imagens geradas

```shell
docker images ls
```

### Mostrando os containers gerados

```shell
docker container ls
```

### Acessando o terminal de um container executando em backgroud

```shell
docker container exec -it {{ cookiecutter.project_slug }}_django bash
```

### Saindo do terminal de um container que foi acesso via comando exec, sem **manter o container**

    CTRL + P, CTRL + Q

### Criando a SECRET_KEY

```shell
docker container exec -it {{ cookiecutter.project_slug }}_django bash -c "python contrib/secret_gen.py"
```

O comando acima retorna uma string similar a esta
***gvN3L7UR_4ADJrUjnLGdjzZuvFoT01gqYyFfQkY0Qava7DigkWS63YP8UBl7saAcV3E***

### Executando o makemigrations

```shell
docker container exec -it {{ cookiecutter.project_slug }}_django bash -c "python manage.py makemigrations"
```

### Executando o migrations

```shell
docker container exec -it {{ cookiecutter.project_slug }}_django bash -c "python manage.py migrate"    
```

### Executando o build da app Usuario

```shell
docker container exec -it {{ cookiecutter.project_slug }}_django bash -c "python manage.py build usuario"
```

### Executando o comando para gerar o SuperUser

```shell
docker container exec -it {{ cookiecutter.project_slug }}_django bash -c "python mock_superuser.py"
```

### Executando o comando para gerar os dados Fake do models Usuario

```shell
docker container exec -it {{ cookiecutter.project_slug }}_django bash -c "python mock_data.py"
```

### Criando uma nova app

```shell
docker container exec -it {{ cookiecutter.project_slug }}_django bash -c "python manage.py startapp NomeDaNovaApp"
```

### Container`s do Projeto

> Django {{ cookiecutter.project_slug }}_django
> PostgreSQL {{ cookiecutter.project_slug }}_database

### Network do Projeto

> {{cookiecutter.project_slug.lower()}}_network

### Dados do container do PostgreSQL

> Nome do Banco de Dados: {{cookiecutter.project_slug.lower()}}_db
> Usuário do Banco de Dados: {{cookiecutter.project_slug.lower()}}_dbmanager_2LiyBoLHeHo5yG
> Senha do Banco de Dados: senha_padrao_deve_ser_mudada
> Volume: {{cookiecutter.project_slug.lower()}}_db

### Acessando o projeto no navegador

http://localhost:{{ cookiecutter.docker_port }}

----

## Licença

[MIT](https://mit-license.org/)

Powered By

![Python](https://www.python.org/static/img/python-logo.png)
![Django](https://static.djangoproject.com/img/logo-django.42234b631760.svg)
