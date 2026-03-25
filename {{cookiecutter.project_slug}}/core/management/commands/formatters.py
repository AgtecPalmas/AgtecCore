import subprocess

from .constants.formatters import DJLINT, RUFF_FORMAT
from .utils import Utils


def run_subprocess_silently(command: str) -> None:
    """Método para executar um comando no terminal silenciosamente"""
    subprocess.run(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=True,
    )


class PythonFormatter:
    """Classe para aplicar os formatters no projeto"""

    def __init__(self, path: str):
        self.path = path

    def apply_ruff(self) -> None:
        """Método para aplicar lint e formatação usando Ruff"""
        try:
            # Corrige problemas automaticamente (lint + imports + etc)
            run_subprocess_silently(f"{RUFF_CHECK} {self.path}")

            # Formata o código (equivalente ao black)
            run_subprocess_silently(f"{RUFF_FORMAT} {self.path}")

        except Exception as error:
            Utils.show_message(f"Error in PythonFormatter.apply_ruff: {error}")

    def format(self) -> None:
        """Método para aplicar os formatters no arquivo"""
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
