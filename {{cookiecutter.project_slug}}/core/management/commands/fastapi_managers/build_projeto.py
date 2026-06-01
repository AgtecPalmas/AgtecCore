import os
import shutil
import subprocess
from pathlib import Path

from decouple import config
from rich.prompt import Prompt

from base.settings import SYSTEM_NAME

from ..utils import Utils


class ProjetoBuild:
    def __init__(self, command):
        self.command = command
        self.fastapi_dir = command.fastapi_dir
        self.django_dir = command.path_root
        self.fastapi_project = Path(f"{command.path_command}/snippets/fastapi_project/")
        self.operation_system = command.operation_system

    def __create_base_project(self):
        """Decide a criação do projeto base FastAPI"""
        try:
            if Utils.check_dir(str(self.fastapi_dir)) and Utils.check_dir(
                f"{self.fastapi_dir}/core"
            ):
                if (
                    Prompt.ask(
                        "Alterações feitas nos arquivos\
                        \n[b red]authentication, core e usuario[/]\
                        \npoderão ser perdidos.\
                        \n\nProjeto base já existe, deseja sobrescrever?",
                        default="n",
                        choices=["s", "n"],
                    )
                    == "s"
                ):
                    self.__overwrite_project()
            else:
                self.__init_fastapi()

        except Exception as error:
            Utils.show_message(f"Ocorreu o erro {error} ao executar a criação")

    def __overwrite_project(self):
        """Sobrescreve o projeto FastAPI"""
        try:
            _ignore = shutil.ignore_patterns("__pycache__", "*.pyc")

            for dirname in ("core", "authentication", "usuario"):
                target = Path(self.fastapi_dir) / dirname
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(
                    self.fastapi_project / dirname,
                    target,
                    ignore=_ignore,
                )

            # atualiza .ia/ e AGENTS.md preservando customizações só de code
            ia_target = Path(self.fastapi_dir) / ".ia"
            if ia_target.exists():
                shutil.rmtree(ia_target)
            shutil.copytree(
                self.fastapi_project / ".ia",
                ia_target,
                ignore=_ignore,
            )

            agents_src = self.fastapi_project / "AGENTS.md"
            agents_dst = Path(self.fastapi_dir) / "AGENTS.md"
            shutil.copyfile(agents_src, agents_dst)

        except Exception as error:
            Utils.show_error(f"Error in __overwrite_project: {error}")

    def __init_fastapi(self) -> None:
        """Copia o projeto base do FastAPI substituindo arquivos existentes"""
        try:
            Utils.show_message("Criando o projeto Fastapi.")
            _ignore = shutil.ignore_patterns("__pycache__", "*.pyc")
            shutil.copytree(self.fastapi_project, self.fastapi_dir, ignore=_ignore)
            Utils.show_message("Projeto base criado com sucesso.")

        except Exception as error:
            Utils.show_error(f"Error in __init_Fastapi: {error}")

    def __copy_file_env_example_to_env(self) -> None:
        """Copiar o arquivo .env.example para .env"""

        try:
            path_env_example = Path(self.fastapi_dir, ".env.example")
            path_env = Path(self.fastapi_dir, ".env")
            if not path_env.exists():
                shutil.copyfile(path_env_example, path_env)

        except Exception as e:
            Utils.show_error(f"Error in __copy_file_env_example_to_env: {e}")

    def __update_env_file(self) -> None:
        """Atualiza o arquivo .env do projeto Fastapi com a SECRET_KEY do Django"""
        secret: str = config("SECRET_KEY")
        db_name: str = config("DB_NAME")
        db_user: str = config("DB_USER")
        db_password: str = config("DB_PASSWORD")
        project_name: str = f"{SYSTEM_NAME}_FastAPI"

        file = Path(self.fastapi_dir) / ".env"

        replace_dict = {
            "__secret_key__": secret,
            "__db_name__": db_name,
            "__db_user__": db_user,
            "__db_password__": db_password,
            "__project_name__": project_name,
        }

        with open(file, "r") as f:
            env_file = f.read()

        for key, value in replace_dict.items():
            env_file = env_file.replace(key, value)

        with open(file, "w") as f:
            f.write(env_file)
            f.truncate()

    def __update_ia_project_name(self) -> None:
        """Substitui __system_name__ pelo nome real do projeto em AGENTS.md e .ia/"""
        targets = [
            Path(self.fastapi_dir) / "AGENTS.md",
            Path(self.fastapi_dir) / ".ia",
        ]

        for target in targets:
            paths = [target] if target.is_file() else target.rglob("*.md")
            for md_file in paths:
                try:
                    content = md_file.read_text(encoding="utf-8")
                    if "__system_name__" in content:
                        md_file.write_text(
                            content.replace("__system_name__", SYSTEM_NAME),
                            encoding="utf-8",
                        )
                except Exception:
                    pass

    def build(self):
        try:
            self.__create_base_project()
            self.__copy_file_env_example_to_env()
            self.__update_env_file()
            self.__update_ia_project_name()

        except Exception as error:
            Utils.show_error(f"Error in build: {error}")
