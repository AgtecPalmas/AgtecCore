import shlex
import subprocess
import sys
from pathlib import Path

from .constants.formatters import DJLINT, ISORT, RUFF_CHECK, RUFF_FORMAT
from .utils import Utils


def _resolve_cmd(command: str) -> list[str]:
    """Resolve o binário do comando para o path absoluto no venv atual.

    Quando manage.py é chamado via .venv/bin/python sem ativar o venv,
    os subprocessos não herdam o PATH do venv. Usar sys.executable para
    derivar o bin/ do venv garante que ruff seja encontrado.
    """
    parts = shlex.split(command)
    venv_bin = Path(sys.executable).parent
    binary = venv_bin / parts[0]
    if binary.exists():
        parts[0] = str(binary)
    return parts


def run_subprocess_silently(command: str, ok_codes: tuple = (0,)) -> bool:
    """Método para executar um comando no terminal silenciosamente"""
    result = subprocess.run(
        _resolve_cmd(command),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode in ok_codes


class PythonFormatter:
    """Classe para aplicar os formatters no projeto"""

    def __init__(self, path: str):
        self.path = path

    def apply_ruff(self) -> None:
        """Método para aplicar lint e formatação usando Ruff"""
        try:
            # exit 1 = encontrou e corrigiu violações (comportamento normal, não erro)
            if not run_subprocess_silently(f"{RUFF_CHECK} {self.path}", ok_codes=(0, 1)):
                Utils.show_message(
                    f"Falha ao executar Ruff check em {self.path}",
                    emoji="warning",
                    border_color="yellow",
                )

            if not run_subprocess_silently(f"{RUFF_FORMAT} {self.path}"):
                Utils.show_message(
                    f"Falha ao executar Ruff format em {self.path}",
                    emoji="warning",
                    border_color="yellow",
                )

        except Exception as error:
            Utils.show_message(f"Error in PythonFormatter.apply_ruff: {error}")

    def apply_isort(self) -> None:
        """Método para aplicar o isort no arquivo — float-to-top move imports
        que aparecem após código não-import para o topo do arquivo"""
        try:
            if not run_subprocess_silently(f"{ISORT} {self.path}", ok_codes=(0, 1)):
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
