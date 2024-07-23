import functools
import json
import pickle
from typing import Any, Callable
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from redis import Redis
from .config import settings 

REDIS_HOST = settings.redis_host
REDIS_PORT = settings.redis_port
REDIS_DB = settings.redis_db

MINUTES: int = 60

class RedisService:
    def __init__(self) -> None:
        self.redis_conn = Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=False
        )

    def _get_chave_paginada(self, chave: str, offset: int, limit: int):
        if not offset:
            chave += f":offset_0:limit:{limit}"
        elif not limit:
            chave += f"offset_{offset}:limit:25"
        else:
            chave += f":offset_{offset}:limit:{limit}"

        return chave

    def get_key(self, key: str) -> str:
        """
        Gets the value for a key from Redis.

        Args:
        key (str): The key to retrieve from Redis.

        Returns:
        str: The value for the provided key.
        """
        _item = self.redis_conn.get(key)
        if _item:
            return pickle.loads(_item)
        return None

    def save_key(self, key: str, value: str | dict, expire_in: int = 60) -> bool:
        """
        Saves a value to Redis with a key and optional expiration.

        Args:
        key (str): The key to save the data under in Redis.
        value (str|dict): The value to save in Redis.
        expire_in (int, optional): Number of minutes until the key expires. Defaults to 60.

        Returns:
        bool: True if the save was successful, False otherwise.

        Raises:
        Exception: Any exception raised while saving to Redis.
        """

        try:
            self.redis_conn.set(key, pickle.dumps(value))
            self.redis_conn.expire(key, expire_in * MINUTES)
            return True
        except Exception as e:
            return False

    def delete(self, key: str) -> bool:
        """
        Deletes a key from Redis.

        Args:
        key (str): The key to delete from Redis.

        Returns:
        bool: True if the delete was successful, False otherwise.

        Raises:
        Exception: Any exception raised while deleting from Redis.
        """

        try:
            self.redis_conn.delete(key)
            return True
        except Exception as e:
            return False

    def invalidate_pattern(self, pattern: str):
        """
        Invalidate all the cached keys that match a pattern.

        Args:
            pattern (str): The desired pattern. Might be the ID of a resource, for example.

        Returns:
            bool: True if success, False if an exception occurred.
        """
        try:
            keys = self.redis_conn.keys(f"*{pattern}*")
            for key in keys:
                self.delete(key)
        except Exception as e:
            raise e

    def _init_chave(self, recurso: str, id_recursos: list[str], requisicao_kwargs: Any) -> str:
        # Extrai dos argumentos da requisição (kwargs) os nomes dos identificadores que
        # serão usados para identificar a chave
        parametros = {}
        for nome_id in id_recursos:
            parametros[nome_id] = requisicao_kwargs.get(nome_id)

        # Inicializa a chave e adiciona a ela os parâmetros desejados,
        # no padrão "parâmetro:valor_do_parâmetro"
        chave = f"{recurso}"
        if parametros:
            for key, value in parametros.items():
                chave += f":{key}:{value}"
        else:
            chave += ":fetch"

        return chave

    def cache_request(
        self, recurso: str, padrao_invalidado: str = None, id_recursos: list[str] = [],  expiracao: int = 3600
    ) -> Callable:
        """Decorator responsável por armazenar em cache o resultado de uma requisição. Deve ser utilizado nas
        funções dos módulos de rotas. 

        Args:
            recurso (str): Nome do recurso a ser armazenado.
            padrao_invalidado (str, optional): Padrão das chaves que devem ser invalidadas nesta requisição.
            id_recursos (list[str], optional): Identificadores que serão utilizados para gerar a chave.
            expiracao (int, optional): Tempo de expiração em segundos.
        """

        def wrapper(func: Callable) -> Callable:
            @functools.wraps(func)
            async def inner(request: Request, *args: Any, **kwargs: Any) -> Callable:
                chave = self._init_chave(
                    recurso=recurso,
                    id_recursos=id_recursos,
                    requisicao_kwargs=kwargs
                    )

                # Tratando caso o usuário tenha inserido um valor vazio para os
                # query params 'página' ou 'total_por_página'
                offset = kwargs.get("offset")
                limit = kwargs.get("limit")

                if offset or limit:
                    chave = self._get_chave_paginada(chave, offset, limit)

                if request.method == 'POST' or request.method == 'PUT': 
                    try:
                        self.invalidate_pattern(chave)
                        if not padrao_invalidado:
                            self.invalidate_pattern(f"{recurso}:fetch")
                        else:
                            self.invalidate_pattern(padrao_invalidado)
                    except Exception:
                        pass

                if request.method == "GET":
                    resultado_cache = self.get_key(chave)
                    if resultado_cache:
                        return json.loads(resultado_cache)

                resultado = await func(request, *args, **kwargs)

                # Para garantir que a requisição só será salva em cache
                # quando retornar código 200.
                salvar_cache = True
                try:
                    if resultado.status_code != 200:
                        salvar_cache = False
                except AttributeError:
                    pass

                if salvar_cache and request.method == "GET":
                    resultado_cache = jsonable_encoder(resultado)
                    resultado_cache = json.dumps(resultado_cache)
                    self.save_key(chave, resultado_cache, expiracao)
                


                return resultado

            return inner

        return wrapper


redis_service = RedisService()