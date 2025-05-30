import base64
import hashlib
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from django.conf import settings


class CPFAnonymizer:
    def __init__(self, key: str | None = None):
        # Converte a chave alfanumérica para uma chave de 32 bytes usando SHA-256
        if key is None:
            key = settings.KEY_ANONYMIZATION_CPF
        self.key = hashlib.sha256(key.encode('utf-8')).digest()
        self.backend = default_backend()

    @staticmethod
    def _pad(data: bytes) -> bytes:
        """
        Adiciona preenchimento (padding) aos dados para que seu tamanho seja múltiplo do tamanho do bloco do algoritmo AES.

        Parâmetros:
            data (bytes): Os dados em bytes que precisam ser preenchidos.

        Retorno:
            bytes: Os dados preenchidos.

        Descrição:
            1. Cria um padder (preenchedor) usando o esquema de preenchimento PKCS7 com o tamanho do bloco do algoritmo AES.
            2. Aplica o padder aos dados fornecidos e finaliza o processo de preenchimento.
            3. Retorna os dados preenchidos.
        """
        _padder = padding.PKCS7(algorithms.AES.block_size).padder()
        return _padder.update(data) + _padder.finalize()

    @staticmethod
    def _unpad(data: bytes) -> bytes:
        """
        Remove o preenchimento (padding) dos dados que foram previamente preenchidos para que seu tamanho seja múltiplo do tamanho do bloco do algoritmo AES.

        Parâmetros:
            data (bytes): Os dados em bytes que precisam ter o preenchimento removido.

        Retorno:
            bytes: Os dados sem o preenchimento.

        Descrição:
            1. Cria um unpadder (removedor de preenchimento) usando o esquema de preenchimento PKCS7 com o tamanho do bloco do algoritmo AES.
            2. Aplica o unpadder aos dados fornecidos e finaliza o processo de remoção do preenchimento.
            3. Retorna os dados sem o preenchimento.
        """
        _unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        return _unpadder.update(data) + _unpadder.finalize()

    def pack_cpf(self, cpf: str) -> str | None:
        """
        Criptografa um CPF usando AES e codifica o resultado em Base64.

        Parâmetros:
            cpf (str): O CPF a ser criptografado.

        Retorno:
            str: O CPF criptografado e codificado em Base64.

        Descrição:
            1. Gera um vetor de inicialização (IV) aleatório de 16 bytes usando os.urandom(16).
            2. Cria um objeto Cipher com o algoritmo AES, modo CBC e o IV gerado.
            3. Cria um encriptador a partir do objeto Cipher.
            4. Adiciona preenchimento (padding) ao CPF para que seu tamanho seja múltiplo do tamanho do bloco do algoritmo AES.
            5. Criptografa os dados preenchidos usando o encriptador.
            6. Codifica o IV concatenado com os dados criptografados em Base64 e retorna como string.
        """
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        padded_data = self._pad(cpf.encode('utf-8'))
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(iv + encrypted).decode('utf-8')

    def unpack_cpf(self, packed: str) -> str:
        """
        Descriptografa o valor do CPF encriptado com AES e codificado em Base64 para recuperar o CPF original.

        Parâmetros:
            packed (str): O CPF encriptado com AES e codificado em Base64.

        Retorno:
            str: O valor do CPF descriptografado (original).

        Descrição:
            1. Decodifica a string Base64 para obter os bytes encriptados.
            2. Extrai os primeiros 16 bytes como o vetor de inicialização (IV).
            3. Os bytes restantes são os dados encriptados.
            4. Cria um objeto Cipher com o algoritmo AES, modo CBC e o IV extraído.
            5. Cria um decriptador a partir do objeto Cipher.
            6. Descriptografa os dados encriptados usando o decriptador.
            7. Remove o preenchimento (padding) dos dados descriptografados.
            8. Decodifica os bytes resultantes para uma string UTF-8 e retorna o CPF original.
        """
        packed_bytes = base64.b64decode(packed.encode('utf-8'))
        iv = packed_bytes[:16]
        encrypted = packed_bytes[16:]
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(encrypted) + decryptor.finalize()
        return self._unpad(decrypted_padded).decode('utf-8')

    def compare_cpf(self, packed: str, cpf: str) -> bool:
        """
        Compara um CPF criptografado com um CPF fornecido.

        Parâmetros:
            packed (str): O CPF criptografado e codificado em Base64.
            cpf (str): O CPF em formato de string que será comparado.

        Retorno:
            bool: Retorna True se o CPF descriptografado for igual ao CPF fornecido, caso contrário, False.

        Descrição:
            1. Descriptografa o valor do CPF criptografado usando o método unpack_cpf.
            2. Compara o CPF descriptografado com o CPF fornecido.
            3. Retorna True se os CPFs forem iguais, caso contrário, retorna False.
        """
        decoded = self.unpack_cpf(packed)
        return decoded == cpf
