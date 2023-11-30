from typing import List

from pydantic import AnyHttpUrl, ConfigDict
from pydantic_settings import BaseSettings

"""
Arquivos principal de configuração da app

- Nesse aquivo podem ser incluídas novos atributos que serão lidos pelo arquivo .env
- APP_NAME no .env se traduz para app_name dentro da aplicação
"""


class Settings(BaseSettings):
    # Projeto
    app_name: str
    app_url: AnyHttpUrl
    debug: str
    environment: str

    # FastAPI
    api_str: str = "/api/v1"
    backend_cors_origins: List[AnyHttpUrl] = ["http://localhost"]

    # Django
    django_url: str
    secret_key: str

    # Banco de dados
    db_engine: str
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    # Sentry
    sentry_dsn: str

    # Elastic
    elastic_apm_server_url: str

    model_config = ConfigDict(env_file=".env")


settings = Settings()
