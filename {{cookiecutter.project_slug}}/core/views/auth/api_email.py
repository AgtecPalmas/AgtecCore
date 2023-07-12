from datetime import datetime
from time import sleep

import requests
from decouple import config
from requests import Response
from sentry_sdk import capture_exception

from core.utils import get_cache, save_to_cache


class ApiEmail:
    """Classe para gerenciar o token da API do ApiEmail"""

    def __init__(self):
        self.token: str = None
        self.expires_at: datetime = None
        self.url_auth: str = f"{config('API_EMAIL_URL')}/api/v1/autenticacao"
        self.url_send_email: str = (
            f"{config('API_EMAIL_URL')}/api/v1/email/mandar_email"
        )
        self.headers: dict = {
            "content-type": "application/x-www-form-urlencoded; charset=utf-8"
        }
        self.auth_data: dict = {
            "username": config("API_EMAIL_USERNAME"),
            "password": config("API_EMAIL_PASSWORD"),
        }

    def is_valid(self) -> bool:
        """Verifica se o token ainda é válido"""
        return self.expires_at > datetime.now()

    def get_token(self) -> str:
        """Retorna o token da API do ApiEmail"""
        # Verifica se o token está no cache
        if self._verify_cache() and self.is_valid():
            return self.token

        # Busca um novo token
        try:
            retries: int = 0

            while retries < 5:
                response: Response = self._request_token()

                if response.get("token") is None:
                    sleep(2**retries)
                    retries += 1

                else:
                    self._update_token(
                        token=response.get("token"),
                        expires_at=datetime.strptime(
                            response.get("time_expiration_token"), "%d/%m/%Y %H:%M:%S"
                        ),
                    )
                    save_to_cache(self.token, 3600)
                    return self.token

            return None

        except Exception as e:
            capture_exception(e)
            return None

    def _update_token(self, token: str, expires_at: datetime) -> None:
        """Atualiza o token"""
        self.token = token
        self.expires_at = expires_at

    def _request_token(self) -> Response:
        """Faz a requisição para obter o token"""
        try:
            return requests.post(
                self.url_auth,
                headers=self.headers,
                data=self.auth_data,
                timeout=5,
                verify=False,
            ).json()

        except requests.exceptions.MissingSchema as e:
            raise Exception("URL de API inválida") from e

        except Exception as e:
            capture_exception(e)
            raise Exception("Erro ao obter o token") from e

    def _verify_cache(self) -> bool:
        """Verifica se o token está no cache"""
        if cached_token := get_cache("emailapi_token"):
            self.token = cached_token.token
            self.expires_at = cached_token.expires_at
            return True
        return False

    def send_email(self, subject: str, message: str, emails: list) -> bool:
        """Envia o e-mail de redefinição de senha"""

        try:
            request = requests.post(
                self.url_send_email,
                json={
                    "assunto": subject,
                    "mensagem": message,
                    "emails": emails,
                },
                headers={
                    "accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": self.get_token(),
                },
                verify=False,
            )

            return request.status_code == 200

        except requests.exceptions.MissingSchema as e:
            raise Exception(f"URL de API inválida: {self.url_send_email}") from e

        except Exception as e:
            capture_exception(e)
            raise Exception("Erro ao enviar o e-mail") from e

    def __str__(self) -> str:
        return self.token
