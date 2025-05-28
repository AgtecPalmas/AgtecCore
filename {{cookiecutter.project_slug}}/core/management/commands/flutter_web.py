import logging
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

from base.settings import FLUTTER_APPS, ORGANIZATION_FLUTTER_NAME
from core.management.commands.constants.flutter import (
    DJANGO_TYPES,
    FLUTTER_TYPES,
    SQLLITE_TYPES,
)
from core.management.commands.flutter_managers import (
    MainFileWebBuilder
)
from core.management.commands.flutter_managers.utils import ignore_base_fields
from core.management.commands.utils import Utils
from django.apps import apps
from django.core.management.base import BaseCommand

logger = logging.getLogger("django_debug")



class AppModel:
    def __init__(self, path_flutter, app_name, model_name=None):
        try:
            self.path_flutter = path_flutter
            self.models = None
            self.model = None
            self.app_name = str(app_name).strip()
            self.app_name_lower = self.app_name.lower()
            self.app = apps.get_app_config(self.app_name_lower)
            self.model_name = str(model_name).strip()
            self.model_name_lower = self.model_name.lower()
            if model_name is not None:
                self.model = self.app.get_model(self.model_name)
            else:
                self.models = [
                    (x, x.__name__.strip(), x.__name__.strip().lower())
                    for x in self.app.get_models()
                ]
            self.operation_system = platform.system().lower()

        except Exception as error:
            raise error

    def get_path_app_dir(self) -> Path:
        """
        Retorna o path da app do projeto Flutter

        Returns
        -------
        Path
            Path da app do projeto Flutter
        """
        try:
            _path_flutter = self.path_flutter
            _app_name_lower = self.app_name_lower
            return Path(f"{_path_flutter}/lib/apps/{_app_name_lower}")
        except Exception as error:
            Utils.show_error(f"Error in get_path_app_dir: {error}")

    def get_path_app_model_dir(self) -> Path:
        """
        Retorna o path do model da app do projeto Flutter

        Returns
        -------
        Path
            Path do model da app do projeto Flutter
        """
        try:
            _path_flutter = self.path_flutter
            _app_name_lower = self.app_name_lower
            _model_name_lower = self.model_name_lower
            return Path(
                f"{_path_flutter}/lib/apps/{_app_name_lower}/{_model_name_lower}"
            )
        except Exception as error:
            Utils.show_error(f"Error in get_path_app_model_dir {error}")

    def get_path_views_dir(self) -> Path:
        """
        Retorna o path das views da app do projeto Flutter

        Returns
        -------
        Path
            Path das views da app do projeto Flutter
        """
        try:
            _path_flutter = self.path_flutter
            _app_name_lower = self.app_name_lower
            _model_name_lower = self.model_name_lower
            return Path(
                f"{_path_flutter}/lib/apps/{_app_name_lower}/{_model_name_lower}/pages/"
            )
        except Exception as error:
            Utils.show_error(f"Error in get_path_views_dir {error}")

    def get_path_files_views(self) -> list[str]:
        """
        Returns
        -------
        list[str]
            Lista contendo os paths de destino dos arquivos de views, create, detail, index, list, update.
        """
        try:
            _path_flutter = self.path_flutter
            _app_name_lower = self.app_name_lower
            _model_name_lower = self.model_name_lower
            _path_root = (
                f"{_path_flutter}/lib/apps/{_app_name_lower}/{_model_name_lower}/pages"
            )
            _create = Path(f"{_path_root}/create.dart")
            _detail = Path(f"{_path_root}/detail.dart")
            _index = Path(f"{_path_root}/index.dart")
            _list = Path(f"{_path_root}/list.dart")
            _update = Path(f"{_path_root}/update.dart")
            return _create, _detail, _index, _list, _update
        except Exception as error:
            Utils.show_error(f"Error in {error}")

    def get_path_data_file(self) -> Path:
        """
        Método para retornar o path do arquivo data.dart

        Returns
        -------
        Path
            Path do arquivo data.dart
        """
        try:
            _path_flutter = self.path_flutter
            _app_name_lower = self.app_name_lower
            _model_name_lower = self.model_name_lower
            return Path(
                f"{_path_flutter}/lib/apps/{_app_name_lower}/{_model_name_lower}/data.dart"
            )
        except Exception as error:
            Utils.show_error(f"Error in get_path_data_file: {error}")

    def get_path_model_file(self) -> Path:
        """
        Retorna o path do arquivo model.dart

        Returns
        -------
        Path
            Path do arquivo model.dart
        """
        try:
            _path_flutter = self.path_flutter
            _app_name_lower = self.app_name_lower
            _model_name_lower = self.model_name_lower
            return Path(
                f"{_path_flutter}/lib/apps/{_app_name_lower}/{_model_name_lower}/model.dart"
            )
        except Exception as error:
            Utils.show_error(f"Error in get_path_model_file {error}")

    def get_path_cubit_file(self) -> Path:
        """
        Retorna o path do arquivo cubit.dart

        Returns
        -------
        Path
            Path do arquivo cubit.dart
        """
        try:
            _path_flutter = self.path_flutter
            _app_name_lower = self.app_name_lower
            _model_name_lower = self.model_name_lower
            return Path(
                f"{_path_flutter}/lib/apps/{_app_name_lower}/{_model_name_lower}/cubit.dart"
            )
        except Exception as error:
            Utils.show_error(f"Error in get_path_provider_file {error}")

    def get_path_cubit_state_file(self) -> Path:
        """
        Retorna o path do arquivo state.dart

        Returns
        -------
        Path
            Path do arquivo state.dart
        """
        try:
            _path_flutter = self.path_flutter
            _app_name_lower = self.app_name_lower
            _model_name_lower = self.model_name_lower
            return Path(
                f"{_path_flutter}/lib/apps/{_app_name_lower}/{_model_name_lower}/state.dart"
            )
        except Exception as error:
            Utils.show_error(f"Error in get_path_provider_file {error}")

    def get_path_service_file(self) -> Path:
        """
        Retorna o path do arquivo service.dart

        Returns
        -------
        Path
            Path do arquivo service.dart
        """
        try:
            _path_flutter = self.path_flutter
            _app_name_lower = self.app_name_lower
            _model_name_lower = self.model_name_lower
            return Path(
                f"{_path_flutter}/lib/apps/{_app_name_lower}/{_model_name_lower}/service.dart"
            )
        except Exception as error:
            Utils.show_error(f"Error in get_path_service_file {error}")

    def print_string(self):
        """
        print_string _summary_
        """
        print("Models (Generator)")
        if self.models is not None:
            for __model in self.models:
                print(f"Model: {__model[0]} Name: {__model[1]} - {__model[2]}")
        else:
            print("None")

    def get_app_model_name(self, title_case=False):
        """Método responsável por retornar o nome do Models das app do projeto Django"""
        try:
            if title_case is True:
                return f"{self.app_name.title()}{self.model_name}"
            return f"{self.app_name}{self.model_name}"
        except Exception as error:
            Utils.show_message(f"Error in get_app_model_name: {error}")
            return None


class Command(BaseCommand):
    help = """Manager responsável por criar o projeto Flutter Web"""

    def __init__(self):
        super().__init__()
        self.path_root: Path = os.getcwd()
        self.path_core: Path = os.path.join(self.BASE_DIR, "core")
        self.path_base: Path = Path(f"{self.path_root}/base")
        self.organization_flutter_name = ORGANIZATION_FLUTTER_NAME

        self.operation_system = platform.system().lower()
        self.path_command = Path(__file__).parent

        _path_project = os.getcwd()

        # Refatorando para Path
        self.project = Path.cwd().parts[-1]
        self.path_root = Path(*Path.cwd().parts[:-2]).as_posix()
        self.flutter_dir = str(Path(f"{self.path_root}/FlutterWeb/{self.project.lower()}"))

        self.project = self.project.replace("-", "").replace("_", "")
        self.flutter_project = f"{self.project}"
        self.core_dir = str(Path(f"{self.flutter_dir}/lib/core"))
        self.constants_dir = str(Path(f"{self.flutter_dir}/lib/constants"))

        self.current_app_model = None

    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )

    _django_types = DJANGO_TYPES

    _flutter_types = FLUTTER_TYPES

    _sqlite_types = SQLLITE_TYPES

    def _ignore_fields(self, field):
        try:
            return ignore_base_fields(field)
        except Exception as error:
            Utils.show_error(f"Error in _ignore_fields: {error}")

    def _init_flutter(self):
        try:
            if not Utils.check_dir(self.flutter_dir):
                Utils.show_message("Criando projeto Flutter")

                _cmd = [
                    "flutter",
                    "create",
                    "--project-name",
                    f"{self.flutter_project.lower()}",
                    "--org",
                    f"{self.organization_flutter_name}",
                    "--platforms",
                    "web",
                    f"{self.flutter_dir}",
                ]

                subprocess.call(
                    _cmd,
                    text=True,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                shutil.copyfile(
                    f"{self.snippet_dir}/README.md", f"{self.flutter_dir}/README.md"
                )
        except Exception as error:
            Utils.show_error(f"Error in _init_flutter: {error}")

    def _build_flutter(self):
        try:
            if Utils.check_dir(self.flutter_dir):
                Utils.show_message("Atualizando o arquivo de dependências.")
                self._add_packages()
                time.sleep(3)

                current_path = os.getcwd()
                os.chdir(self.flutter_dir)
                subprocess.run(
                    ["flutter", "pub", "get"],
                    text=True,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                os.chdir(current_path)

                Utils.show_message("Atualizando o arquivo main.dart.")
                self._replace_main()

        except Exception as error:
            Utils.show_error(f"Error in __build_flutter: {error}")

    def _replace_main(self):
        try:
            MainFileBuilder(command=self, flutter_apps=FLUTTER_APPS).build()
        except Exception as error:
            Utils.show_error(f"Error in __replace_main: {error}")

    def _check_flutter_installation(self) -> bool:
        if subprocess.call(
            ["flutter", "--version"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ):
            Utils.show_error("Flutter não está instalado na máquina.")
            return False
        return True

    def call_methods(self, options):
        if self._check_flutter_installation() is False:
            Utils.show_error("Flutter não está instalado na máquina.", exit=True)
            return

        if options["main"]:
            self._replace_main()
            return
        elif options["yaml"]:
            self._add_packages()
            return
        elif options["routers"]:
            self._build_named_routes()
            return
        elif options["clear"]:
            self._clear_project()
            sys.exit()

        else:
            self._init_flutter()
            self._build_flutter()
        return

    def __verify_valid_flags(self, options):
        """Verificações comuns para as flags"""
        if not bool(
            (
                options.get("all")
                or options.get("clear")
                or options.get("main")
                or options.get("routers")
                or options.get("yaml")
            )
        ):
            Utils.show_error(
                "Para gerar o projeto é necessário informar uma das flags:\
                \n[b cyan]--all\n--clear\n--main\n--routers\n--yaml[/]"
            )

    def handle(self, *args, **options):
        Utils.show_core_box("", tipo="core")
        app = options["App"] or None
        model = options["Model"] or None

        self.__verify_valid_flags(options)
        if self._check_flutter_installation() is False:
            return

        if app is None and model is None and not FLUTTER_APPS:
            Utils.show_error(
                "Você não configurou o FLUTTER_APPS no settings e também não informou uma APP para ser gerada.",
            )
            return

        if app:
            try:
                apps.get_app_config(app)
            except LookupError:
                Utils.show_error(f"App {app} não encontrada")
                return

            if model:
                try:
                    apps.get_app_config(app).get_model(model)
                except LookupError:
                    Utils.show_error(f"Modelo {model} não encontrado")
                    return

        if app and model:
            if Utils.contain_number(app) or Utils.contain_number(model):
                Utils.show_message("Nome da app ou do model contendo números")
                return

            self.current_app_model = AppModel(self.flutter_project, app, model)
            with Utils.ProgressBar() as bar:
                bar.add_task(
                    f"Gerando App [b green]{app}[/]:[b cyan]{model}[/] - [1/1]",
                    total=1,
                )
                self._create_source_from_model()

        elif app and model is None:
            if Utils.contain_number(app):
                Utils.show_error("Nome da app contendo números")
                return

            self.current_app_model = AppModel(self.flutter_project, app)
            self._create_source_from_generators()

        elif not FLUTTER_APPS:
            Utils.show_error("Não foram informadas as APPS a serem mapeadas")
            return

        else:
            self.call_methods(options)

            for _app in FLUTTER_APPS:
                self.current_app_model = AppModel(self.flutter_project, _app)
                self._create_source_from_generators()

        Utils.show_message("Processo concluído", title=True, emoji="rocket")

    def _clear_project(self, path=None):
        try:
            _path = path or f"{self.flutter_dir}"
            shutil.rmtree(_path)

        except Exception as error:
            Utils.show_message(f"Error in __clear_project: {error}")
