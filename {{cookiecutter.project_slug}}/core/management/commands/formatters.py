import subprocess

from .constants.formatters import AUTOFLAKE, AUTOPEP8, BLACK, DJLINT, ISORT
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

    def apply_autoflake(self) -> None:
        """Método para aplicar o autoflake no arquivo"""
        try:
            run_subprocess_silently(f"{AUTOFLAKE} {self.path}")
        except Exception as error:
            Utils.show_message(f"Error in PythonFormatter.apply_autoflake: {error}")

    def apply_autopep8(self) -> None:
        """Método para aplicar o autopep8 no arquivo"""
        try:
            run_subprocess_silently(f"{AUTOPEP8} {self.path}")
        except Exception as error:
            Utils.show_message(f"Error in PythonFormatter.apply_autopep8: {error}")

    def apply_isort(self) -> None:
        """Método para aplicar o isort no arquivo"""
        try:
            run_subprocess_silently(f"{ISORT} {self.path}")
        except Exception as error:
            Utils.show_message(f"Error in PythonFormatter.apply_isort: {error}")

    def apply_black(self) -> None:
        """Método para aplicar o black no arquivo"""
        try:
            run_subprocess_silently(f"{BLACK} {self.path}")
        except Exception as error:
            Utils.show_message(f"Error in PythonFormatter.apply_black: {error}")

    def format(self) -> None:
        """Método para aplicar os formatters no arquivo"""
        self.apply_autoflake()
        self.apply_autopep8()
        self.apply_isort()
        self.apply_black()


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
