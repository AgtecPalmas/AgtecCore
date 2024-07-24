import contextlib
import functools
import json
import pickle
from http import HTTPStatus
from typing import Any, Callable, Optional

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
            host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=False
        )

    def _get_chave_paginada(self, chave: str, offset: int, limit: int) -> str:
        if not offset:
            offset = 0

        if not limit:
            limit = 25

        return f"{chave}:offset:{offset}:limit:{limit}"

    def get_key(self, key: str) -> Optional[str]:
        """
        Gets the value for a key from Redis.

        Args:
        key (str): The key to retrieve from Redis.

        Returns:
        str: The value for the provided key
        None: If the key does not exist in Redis
        """
        _item = self.redis_conn.get(key)
        return pickle.loads(_item) if _item else None

    def get_keys(self, pattern: str):
        try:
            keys = self.redis_conn.scan(match=f"*{pattern}*")
            return [key.decode() for key in keys[1]]
        except Exception:
            return []

    def get_key_hash(self, key: str, field: str) -> str:
        """
        Gets the value of a specific field within a Redis hash.

        Args:
        - key (str): The key associated with the Redis hash.
        - field (str): The field within the hash to retrieve.

        Returns:
        - str: The value associated with the specified field.

        Raises:
        - KeyError: If the key or field does not exist in Redis.
        - Exception: Any other exception that may occur during the retrieval process.
        """
        try:
            _item = self.redis_conn.hget(key, field)
            if _item:
                return pickle.loads(_item)
            raise KeyError
        except Exception as e:
            raise ("Erro ao buscar dados no Redis: ", e)

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

        except Exception:
            return False

    def save_hash_data(self, key: str, field: str, field_value: dict, expire_in=60):
        """
        Save data to Redis using a key for a hash and an optional expiration time.

        Args:
        - key (str): The key under which to store the data in Redis.
        - field (str): The field name to associate with the value within the hash.
        - field_value (dict): The value to save in the specified field.
        - expire_in (int, optional): Number of minutes until the key expires. Defaults to 60.

        Raises:
        - Exception: Any exception raised while saving to Redis.
        """
        try:
            self.redis_conn.hset(key, field, pickle.dumps(field_value))
            self.redis_conn.expire(key, expire_in * MINUTES)
        except Exception as e:
            raise ("Erro ao salvar dados no Redis usando hash: ", e)

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

        except Exception:
            return False

    def delete_hash(self, key: str, field: str) -> bool:
        """
        Deletes a field from a Redis hash.

        Args:
        key (str): The key associated with the Redis hash.
        field (str): The field to delete from the hash.

        Returns:
        bool: True if the delete was successful, False otherwise.

        Raises:
        Exception: Any exception raised while deleting from Redis.
        """

        try:
            self.redis_conn.hdel(key, field)
            return True
        except Exception as e:
            raise ("Erro ao deletar chave do hash: ", e)

    def delete_all_keys(self) -> bool:
        """
        Deletes all keys from Redis.

        Returns:
        bool: True if the delete was successful, False otherwise.

        Raises:
        Exception: Any exception raised while deleting from Redis.
        """

        try:
            self.redis_conn.flushdb()
            return True
        except Exception as e:
            raise ("Erro ao deletar todas chaves: ", e)

    def delete_specific_keys(self, key_name: str) -> bool:
        """
        Delete all keys from Redis that start with the specified key name.

        Returns:
        bool: True if the delete was successful, False otherwise.

        Raises:
        Exception: Any exception raised while deleting from Redis.
        """

        try:
            for key in self.redis_conn.scan_iter(key_name + "*"):
                self.redis_conn.delete(key)
            return True
        except Exception as e:
            raise ("Erro ao deletar chave específica: ", e)

    def invalidate_pattern(self, pattern: str) -> bool:
        """
        Invalidate all the cached keys that match a pattern.

        Args:
            pattern (str): The desired pattern. Might be the ID of a resource, for example.

        Returns:
            bool: True if success, False otherwise.
        """
        try:
            keys = self.redis_conn.keys(f"*{pattern}*")
            for key in keys:
                self.delete(key)
            return True

        except Exception:
            return False

    def get_specific_field(self, key_name: str, field: str) -> Optional[str]:
        """
        Get

        Args:
            key_name (str): _description_
            field (str): _description_

        Returns:
            bool: _description_
        """
        try:
            for key in self.redis_conn.scan_iter(key_name + "*"):
                if teste := self.redis_conn.hget(key, field):
                    return teste
            return None
        except Exception as e:
            raise (f"Erro ao encontrar o campo nos hashes. Detail: {e}", e)

    def get_hash_field(self, key: str, field: str):
        try:
            object_redis = self.get_specific_field(key, field)
            if object_redis:
                return pickle.loads(object_redis)
            return None
        except Exception as e:
            return None

    def _init_chave(
        self, recurso: str, id_recursos: list[str], requisicao_kwargs: Any
    ) -> str:
        parametros = {
            nome_id: requisicao_kwargs.get(nome_id) for nome_id in id_recursos
        }
        # Inicializa a chave e adiciona a ela os parâmetros desejados,
        # no padrão "parâmetro:valor_do_parâmetro"
        chave = f"{recurso}"

        if parametros:
            for key, value in parametros.items():
                chave += f":{key}:{value}"

        else:
            chave += ":fetch"

        return chave

    def _handle_resource_update(
        self, recurso: str, chave: str, padrao_invalidado: str
    ) -> None:
        """
        Handles the update of a resource in Redis by invalidating cached keys based on provided patterns.

        Args:
            recurso (str): The name of the resource being updated.
            chave (str): The key associated with the resource.
            padrao_invalidado (str): The pattern to invalidate keys. If empty, a default pattern is used.

        Returns:
            None
        """
        with contextlib.suppress(Exception):
            self.invalidate_pattern(chave)
            if not padrao_invalidado:
                self.invalidate_pattern(f"{recurso}:fetch")

            else:
                self.invalidate_pattern(padrao_invalidado)

    def healthy(self):
        try:
            self.redis_conn.ping()
            return True
        except Exception:
            return False

    def cache_request(
        self,
        recurso: str,
        padrao_invalidado: str = None,
        id_recursos: list[str] = [],
        expiracao: int = 60 * MINUTES,
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
                if not self.healthy():
                    return await func(request, *args, **kwargs)

                chave = self._init_chave(
                    recurso=recurso, id_recursos=id_recursos, requisicao_kwargs=kwargs
                )

                if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
                    self._handle_resource_update(recurso, chave, padrao_invalidado)
                    return await func(request, *args, **kwargs)

                # Tratando caso o usuário tenha inserido um valor vazio para os
                # query params 'página' ou 'total_por_página'
                if kwargs.get("offset") or kwargs.get("limit"):
                    chave = self._get_chave_paginada(
                        chave, kwargs.get("offset"), kwargs.get("limit")
                    )

                if request.method == "GET":
                    resultado_cache = self.get_key(chave)
                    if resultado_cache:
                        if type(resultado_cache) in [str, bytes, bytearray]:
                            return json.loads(resultado_cache)
                        return resultado_cache

                resultado = await func(request, *args, **kwargs)

                # Para garantir que a requisição só será salva em cache
                # quando retornar código OK.
                if (
                    request.method == "GET"
                    and getattr(resultado, "status_code", HTTPStatus.OK)
                    == HTTPStatus.OK
                ):
                    resultado_cache = jsonable_encoder(resultado)
                    resultado_cache = json.dumps(resultado_cache)
                    self.save_key(chave, resultado_cache, expiracao)

                return resultado

            return inner

        return wrapper


redis_service = RedisService()