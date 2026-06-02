import subprocess

from .constants.formatters import ISORT, DJLINT, RUFF_FORMAT, RUFF_CHECK
from .utils import Utils


def run_subprocess_silently(command: str) -> bool:
    """Método para executar um comando no terminal silenciosamente"""
    result = subprocess.run(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=True,
    )
    return result.returncode == 0


class PythonFormatter:
    """Classe para aplicar os formatters no projeto"""

    def __init__(self, path: str):
        self.path = path

    def apply_ruff(self) -> None:
        """Método para aplicar lint e formatação usando Ruff"""
        try:
            # Corrige problemas automaticamente (lint + imports + etc)
            if not run_subprocess_silently(f"{RUFF_CHECK} {self.path}"):
                Utils.show_message(
                    f"Falha ao executar Ruff check em {self.path}",
                    emoji="warning",
                    border_color="yellow",
                )

            # Formata o código (equivalente ao black)
            if not run_subprocess_silently(f"{RUFF_FORMAT} {self.path}"):
                Utils.show_message(
                    f"Falha ao executar Ruff format em {self.path}",
                    emoji="warning",
                    border_color="yellow",
                )

        except Exception as error:
            Utils.show_message(f"Error in PythonFormatter.apply_ruff: {error}")

    def apply_isort(self) -> None:
        """Método para aplicar o isort no arquivo"""
        try:
            if not run_subprocess_silently(f"{ISORT} {self.path}"):
                Utils.show_message(
                    f"Falha ao executar isort em {self.path}",
                    emoji="warning",
                    border_color="yellow",
                )
        except Exception as error:
            Utils.show_message(f"Error in PythonFormatter.apply_isort: {error}")

    def format(self) -> None:
        """Método para aplicar os formatters no arquivo"""
        self.apply_isort()
        self.apply_ruff()


class HtmlFormatter:
    """Classe para aplicar os formatters no projeto"""

    def __init__(self, path: str):
        self.path = path

    def apply_djlint(self) -> None:
        """Método para aplicar o djlint no arquivo"""
        try:
            run_subprocess_silently(f"{DJLINT} {self.path}")
        except Exception as error:
            Utils.show_message(f"Error in Utils.apply_formatters_html: {error}")

    def format(self) -> None:
        """Método para aplicar os formatters no arquivo"""
        self.apply_djlint()
