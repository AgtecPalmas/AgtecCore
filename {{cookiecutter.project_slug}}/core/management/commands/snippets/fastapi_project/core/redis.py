import contextlib
import functools
import json
import pickle
from http import HTTPStatus
from typing import Any, Callable, Optional

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from redis import Redis
from redis.exceptions import RedisError

from .config import settings

REDIS_HOST = settings.redis_host
REDIS_PORT = settings.redis_port
REDIS_DB = settings.redis_db
CACHE_DEFAULT_EXPIRE_IN_MINUTES = settings.cache_default_expire_in_minutes

MINUTES: int = 60


class RedisService:
    def __init__(self) -> None:
        self.redis_conn = Redis(
            host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=False
        )

    def _get_cached_response(self, request: Request, key: str) -> Any:
        """Method that gets the cached response for a HTTP request.

        Args:
            request (Request): the instance of the request
            key (str): the Redis key in which the response might be cached

        Returns:
            Any: The cached response
        """
        if request.method == "GET":
            resultado_cache = self.get_key(key)
            if type(resultado_cache) in [str, bytes, bytearray]:
                return json.loads(resultado_cache)
            return resultado_cache

    def _cache_response(
        self,
        request: Request,
        key: str,
        response: Any,
        expire_in: int = CACHE_DEFAULT_EXPIRE_IN_MINUTES * MINUTES,
    ):
        """Method that stores a request's response on cache. Only saves the response
        if it's status code is OK.

        Args:
            request (Request): An instance of the request
            key (str): The key in which the response will be stored
            response (Any): The content of the response
            expire_in (int): The expiration time in seconds
        """
        if (
            request.method == "GET"
            and getattr(response, "status_code", HTTPStatus.OK) == HTTPStatus.OK
        ):
            resultado_cache = jsonable_encoder(response)
            resultado_cache = json.dumps(resultado_cache)
            self.save_key(key, resultado_cache, expire_in)

    def _init_redis_key(
        self, resource: str, id_resources: list[str], request_kwargs: Any
    ) -> str:
        """Initializes a Redis key based on the data from the request.

        Args:
            resource (str): The resource to be cached through the key
            id_resources (list[str]): The resource identificators' names
            request_kwargs (Any): The arguments of the request

        Returns:
            str: The resultant key
        """
        params = {id_name: request_kwargs.get(id_name) for id_name in id_resources}
        # Inicializa a chave e adiciona a ela os parâmetros desejados,
        # no padrão "parâmetro:valor_do_parâmetro"
        redis_key = f"{resource}"

        if params:
            for key, value in params.items():
                redis_key += f":{key}:{value}"

        else:
            redis_key += ":fetch"

        return redis_key

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

    def _decode_scan_result(self, result):
        try:
            return [key.decode() for key in result]
        except Exception as e:
            raise Exception(f"Erro ao decodificar resultados de SCAN: {e}")

    def _get_paginated_key(self, chave: str, offset: int, limit: int) -> str:
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
            keys = self.redis_conn.scan_iter(match=f"*{pattern}*")
            return self._decode_scan_result(keys)
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
        except pickle.PickleError as e:
            raise pickle.PickleError(f"Error while unpickling data. Detail: {e}")
        except RedisError as e:
            raise RedisError("Erro ao buscar dados no Redis: ", e)

    def save_key(
        self,
        key: str,
        value: str | dict,
        expire_in: int = CACHE_DEFAULT_EXPIRE_IN_MINUTES * MINUTES,
    ) -> bool:
        """
        Saves a value to Redis with a key and optional expiration.

        Args:
        key (str): The key to save the data under in Redis.
        value (str|dict): The value to save in Redis.
        expire_in (int, optional): Number of minutes until the key expires. Defaults to 60.

        Returns:
        bool: True if the save was successful, False otherwise.

        Raises:
        RedisError: Any exception raised while saving to Redis.
        """

        try:
            self.redis_conn.set(key, pickle.dumps(value))
            self.redis_conn.expire(key, expire_in * MINUTES)
            return True

        except RedisError:
            return False

    def save_hash_data(
        self,
        key: str,
        field: str,
        field_value: dict,
        expire_in: int = CACHE_DEFAULT_EXPIRE_IN_MINUTES * MINUTES,
    ):
        """
        Save data to Redis using a key for a hash and an optional expiration time.

        Args:
        - key (str): The key under which to store the data in Redis.
        - field (str): The field name to associate with the value within the hash.
        - field_value (dict): The value to save in the specified field.
        - expire_in (int, optional): Number of minutes until the key expires. Defaults to 60.

        Raises:
        - RedisError: Any exception raised while saving to Redis.
        """
        try:
            self.redis_conn.hset(key, field, pickle.dumps(field_value))
            self.redis_conn.expire(key, expire_in * MINUTES)
        except RedisError as e:
            raise RedisError(f"Error while storing hash data on Redis: {e}")

    def delete(self, key: str) -> bool:
        """
        Deletes a key from Redis.

        Args:
        key (str): The key to delete from Redis.

        Returns:
        bool: True if the delete was successful, False otherwise.

        Raises:
        RedisError: Any exception raised while deleting from Redis.
        """

        try:
            self.redis_conn.delete(key)
            return True

        except RedisError:
            return False

    def delete_hash_field(self, key: str, field: str) -> bool:
        """
        Deletes a field from a Redis hash.

        Args:
        key (str): The key associated with the Redis hash.
        field (str): The field to delete from the hash.

        Returns:
        bool: True if the delete was successful, False otherwise.

        Raises:
        RedisError: Any exception raised while deleting from Redis.
        """

        try:
            self.redis_conn.hdel(key, field)
            return True
        except RedisError as e:
            raise RedisError(f"Error while deleting hash field: {e}")

    def delete_all_keys(self) -> bool:
        """
        Deletes all keys from Redis.

        Returns:
        bool: True if the delete was successful, False otherwise.

        Raises:
        RedisError: Any exception raised while deleting from Redis.
        """

        try:
            self.redis_conn.flushdb()
            return True
        except RedisError as e:
            raise RedisError(f"Error while deletig all keys: {e}")

    def delete_specific_keys(self, key_name: str) -> bool:
        """
        Delete all keys from Redis that start with the specified key name.

        Returns:
        bool: True if the delete was successful, False otherwise.

        Raises:
        RedisError: Any exception raised while deleting from Redis.
        """

        try:
            for key in self.redis_conn.scan_iter(key_name + "*"):
                self.redis_conn.delete(key)
            return True
        except RedisError as e:
            raise RedisError(f"Error while deleting key '{key_name}': {e}")

    def invalidate_pattern(self, pattern: str) -> bool:
        """
        Invalidate all the cached keys that contain a pattern.

        Args:
            pattern (str): The desired pattern. Might be the ID of a resource, for example.

        Returns:
            bool: True if success, False otherwise.

        Raises:
        RedisError: Any exception raised while deleting from Redis.
        """
        try:
            for key in self.redis_conn.scan_iter(match=f"*{pattern}*"):
                self.delete(key)
            return True

        except RedisError as e:
            raise RedisError(f"Error while invalidating pattern '{pattern}': {e}")

    def get_specific_field(self, key_name: str, field: str) -> Optional[str]:
        """
        Get

        Args:
            key_name (str): _description_
            field (str): _description_

        Returns:
            bool:

        Raises:
        RedisError: Any exception raised while getting key from Redis.
        """
        try:
            for key in self.redis_conn.scan_iter(key_name + "*"):
                if field := self.redis_conn.hget(key, field):
                    return field
            return None
        except RedisError as e:
            raise RedisError(f"Error while getting data from Redis. Detail: {e}")

    def get_hash_field(self, key: str, field: str):
        try:
            object_redis = self.get_specific_field(key, field)
            if object_redis:
                return pickle.loads(object_redis)
            return None
        except pickle.PickleError as e:
            raise pickle.PickleError(f"Error while unpickling data. Detail: {e}")
        except RedisError as e:
            raise RedisError(f"Error while getting data from Redis. Detail: {e}")

    def healthy(self):
        """Method that verifies if the Redis instance is running or not.

        Returns:
            bool: If the redis instance is healthy or not
        """
        try:
            self.redis_conn.ping()
            return True
        except RedisError:
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

                chave = self._init_redis_key(
                    resource=recurso, id_resources=id_recursos, request_kwargs=kwargs
                )

                # Verificando se o debug é true para limpar o cache
                if settings.debug:
                    self.invalidate_pattern(recurso)
                    return await func(request, *args, **kwargs)

                if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
                    self._handle_resource_update(recurso, chave, padrao_invalidado)
                    return await func(request, *args, **kwargs)

                # Tratando caso o resultado seja paginado e o usuário tenha
                # inserido um valor vazio para os query params 'página' ou
                # 'total_por_página'
                if kwargs.get("offset") or kwargs.get("limit"):
                    chave = self._get_paginated_key(
                        chave, kwargs.get("offset"), kwargs.get("limit")
                    )

                if cached_response := self._get_cached_response(request, chave):
                    return cached_response

                resultado = await func(request, *args, **kwargs)
                self._cache_response(request, chave, resultado, expiracao)

                return resultado

            return inner

        return wrapper


redis_service = RedisService()
