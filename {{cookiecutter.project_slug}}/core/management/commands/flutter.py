import logging
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand

from base.settings import FLUTTER_APPS, ORGANIZATION_FLUTTER_NAME
from core.management.commands.constants.flutter import (
    DJANGO_TYPES,
    FLUTTER_TYPES,
    SQLLITE_TYPES,
)
from core.management.commands.flutter_managers import (
    AddPackagesBuilder,
    AnalisysOptionsBuilder,
    AuthAppBuilder,
    ColorsSchemeBuilder,
    ControllerBuilder,
    CustomColorsBuilder,
    CustomDIOBuilder,
    CustomDIOInterceptorsBuilder,
    CustomStyleBuilder,
    DataServiceLayerBuild,
    ExceptionClassBuilder,
    LoggerBuilder,
    MainFileBuilder,
    MixinsClassBuilder,
    ModelsBuilder,
    NamedRoutesBuilder,
    PagesBuilder,
    RegisterProviderControllerBuilder,
    SettingsControllerBuilder,
    SizedExtensionsBuilder,
    SourceFileBuilder,
    StringExtensionsBuilder,
    TranslateStringBuilder,
    UserInterfaceBuilder,
    UtilsBuilder,
    WidgetBuilder,
)
from core.management.commands.flutter_managers.utils import ignore_base_fields
from core.management.commands.utils import Utils

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
                self.models = (
                    (x, x.__name__.strip(), x.__name__.strip().lower())
                    for x in self.app.get_models()
                )
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
    help = """Manager responsável por analisar as classes de modelos do projeto Django para gerar os demais arquivos
    do projeto Django (templates, forms, views, urls, serializers) seguindo os arquivos de modelos, snippets, e também
    gerar o projeto Flutter correspondente às apps do Django"""

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
        self.flutter_dir = str(Path(f"{self.path_root}/Flutter/{self.project.lower()}"))

        self.project = self.project.replace("-", "").replace("_", "")
        self.flutter_project = f"{self.project}"

        self.core_dir = str(Path(f"{self.flutter_dir}/lib/core"))
        self.ui_dir = str(Path(f"{self.core_dir}/user_interface"))
        self.ui_extensions = str(Path(f"{self.core_dir}/extensions"))
        self.ui_extensions_file = str(
            Path(f"{self.ui_extensions}/size_screen_extension.dart")
        )
        self.ui_string_extensions_file = str(
            Path(f"{self.ui_extensions}/string_methods_extensions.dart")
        )

        self.config_file = str(Path(f"{self.core_dir}/config.dart"))
        self.util_file = str(Path(f"{self.core_dir}/util.dart"))
        self.snippet_dir = str(
            Path(f"{self.path_core}/management/commands/snippets/flutter")
        )

        self.app_configuration = str(Path(f"{self.flutter_dir}/lib/apps/configuracao"))
        self.app_configuration_page_file = str(
            Path(f"{self.app_configuration}/index.page.dart")
        )
        self.app_configuration_controller_file = str(
            Path(f"{self.app_configuration}/controller.dart")
        )
        self.app_configuration_profile_file = str(
            Path(f"{self.app_configuration}/model.dart")
        )
        self.app_configuration_cubit_file = str(
            Path(f"{self.app_configuration}/cubit.dart")
        )
        self.app_configuration_cubit_state_file = str(
            Path(f"{self.app_configuration}/state.dart")
        )

        self.current_app_model = None

    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )

    _django_types = DJANGO_TYPES

    _flutter_types = FLUTTER_TYPES

    _sqlite_types = SQLLITE_TYPES

    def add_arguments(self, parser):
        parser.add_argument("App", type=str, nargs="?")
        parser.add_argument("Model", type=str, nargs="?")
        parser.add_argument(
            "--app", action="store_true", dest="app", help="Criar a App e seus models"
        )
        parser.add_argument(
            "--app_model",
            action="store_true",
            dest="app_model",
            help="Criar a App e o Model informado",
        )
        parser.add_argument(
            "--main", action="store_true", dest="main", help="Renderizar a main.dart"
        )
        parser.add_argument(
            "--yaml", action="store_true", dest="yaml", help="Refatorando o YAML"
        )
        parser.add_argument(
            "--init_cubit",
            action="store_true",
            dest="init_cubit",
            help="Gerar o projeto Flutter utilizando o Cubit como gerencia de estado.",
        )
        parser.add_argument(
            "--clear", action="store_true", dest="clear", help="Limpar projeto flutter."
        )
        parser.add_argument(
            "--routers",
            action="store_true",
            dest="routers",
            help="Criar o arquivo de rotas nomeadas.",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            dest="all",
            help="Criar o projeto Flutter e todos os arquivos necessários.",
        )

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
                    f"br.com.{self.organization_flutter_name}",
                    "--platforms",
                    "android,ios",
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

    def _build_auth_app(self):
        try:
            AuthAppBuilder(command=self).build()
        except Exception as error:
            Utils.show_error(f"Error in __build_auth_app {error}")

    def _register_providers_controller(self) -> tuple:
        try:
            return RegisterProviderControllerBuilder(command=self).build()
        except Exception as error:
            Utils.show_error(f"Error in _register_providers_controller: {error}")
            return None, None

    def _build_widget(self, app):
        try:
            __widget_file = Path(f"{app.get_path_views_dir()}/widget.dart")
            if Utils.check_file_is_locked(__widget_file):
                return
            WidgetBuilder(command=self, app=app).build()
        except Exception as error:
            Utils.show_error(f"Error in _build_widget {error}")

    def _build_exception_class(self):
        try:
            _path_directory = Path(f"{self.flutter_dir}/lib/core/exceptions")
            if not Utils.check_dir(_path_directory):
                os.makedirs(_path_directory)
            ExceptionClassBuilder(command=self).build()

        except Exception as error:
            Utils.show_error(f"Error in _build_exception_class: {error}")

    def _build_custom_dio_interceptors(self):
        try:
            _path = Path(f"{self.flutter_dir}/lib/core/dio/interceptors")
            if not Utils.check_dir(_path):
                os.makedirs(_path)
            CustomDIOInterceptorsBuilder(command=self).build()
        except Exception as error:
            Utils.show_error(f"Error in __build_custom_dio_interceptors {error}")

    def _build_custom_dio(self):
        try:
            _path_directory = Path(f"{self.flutter_dir}/lib/core/dio")
            if not Utils.check_dir(_path_directory):
                os.makedirs(_path_directory)
            CustomDIOBuilder(command=self).build()
        except Exception as error:
            Utils.show_error(f"Error in __build_custom_dio {error}")

    def _build_custom_style(self):
        try:
            if not Utils.check_dir(self.ui_dir):
                os.makedirs(self.ui_dir)
            CustomStyleBuilder(command=self).build()
        except Exception as error:
            Utils.show_error(f"Error in _build_custom_style {error}")

    def _build_sized_extensions(self):
        try:
            if not Utils.check_dir(self.ui_extensions):
                os.makedirs(self.ui_extensions)
            SizedExtensionsBuilder(command=self).build()
        except Exception as error:
            Utils.show_error(f"Error in _build_sized_extensions {error}")

    def _build_string_extensions(self):
        try:
            if not Utils.check_dir(self.ui_extensions):
                os.makedirs(self.ui_extensions)
            StringExtensionsBuilder(command=self).build()
        except Exception as error:
            Utils.show_error(f"Error in _build_string_extensions {error}")

    def _build_logger_file(self):
        try:
            if not Utils.check_dir(self.core_dir):
                os.makedirs(self.core_dir)
            LoggerBuilder(command=self).build()
        except Exception as error:
            Utils.show_error(f"Error in __build_logger_file {error}")

    def _build_colors_schemes_file(self):
        try:
            if not Utils.check_dir(self.core_dir):
                os.makedirs(self.core_dir)
            ColorsSchemeBuilder(command=self).build()
        except Exception as error:
            Utils.show_error(f"Error in _build_colors_schemes_file {error}")

    def _build_analysis_options_file(self):
        try:
            if not Utils.check_dir(self.core_dir):
                os.makedirs(self.core_dir)
            AnalisysOptionsBuilder(command=self).build()
        except Exception as error:
            Utils.show_error(f"Error in _build_colors_schemes_file {error}")

    def _controller_parser(self, app):
        try:
            if app.model is None:
                return
            ControllerBuilder(command=self, app=app).build()
        except Exception as error:
            Utils.show_error(f"Error in _controller_parser: {error}")

    def _data_local_and_service_layer_parser(self, app: AppModel):
        try:
            if app.model is None:
                return
            DataServiceLayerBuild(command=self, app=app).build()
        except Exception as error:
            Utils.show_error(f"Error in _data_local_and_service_layer_parser: {error}")

    def _model_parser(self, app):
        try:
            if app.model is None:
                return
            ModelsBuilder(command=self, app=app).build()
        except Exception as error:
            Utils.show_error(f"Error in _model_parser: {error}")

    def _build_custom_colors(self):
        try:
            # Verificando se o diretório das extensions existe
            if not Utils.check_dir(self.ui_dir):
                os.makedirs(self.ui_dir)
            CustomColorsBuilder(command=self).build()
        except Exception as error:
            Utils.show_error(f"Error in _build_custom_colors {error}")

    def _build_config_utils_file(self):
        try:
            if not Utils.check_dir(self.core_dir):
                os.makedirs(self.core_dir)
            UtilsBuilder(command=self).build()
        except Exception as error:
            Utils.show_error(f"Error in __build_utils {error}")

    def _build_named_routes(self):
        try:
            path_routes = Path(f"{self.flutter_dir}/lib/routers.dart")
            if Utils.check_file_is_locked(path_routes):
                return
            NamedRoutesBuilder(command=self, flutter_apps=FLUTTER_APPS).build()
        except Exception as error:
            Utils.show_error(f"Error in __create_name_route: {error}", exit=False)

    def _buid_settings(self):
        try:
            if not Utils.check_dir(self.app_configuration):
                os.makedirs(self.app_configuration)
                SettingsControllerBuilder(command=self).build()
        except Exception as error:
            Utils.show_error(f"Error in _buid_settings: {error}")

    def _build_user_interface(self):
        try:
            if not Utils.check_dir(self.ui_dir):
                os.makedirs(self.ui_dir)
            UserInterfaceBuilder(command=self).build()
        except Exception as error:
            Utils.show_error(f"Error in _build_user_interface: {error}")

    def _build_user_interface_mixins(self):
        try:
            if not Utils.check_dir(self.ui_dir):
                os.makedirs(self.ui_dir)
            MixinsClassBuilder(command=self).build()
        except Exception as error:
            Utils.show_error(f"Error in _build_user_interface: {error}")

    def _add_packages(self):
        try:
            AddPackagesBuilder(command=self).build()
        except Exception as error:
            Utils.show_error(f"Error in _add_packages: {error}")

    def _build_translate_strings(self):
        try:
            TranslateStringBuilder(command=self).build()
        except Exception as error:
            Utils.show_error(f"Error in _build_translate_strings: {error}")

    def _create_source_from_model(self):
        Utils.show_message("Criando as apps baseado na App e no Model")
        try:
            Utils.show_core_box(f"App {self.current_app_model.app_name}", tipo="app")

            self._create_source_files(
                self.current_app_model.app_name, self.current_app_model.model_name
            )
        except Exception as error:
            Utils.show_error(f"Error in __create_source_from_model: {error}")

    def _create_source_from_generators(self):
        try:
            Utils.show_core_box(f"App {self.current_app_model.app_name}", tipo="app")

            with Utils.ProgressBar() as bar:
                task = bar.add_task("", total=len(self.current_app_model.models))
                for i, model in enumerate(self.current_app_model.models):
                    bar.update(
                        task,
                        description=f"Gerando App [b green]{self.current_app_model.app_name}[/]:[b cyan]{model[1]}[/] - [{i+1}/{len(self.current_app_model.models)}]",
                    )
                    self._create_source_files(self.current_app_model.app_name, model[1])
                    bar.advance(task, 1)

        except Exception as error:
            Utils.show_error(f"Error in __create_source_from_generators: {error}")

    def _create_source_files(self, app_name, model_name):
        try:
            if app_name is None:
                Utils.show_message("É necessário passar a App")
                return

            if model_name is None:
                Utils.show_message("É necessário passar o Model")
                return

            Utils.show_core_box(f"Model {app_name}:{model_name}", tipo="model")

            _source_class = AppModel(self.flutter_dir, app_name, model_name)

            SourceFileBuilder(
                command=self,
                source_app=_source_class,
                app_name=app_name,
                model_name=model_name,
            ).build()

            PagesBuilder(command=self, source_app=_source_class).build()
            self._build_widget(_source_class)
            self._model_parser(_source_class)
            self._data_local_and_service_layer_parser(_source_class)
            self._controller_parser(_source_class)

        except Exception as error:
            Utils.show_error(f"Error in _create_source_file: {error}")

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
            self._build_auth_app()
            self._build_flutter()

            self._build_user_interface()
            self._build_user_interface_mixins()
            self._build_named_routes()
            self._buid_settings()
            self._build_exception_class()
            self._build_custom_dio()
            self._build_custom_dio_interceptors()
            self._build_custom_colors()
            self._build_custom_style()
            self._build_translate_strings()
            self._build_logger_file()
            self._build_colors_schemes_file()
            self._build_analysis_options_file()
            self._build_string_extensions()
            self._build_sized_extensions()
            self._build_config_utils_file()
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
