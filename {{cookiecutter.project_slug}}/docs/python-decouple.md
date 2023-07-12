# Python Decouple

## Sobre

Lib para aplicar dentre outras funcionalidades a separação de dados sensíveis da aplicação do arquivo settings e colocar em variáveis de ambiente

## Arquivo .env
No ambiente de desenvolvimento deve-se utilizar esse arquivo para conter as configurações do projeto. Como exemplo 
temos a configuração da variáveis SECRET_KEY e do DATABASE.

### Gerando uma nova chave SECRET_KEY para o projeto gerado

```python
from django.core.management import utils
print(utils.get_random_secret_key())
```

### O arquivo .env deve ser adicionado no arquivo .gitignore para evitar de ser enviado ao servidor de versionamento  

  
```
# Substitua os __itens__ pelos valores correspondentes

SECRET_KEY=__secret_key__
DEBUG=True
ALLOWED_HOSTS=.localhost,*
API_PATH=http://localhost:8080/

# Sentry
SENTRY_DNS=__sentry_dns__

# Database
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=__nome_do_banco_de_dados__
DB_USER=__usuario_do_banco_de_dados__
DB_PASSWORD=__senha_do_banco_de_dados__
DB_HOST=__host_do_banco_de_dados__
DB_PORT=__porta_do_banco_de_dados__

FCM_KEY=#Informar a chave de envio de PushNotification do Firebase
HORAS_SEM_ATENDIMENTO=19, 20, 21, 22, 23, 0, 1, 2, 3, 4, 5, 6, 7, 12
# 0 Seg - 1 Ter - 2 Qua - 3 Qui - 4 Sex - 5 Sab - 6 Dom
DIAS_DA_SEMANA=0, 1, 2, 3, 4
SENHA_PADRAO=__para_mockar_users__

# ELASTIC APM
ELASTIC_APM_SERVER_URL=__url_do_servidor_apm__:__porta_do_servidor_apm__
ELASTIC_APM_ENVIRONMENT=__nome_do_ambiente__

# Gitlab Core
GITLAB_API_CORE_URL=https://__url_gitlab__/api/v4/projects/__id_projeto__/repository/
GITLAB_TOKEN=__token_gitlab__
```

## Links
|Pip |Docs  |
--- | --- |
|[Pip](https://pypi.org/project/python-decouple/)|[Doc](https://github.com/henriquebastos/python-decouple)|
