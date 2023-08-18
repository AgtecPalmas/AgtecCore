import os
from pathlib import Path

from core.management.commands.utils import Utils


class AuthAppBuilder:
    def __init__(self, command) -> None:
        self._command = command
        self._snippet_dir = Path(f"{self._command.path_command}/snippets/flutter/cubit")
        self._flutter_dir = self._command.flutter_dir
        self._auth_dir = Path(f"{self._flutter_dir}/lib/apps/auth")

    def build(self):
        """Método responsável por criar a app de autenticação no projeto Flutter utilizando o Firebase como back end de
        autenticação. Já traz por padrão os métodos de autentica por:
            1 - Email
            2 - Google Account
            3 - Facebook
            4 - Apple Account
        É necessário trabalhar na geração dos tokens de acesso, bem como criar um projeto no Firebase e habilitar
        os tipos de autenticação que desejam implementar.
        """
        try:
            if Utils.check_dir(self._auth_dir):
                return

            # Criando o diretório
            os.makedirs(self._auth_dir)

            # Criando o diretório pages
            os.makedirs(Path(self._auth_dir, "pages"))

            self._build_data_file()
            self._build_model_file()
            self._build_service_file()
            self._build_state_file()
            self._build_controller_file()
            self._build_pages_directory()
            
        except Exception as error:
            Utils.show_error(f"Erro ao executar build do main file: {error}")

    def _build_data_file(self):
        _snippet = Path(f"{self._snippet_dir}/auth_data.txt")
        _target_file = Path(f"{self._auth_dir}/data.dart")
        try:
            _content = Utils.get_snippet(_snippet)
            _content = _content.replace("$project$", self._command.flutter_project)
            with open(_target_file, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as error:
            Utils.show_error(f"Erro ao executar build do data file: {error}")

    def _build_model_file(self):
        try:
            _snippet = Path(f"{self._snippet_dir}/auth_model.txt")
            _target_file = Path(f"{self._auth_dir}/model.dart")
            _content = Utils.get_snippet(_snippet)
            with open(_target_file, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as error:
            Utils.show_error(f"Erro ao executar build do model file: {error}")

    def _build_service_file(self):
        try:
            _snippet = Path(f"{self._snippet_dir}/auth_service.txt")
            _target_file = Path(f"{self._auth_dir}/service.dart")
            _content = Utils.get_snippet(_snippet)
            with open(_target_file, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as error:
            Utils.show_error(f"Erro ao executar build do service file: {error}")

    def _build_state_file(self):
        try:
            _snippet = Path(f"{self._snippet_dir}/auth_state.txt")
            _target_file = Path(f"{self._auth_dir}/state.dart")
            _content = Utils.get_snippet(_snippet)
            with open(_target_file, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as error:
            Utils.show_error(f"Erro ao executar build do service file: {error}")

    def _build_controller_file(self):
        try:
            _snippet = Path(f"{self._snippet_dir}/auth_app.txt")
            _target_file = Path(f"{self._auth_dir}/cubit.dart")
            _content = Utils.get_snippet(_snippet)
            with open(_target_file, "w", encoding="utf-8") as _file:
                _file.write(_content)
        except Exception as error:
            Utils.show_error(f"Erro ao executar build do service file: {error}")

    def _build_pages_directory(self):
        try:
            for page in ["index", "signin", "signup", "termo_uso"]:
                _target_file = Path(f"{self._auth_dir}/pages/{page}.dart")
                _content = Utils.get_snippet(Path(f"{self._snippet_dir}/auth_{page}_page.txt"))
                with open(_target_file, "w", encoding="utf-8") as _file:
                    _file.write(_content)
        except Exception as error:
            Utils.show_error(f"Erro ao executar build do pages directory: {error}")
