import os
import platform
import subprocess
import sys
import time
from base.settings import API_PATH, FLUTTER_APPS, SYSTEM_NAME
from core.management.commands.parser_content import ParserContent
from core.management.commands.utils import Utils
from core.models import Base
from django.apps import apps
from django.core.management.base import BaseCommand
from enum import Enum
from pathlib import Path


class AppModel:
    """Classe responsável pelo processo de análise do models do Django para
    gerar os arquivos tantos do projeto Django como do Flutter

    Arquivos Django Gerados:
        1 - templates (create, list, update, detail, delete)
        2 - forms
        3 - views
        4 - urls
        5 - api_views
        6 - api_urls
        7 - serializers

    Arguments:
        path_flutter {String} -- Caminho do projeto Flutter
        app_name {String} -- Nome do app do projeto que será mapeada para gerar os arquivos do projeto

    Keyword Arguments:
        model_name {String} -- Nome do models a ser mapeado, caso não seja passado o script fará a
                               análise de todos os models da app (default: {None})
    """

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
                self.models = ((x, x.__name__.strip(), x.__name__.strip().lower()) for x in self.app.get_models())
            self.operation_system = platform.system().lower()

        except Exception as error:
            raise error

    def get_path_app_dir(self):
        """Método para retornar o caminho aonde será criado o projeto Flutter"""
        try:
            return Path("{}/lib/apps/{}".format(self.path_flutter, self.app_name_lower))
        except Exception as error:
            Utils.show_error(
                f"Error in get_path_app_dir: {error}",
            )

    def get_path_app_model_dir(self):
        """Método para retornar o caminho aonde será criado a app Flutter correspondente à app do projeto Django"""
        try:
            return Path("{}/lib/apps/{}/{}".format(self.path_flutter, self.app_name_lower, self.model_name_lower))
        except Exception as error:
            Utils.show_error(
                f"Error in get_path_app_model_dir {error}",
            )

    def get_path_views_dir(self):
        """Método para retornar o caminho aonde será criado o diretório das páginas/telas da app no projeto Flutter"""
        try:
            return Path(
                "{}/lib/apps/{}/{}/pages/".format(self.path_flutter, self.app_name_lower, self.model_name_lower)
            )
        except Exception as error:
            Utils.show_error(
                f"Error in get_path_views_dir {error}",
            )

    def get_path_files_views(self):
        """
        Método para retornar a lista com os caminhos aonde serão criados os arquivos das
        páginas no projeto Flutter
        """
        try:
            __create = Path(
                "{}/lib/apps/{}/{}/pages/create.dart".format(
                    self.path_flutter, self.app_name_lower, self.model_name_lower
                )
            )
            __detail = Path(
                "{}/lib/apps/{}/{}/pages/detail.dart".format(
                    self.path_flutter, self.app_name_lower, self.model_name_lower
                )
            )
            __index = Path(
                "{}/lib/apps/{}/{}/pages/index.dart".format(
                    self.path_flutter, self.app_name_lower, self.model_name_lower
                )
            )
            __list = Path(
                "{}/lib/apps/{}/{}/pages/list.dart".format(
                    self.path_flutter, self.app_name_lower, self.model_name_lower
                )
            )
            __update = Path(
                "{}/lib/apps/{}/{}/pages/update.dart".format(
                    self.path_flutter, self.app_name_lower, self.model_name_lower
                )
            )

            return __create, __detail, __index, __list, __update
        except Exception as error:
            Utils.show_error(
                f"Error in get_path_files_views: {error}",
            )

    def get_path_data_file(self):
        """Método para retornar o o caminho aonde será criado o arquivo de persistência local do modelo no projeto
        Flutter"""
        try:
            return Path(
                "{}/lib/apps/{}/{}/data.dart".format(self.path_flutter, self.app_name_lower, self.model_name_lower)
            )
        except Exception as error:
            Utils.show_error(
                f"Error in get_path_data_file: {error}",
            )

    def get_path_model_file(self):
        """Método para retornar o o caminho aonde será criado o arquivo do modelo no projeto Flutter"""
        try:
            return Path(
                "{}/lib/apps/{}/{}/model.dart".format(self.path_flutter, self.app_name_lower, self.model_name_lower)
            )
        except Exception as error:
            Utils.show_error(
                f"Error in get_path_model_file {error}",
            )

    def get_path_cubit_file(self):
        """Método para retornar o o caminho aonde será criado o arquivo Cubit no projeto Flutter.
        Utilizado apenas nos projetos que utilizam a gerência de estado do Cubit (Package Padrão)
        """
        try:
            return Path(
                "{}/lib/apps/{}/{}/cubit.dart".format(self.path_flutter, self.app_name_lower, self.model_name_lower)
            )
        except Exception as error:
            Utils.show_error(
                f"Error in get_path_provider_file {error}",
            )

    def get_path_cubit_state_file(self):
        """Método para retornar o o caminho aonde será criado o arquivo state no projeto Flutter.
        Utilizado apenas nos projetos que utilizam a gerência de estado do Cubit (Package Padrão)
        """
        try:
            return Path(
                "{}/lib/apps/{}/{}/state.dart".format(self.path_flutter, self.app_name_lower, self.model_name_lower)
            )
        except Exception as error:
            Utils.show_error(
                f"Error in get_path_provider_file {error}",
            )

    def get_path_service_file(self):
        """Método para retornar o o caminho aonde será criado o arquivo service no projeto Flutter, responsável
        por acessar a APIRest utilizando o pacote dio.
        """
        try:
            return Path(
                "{}/lib/apps/{}/{}/service.dart".format(self.path_flutter, self.app_name_lower, self.model_name_lower)
            )
        except Exception as error:
            Utils.show_error(
                f"Error in get_path_service_file {error}",
            )

    def print_string(self):
        """Método auxiliar para imprimir no console/terminal do python dados sobre o parser do modelo"""

        print("Models (Generator)")
        if self.models is not None:
            for __model in self.models:
                print("Model: {} Name: {} - {}".format(__model[0], __model[1], __model[2]))
        else:
            print("None")

    def check_inherited_base(self, model):
        """Método para verificar se o model passado como parâmetro herda da classe Base do projeto Core.
        Apenas as classes que herdam de Base serão analisadas e consequentemente gerados os arquivos
        Django e Flutter."""
        try:
            __instance = apps.get_app_config(self.app_name_lower)
            __model = __instance.get_model(model)
            return issubclass(__model, Base)
        except Exception as error:
            Utils.show_message(f"Error in check_inherited_base: {error}")
            return False

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
        self.path_root = os.getcwd()
        self.path_core = os.path.join(self.BASE_DIR, "core")
        self.operation_system = platform.system().lower()

        _path_project = os.getcwd()

        # TODO Refatorar para utilizar o PathLib
        if self.operation_system == "windows":
            self.project = os.getcwd().split("\\")[-1:][0]
            self.flutter_dir = "{}\\Flutter\\{}".format("\\".join(os.getcwd().split("\\")[:-2]), self.project.lower())
            self.project = self.project.replace("-", "").replace("_", "")
            self.flutter_project = "{}".format(self.project)
            # self.utils_dir = "{}\\lib\\utils\\".format(self.flutter_dir)
            self.core_dir = "{}\\lib\\core\\".format(self.flutter_dir)
            self.ui_dir = "{}\\lib\\core\\user_interface\\".format(self.flutter_dir)
            self.ui_extensions = "{}\\lib\\core\\extensions".format(self.flutter_dir)
            self.ui_extensions_file = "{}\\lib\\core\\extensions\\size_screen_extension.dart".format(self.flutter_dir)
            self.ui_string_extensions_file = "{}\\lib\\core\\extensions\\string_methods_extensions.dart".format(
                self.flutter_dir
            )
            self.config_file = "{}\\lib\\core\\config.dart".format(self.flutter_dir)
            self.util_file = "{}\\lib\\core\\util.dart".format(self.flutter_dir)
            # self.process_controller_file = "{}\\lib\\utils\\process.controller.dart".format(self.flutter_dir)
            # self.process_provider_file = "{}\\lib\\utils\\process.provider.dart".format(self.flutter_dir)
            self.snippet_dir = "{}\\{}".format(self.path_core, "management\\commands\\snippets\\flutter\\")
            self.app_configuration = "{}\\lib\\apps\\configuracao\\".format(self.flutter_dir)
            self.app_configuration_page_file = f"{self.app_configuration}\\index.page.dart"
            self.app_configuration_controller_file = f"{self.app_configuration}\\controller.dart"
            self.app_configuration_profile_file = f"{self.app_configuration}\\model.dart"
            self.app_configuration_cubit_file = f"{self.app_configuration}\\cubit.dart"
            self.app_configuration_cubit_state_file = f"{self.app_configuration}\\state.dart"
        else:
            self.project = _path_project.split("/")[-1:][0]
            self.project = self.project.replace("-", "").replace("_", "")
            self.flutter_dir = "{}/Flutter/{}".format("/".join(_path_project.split("/")[:-2]), self.project.lower())
            self.flutter_project = "{}".format(self.project)
            # self.utils_dir = "{}/lib/utils/".format(self.flutter_dir)
            self.core_dir = "{}/lib/core/".format(self.flutter_dir)
            self.ui_dir = "{}/lib/core/user_interface/".format(self.flutter_dir)
            self.ui_extensions = "{}/lib/core/extensions".format(self.flutter_dir)
            self.ui_extensions_file = "{}/lib/core/extensions/size_screen_extension.dart".format(self.flutter_dir)
            self.ui_string_extensions_file = "{}/lib/core/extensions/string_methods_extensions.dart".format(
                self.flutter_dir
            )
            self.config_file = "{}/lib/core/config.dart".format(self.flutter_dir)
            self.util_file = "{}/lib/core/util.dart".format(self.flutter_dir)
            # self.process_controller_file = "{}/lib/utils/process.controller.dart".format(self.flutter_dir)
            self.snippet_dir = "{}/{}".format(self.path_core, "management/commands/snippets/flutter/")
            self.app_configuration = "{}/lib/apps/configuracao/".format(self.flutter_dir)
            self.app_configuration_page_file = f"{self.app_configuration}/index.page.dart"
            self.app_configuration_controller_file = f"{self.app_configuration}/controller.dart"
            self.app_configuration_cubit_state_file = f"{self.app_configuration}/state.dart"
            self.app_configuration_cubit_file = f"{self.app_configuration}/cubit.dart"

        self.current_app_model = None

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    _django_types = [
        "SmallAutoField",
        "AutoField",
        "BLANK_CHOICE_DASH",
        "BigAutoField",
        "BigIntegerField",
        "BinaryField",
        "BooleanField",
        "CharField",
        "CommaSeparatedIntegerField",
        "DateField",
        "DateTimeField",
        "DecimalField",
        "DurationField",
        "EmailField",
        "Empty",
        "FileField",
        "Field",
        "FieldDoesNotExist",
        "FilePathField",
        "FloatField",
        "GenericIPAddressField",
        "IPAddressField",
        "IntegerField",
        "FieldFile",
        "NOT_PROVIDED",
        "NullBooleanField",
        "ImageField",
        "PositiveIntegerField",
        "PositiveSmallIntegerField",
        "SlugField",
        "SmallIntegerField",
        "TextField",
        "TimeField",
        "URLField",
        "UUIDField",
        "ForeignKey",
        "OneToOneField",
    ]

    _flutter_types = [
        "int",
        "int",
        "BLANK_CHOICE_DASH",
        "int",
        "int",
        "String",
        "bool",
        "String",
        "String",
        "DateTime?",
        "DateTime?",
        "double",
        "int",
        "String",
        "String",
        "String",
        "String",
        "String",
        "String",
        "double",
        "String",
        "String",
        "int",
        "String",
        "String",
        "bool",
        "String",
        "int",
        "int",
        "String",
        "int",
        "String",
        "DateTime?",
        "String",
        "String",
        "String",
        "int",
    ]

    _sqlite_types = [
        "INT",
        "INT",
        "BLANK_CHOICE_DASH",
        "BIGINT",
        "BIGINT",
        "TEXT",
        "BOOLEAN",
        "TEXT",
        "TEXT",
        "DATE",
        "DATETIME",
        "DOUBLE",
        "INT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "TEXT",
        "FLOAT",
        "TEXT",
        "TEXT",
        "INT",
        "TEXT",
        "TEXT",
        "BOOLEAN",
        "TEXT",
        "INT",
        "INT",
        "TEXT",
        "SMALLINT",
        "TEXT",
        "DATETIME",
        "TEXT",
        "TEXT",
        "TEXT",
        "INT",
    ]

    def add_arguments(self, parser):
        parser.add_argument("App", type=str, nargs="?")
        parser.add_argument("Model", type=str, nargs="?")
        parser.add_argument("--app", action="store_true", dest="app", help="Criar a App e seus models")
        parser.add_argument(
            "--app_model",
            action="store_true",
            dest="app_model",
            help="Criar a App e o Model informado",
        )
        parser.add_argument("--main", action="store_true", dest="main", help="Renderizar a main.dart")
        parser.add_argument("--yaml", action="store_true", dest="yaml", help="Refatorando o YAML")
        parser.add_argument(
            "--init_cubit",
            action="store_true",
            dest="init_cubit",
            help="Gerar o projeto Flutter utilizando o Cubit como gerencia de estado.",
        )
        parser.add_argument("--clear", action="store_true", dest="clear", help="Limpar projeto flutter.")
        parser.add_argument(
            "--routers",
            action="store_true",
            dest="routers",
            help="Criar o arquivo de rotas nomeadas.",
        )

    def __ignore_base_fields(self, field):
        """Método responsável por remover da análise do models os atributos herdados da classe pai Base

        Arguments:
            field {String} -- Nome do atributo

        Returns:
            bool -- True se o atributo for um dos atributos da classe pai, caso contrário False.
        """
        try:
            __ignore_fields = [
                "id",
                "enabled",
                "deleted",
                "createdOn",
                "created_on",
                "updatedOn",
                "updatedOn",
            ]
            return field in __ignore_fields
        except Exception as error:
            Utils.show_error(
                f"Error in __ignore_base_fields: {error}",
            )

    def __to_camel_case(self, text, flutter=False):
        """Método responsável por converter uma String no padrão camelCase, caso o parâmetro Flutter for True,
        o retorno será no formato camelCase do padrão Dart/Flutter

        Arguments:
            str {str} -- Texto a ser convertido
            flutter {bool} -- Determina se o retorno deve seguir o padrão camelCase do Dart/Flutter (default: {False})
        """
        try:
            components = text.split("_")
            if flutter is True:
                if len(components) == 1:
                    __string = components[0]
                    return "{}{}".format(__string[:1].lower(), __string[1:])
                return components[0] + "".join(x.title() for x in components[1:])
            return components[0] + "".join(x.title() for x in components[1:])
        except Exception as error:
            Utils.show_message(f"Error in Camel Case: {error}")
            return None

    def __get_snippet(self, path=None, file_name=None, state_manager=False):
        """Método para recuperar o valor do arquivo de snippet a ser convertido pela substituição com os valores
        baseados em modelos do projeto Django

        Arguments:
            path {str} - Caminho do arquivo snippet a ser utilizado como padrão para gerar o arquivo resultante.
            file_name {str} - Nome do arquivo snippet a ser lido
            state_manager {bool} - Booleano para determinar se o snippet a ser lido é de algum dos pacotes
                                   de gerência de estado do projeto Flutter (deprecated)

        Returns:
            str -- Texto base a ser utilizado para geração dos arquivos resultantes da conversão
        """

        try:
            if file_name and state_manager is True:
                path = f"{self.snippet_dir}cubit/"
                path += file_name

            if os.path.isfile(path):
                with open(path, encoding="utf-8") as arquivo:
                    return arquivo.read()
        except Exception as e:
            Utils.show_error(
                f"Error in get_snippet {e}",
            )

    def __init_flutter(self):
        """Método para iniciar o projeto Flutter"""
        try:
            if not Utils.check_dir(self.flutter_dir):
                Utils.show_message("Criando o projeto flutter.")
                # flutter create --project-name=NomeDoProjeto --org br.com.NomeDaOrganizacao
                # --platforms android, ios -a kotlin -i swift PathDoProjeto
                # Versão anterior
                # __cmd_flutter_create = "flutter create {}".format(self.flutter_dir)
                __cmd_flutter_create = "flutter create --project-name={1} --org br.com.{1} {2} {0}".format(
                    self.flutter_dir,
                    self.flutter_project.lower(),
                    '--platforms="android,ios"',
                )
                subprocess.call(__cmd_flutter_create, shell=True)
                Utils.show_message("Projeto criado com sucesso.")
        except Exception as error:
            Utils.show_error(
                f"Error in __init_flutter: {error}",
            )

    def __build_flutter(self):
        """Método para após criado o projeto Flutter realizar os comandos de instalação das dependências do projeto
        e atualização do arquivo principal do projeto main.dart
        """
        try:
            if Utils.check_dir(self.flutter_dir):
                Utils.show_message("Atualizando o arquivo de dependências.")
                self.__add_packages()
                time.sleep(3)

                current_path = os.getcwd()
                os.chdir(self.flutter_dir)
                subprocess.run("flutter pub get", shell=True)
                os.chdir(current_path)
                time.sleep(3)

                Utils.show_message("Atualizando o arquivo main.dart.")
                self.__replace_main()
                time.sleep(3)

        except Exception as error:
            Utils.show_error(
                f"Error in __build_flutter: {error}",
            )

    def __build_menu_home_page_items(self):
        """Método responsável por gerar os componentes visual de acesso aos módulos no projeto Flutter"""
        try:
            __items_menu = ""
            for app in FLUTTER_APPS:
                __current_app = AppModel(self.flutter_project, app)
                __app = __current_app.app_name
                for model in __current_app.models:
                    __model = model[1]
                    __items_menu += f"list.add(Itens(title: '{__model.title()}'"
                    __items_menu += f",icon: FontAwesomeIcons.folderOpen,uri: {__app.title()}{__model}"
                    __items_menu += f"Views.{__model}ListPage(),),);"
            return __items_menu
        except Exception as error:
            Utils.show_error(
                f"Error in __build_menu_home_page_itens: {error}",
            )

    def __register_provider(self):
        """Método responsável por registrar no arquivo main.dart os Providers das apps do
        projeto Flutter (deprecated)"""
        __register_provider = ""
        __import_provider = ""
        try:
            for app in FLUTTER_APPS:
                __current_app = AppModel(self.flutter_project, app)
                __app = __current_app.app_name
                for model in __current_app.models:
                    __import_provider += f"import 'apps/{__app.lower()}/{model[1].lower()}/provider.dart';\n"
                    __register_provider += f"ChangeNotifierProvider<{model[1].title()}Provider> "
                    __register_provider += f"(create: (_) => {model[1].title()}Provider(),),\n"

            __import_provider += f"import 'apps/auth/provider.dart';\n"
            __register_provider += f"ChangeNotifierProvider<SettingsProvider>(create: (_) => SettingsProvider(),),\n"
            __register_provider += f"ChangeNotifierProvider<AuthProvider>(create: (_) => AuthProvider(),),\n"
        except Exception as error:
            Utils.show_error(
                f"Error in __register_provider: {error}",
            )
        return __import_provider, __register_provider

    def __register_cubit(self) -> tuple:
        """Método responsável por registrar no arquivo main.dart os módulos cubit de gerência de
        estado do projeto Flutter"""
        _register = ""
        __import = ""
        try:
            for app in FLUTTER_APPS:
                __current_app = AppModel(self.flutter_project, app)
                __app = __current_app.app_name

                for model in __current_app.models:
                    __import += f"import 'apps/{__app.lower()}/{model[1].lower()}/cubit.dart';\n"
                    _register += f"BlocProvider<{model[1]}Cubit>(create: (_) => {model[1]}Cubit(),),\n"

            __import += f"import 'apps/auth/cubit.dart';\n"
            _register += f"BlocProvider<SettingsCubit>(create: (_) => SettingsCubit(),),\n"
            _register += f"BlocProvider<AuthCubit>(create: (_) => AuthCubit(),),\n"
        except Exception as error:
            Utils.show_error(
                f"Error in __register_cubit: {error}",
            )
        return __import, _register

    def __mapping_all_application(self):
        """Método para ler da variável FLUTTER_APPS do arquivo settings.py do projeto Django quais apps deve ser
        geradas no projeto Flutter."""
        try:
            __imports_views = ""
            __imports_controllers = ""
            __controllers_models = ""
            __list_views = ""
            __current_app = None

            for app in FLUTTER_APPS:
                __current_app = AppModel(self.flutter_project, app)
                __app = __current_app.app_name
                for model in __current_app.models:
                    __model = model[1]
                    __imports_views += "import 'apps/{}/{}/pages/list.dart' as {}Views;\n".format(
                        __app, __model.lower(), f"{__app.title()}{__model}"
                    )
                    __list_views += f"Itens(title: '{model[0]._meta.verbose_name}', "
                    __list_views += f"icon: FontAwesomeIcons.folderOpen, uri: {__app.title()}{__model}."
                    __list_views += f"{__model}ListPage()),\n"
                    __imports_controllers += f"import 'apps/{__app.lower()}/{__model.lower()}/controller.dart' "
                    __imports_controllers += f"as {__app.title()}{__model.title()}Controller;\n"
                    __controller_model = f"{__app.title()}{__model.title()}Controller.{__model}"
                    __controllers_models += f"getIt.registerSingleton<{__controller_model}Controller>"
                    __controllers_models += f"({__controller_model}Controller(), instanceName: "
                    __controllers_models += f"'{__app.title()}{__model.title()}Controller');\n    "

            return (
                __imports_views,
                __imports_controllers,
                __controllers_models,
                __list_views,
            )

        except Exception as error:
            Utils.show_error(
                f"Error in __mapping_all_application: {error}",
            )

    def __indexpage_parser(self, app):
        """Método para criar a página de index da app no projeto Flutter"""
        try:
            __indexpage_file = Path(f"{app.get_path_views_dir()}/index.dart")
            if Utils.check_file_is_locked(__indexpage_file):
                return

            content = ParserContent(
                ["$ModelClass$", "$ModelClassCamelCase$", "$project$"],
                [
                    app.model_name,
                    self.__to_camel_case(app.model_name, True),
                    self.flutter_project.lower(),
                ],
                self.__get_snippet(file_name="index_page.txt", state_manager=True),
            ).replace()

            with open(__indexpage_file, "w", encoding="utf-8") as page:
                page.write(content)

        except Exception as error:
            Utils.show_error(
                f"Error in __indexpage_parser {error}",
            )

    def __listpage_parser(self, app):
        """Método para criar a página de listagem da app no projeto Flutter"""
        try:
            __listpage_file = Path(f"{app.get_path_views_dir()}/list.dart")
            if Utils.check_file_is_locked(__listpage_file):
                return

            content = ParserContent(
                [
                    "$App$",
                    "$Model$",
                    "$ModelClass$",
                    "$ModelClassCamelCase$",
                    "$project$",
                ],
                [
                    app.app_name,
                    app.model_name_lower,
                    app.model_name,
                    self.__to_camel_case(app.model_name, True),
                    self.flutter_project,
                ],
                self.__get_snippet(file_name="list_page.txt", state_manager=True),
            ).replace()

            with open(__listpage_file, "w", encoding="utf-8") as page:
                page.write(content)

        except Exception as error:
            Utils.show_error(
                f"Error in __listpage_parser: {error}",
            )

    def __get_attributes_data(self, attribute, model_name, name, name_title) -> str:
        """Método para analisar os atributos do models do Django para gerar o valor correspondente
        para o arquivo que será gerado após a análise."""

        __attribute = ""
        try:
            if attribute == "int":
                if f"id{model_name.lower()}" == name.lower():
                    __attribute = "{0}_{1}Model.id = int.tryParse(_{1}Form{2}.text) ?? 0;\n".format(
                        " " * 16, self.__to_camel_case(model_name, True), name_title
                    )
                else:
                    __attribute = "{0}_{1}Model.{2} = int.tryParse(_{1}Form{3}.text) ?? 0;\n".format(
                        " " * 16,
                        self.__to_camel_case(model_name, True),
                        name,
                        name_title,
                    )

            elif attribute == "double":
                __attribute = "{0}_{1}Model.{2} = double.tryParse(_{1}Form{3}.text) ?? 0.0;\n".format(
                    " " * 16, self.__to_camel_case(model_name, True), name, name_title
                )

            elif attribute == "bool":
                __atribute = "{0}_{1}Model.{2} = _{1}Form{3}.text.isNotEmpty ? _{1}Form{3}.text.contains('0') ? true: false : false;\n".format(
                    " " * 16, self.__to_camel_case(model_name, True), name, name_title
                )
                # __attribute = "{0}_{1}Model.{2} = _{1}Form{3}.text;\n".format(
                #     " " * 16, self.__to_camel_case(model_name, True), name, name_title)

            elif attribute == "DateTime?":
                __attribute = "{0}_{1}Model.{2} = ".format(" " * 16, self.__to_camel_case(model_name, True), name)
                __attribute += '_{0}Form{1}.text != "" ?Util.convertDate(_{0}Form{1}.text): null;\n'.format(
                    self.__to_camel_case(model_name, True), name_title
                )

            else:
                __attribute = "{0}_{1}Model.{2} = _{1}Form{3}.text;\n".format(
                    " " * 16, self.__to_camel_case(model_name, True), name, name_title
                )
        except Exception as error:
            Utils.show_error(
                f"Error in __get_attributes: {error}",
            )
        finally:
            return __attribute

    def __get_controllers_data(self, attribute, model_name, name, name_title) -> str:
        """Método para analisar os atributos do models Django para gerar os campos correspondentes no
        projeto Flutter para quando for utilizado a gerência de estado Provider (deprecated)"""
        __controllers_data = ""
        try:
            if attribute == "int":
                if f"id{model_name.lower()}" == name.lower():
                    __controllers_data = "{0}_{1}Model.id = int.tryParse(_{1}Form{2}.text) ?? 0;\n".format(
                        " " * 6, self.__to_camel_case(model_name, True), name_title
                    )
                else:
                    __controllers_data = "{0}_{1}Model.{2} = int.tryParse(_{1}Form{3}.text) ?? 0;\n".format(
                        " " * 6,
                        self.__to_camel_case(model_name, True),
                        name,
                        name_title,
                    )
            elif attribute == "double":
                __controllers_data = "{0}_{1}Model.{2} = double.tryParse(_{1}Form{3}.text) ?? 0.0;\n".format(
                    " " * 6, self.__to_camel_case(model_name, True), name, name_title
                )
            elif attribute == "bool":
                __controllers_data = "{0}_{1}Model.{2} = _{1}Form{3}.text.isNotEmpty ? _{1}Form{3}.text.contains('0') ? true: false : false;\n".format(
                    " " * 6, self.__to_camel_case(model_name, True), name, name_title
                )
            elif attribute == "DateTime?":
                __controllers_data = '{0}_{1}Model.{2} = _{1}Form{3}.text != ""?'.format(
                    " " * 6,
                    self.__to_camel_case(model_name, True),
                    name,
                    name_title,
                )
                __controllers_data += " Util.convertDate(_{}Form{}.text) : null;\n".format(
                    self.__to_camel_case(model_name, True), name_title
                )
            else:
                __controllers_data = "{0}_{1}Model.{2} = _{1}Form{3}.text;\n".format(
                    " " * 6, self.__to_camel_case(model_name, True), name, name_title
                )
        except Exception as error:
            Utils.show_error(
                f"Error in __get_controllers_data: {error}",
            )
        finally:
            return __controllers_data

    def __create_update_page_parser(self, app, create_page=True):
        """MMétodo para criar a página de criação/atualização da app no projeto Flutter"""
        try:
            if create_page is True:
                __create_page_file = Path(f"{app.get_path_views_dir()}/create.dart")
                content = self.__get_snippet(file_name="create_page.txt", state_manager=True)
                if Utils.check_file_is_locked(__create_page_file):
                    return
            else:
                __create_page_file = Path(f"{app.get_path_views_dir()}/update.dart")
                content = self.__get_snippet(file_name="update_page.txt", state_manager=True)
                if Utils.check_file_is_locked(__create_page_file):
                    return

            content_form = self.__get_snippet(f"{self.snippet_dir}text_field.txt")

            content_attributes = ""
            text_fields = ""
            attributes_data = ""
            clear_data = ""
            edited_attributes = ""
            get_controllers_data = ""

            for field in iter(app.model._meta.fields):
                __app, __model, __name = str(field).split(".")
                __nameTitle = self.__to_camel_case(__name.title())
                __name = self.__to_camel_case(__name.lower())

                if self.__ignore_base_fields(__name):
                    continue

                field_type = str(str(type(field)).split(".")[-1:]).replace('["', "").replace("'>\"]", "")

                attribute = self._flutter_types[self._django_types.index(field_type)]
                content_attributes += "  final _{0}Form{1} = TextEditingController();\n".format(
                    self.__to_camel_case(app.model_name, True), __nameTitle
                )
                text_field = content_form
                controller = "_{}Form{}".format(self.__to_camel_case(app.model_name, True), __nameTitle)
                text_field = text_field.replace("$controller$", controller)
                text_field = text_field.replace("$Field$", str(field.verbose_name).replace("R$", "R\$"))
                text_fields += text_field
                attributes_data += self.__get_attributes_data(attribute, app.model_name, __name, __nameTitle)
                get_controllers_data += self.__get_controllers_data(attribute, app.model_name, __name, __nameTitle)
                clear_data += "    {}.clear();\n".format(controller)

                if __name.startswith(f"id{app.model_name_lower}"):
                    __name = "id"
                edited_attributes += "      {}.text = _{}Model.{}.toString();\n".format(
                    controller, self.__to_camel_case(app.model_name, True), __name
                )

            content = ParserContent(
                [
                    "$app$",
                    "$App$",
                    "$Model$",
                    "$model$",
                    "$ModelClass$",
                    "$ModelClassCamelCase$",
                    "$project$",
                    "$Attributes$",
                    "$Form$",
                    "$AttributesData$",
                    "$ClearData$",
                    "$EditedAttributes$",
                    "$GetValuesControllers$",
                ],
                [
                    app.app_name_lower,
                    app.app_name_lower,
                    self.__to_camel_case(app.model_name, True),
                    app.model_name_lower,
                    app.model_name,
                    self.__to_camel_case(app.model_name, True),
                    self.flutter_project,
                    content_attributes,
                    text_fields,
                    attributes_data,
                    clear_data,
                    edited_attributes,
                    get_controllers_data,
                ],
                content,
            ).replace()

            with open(__create_page_file, "w", encoding="utf-8") as page:
                page.write(content)

        except Exception as error:
            Utils.show_error(
                f"Error in __create_update_page_parser: {error}",
            )

    def __detailpage_parser(self, app):
        """Método para criar a página de detalhe da app no projeto Flutter"""
        try:
            __detail_page_file = Path(f"{app.get_path_views_dir()}/detail.dart")

            if Utils.check_file_is_locked(__detail_page_file):
                return

            content = ParserContent(
                [
                    "$App$",
                    "$app$",
                    "$Model$",
                    "$ModelClassCamelCase$",
                    "$model$",
                    "$ModelClass$",
                    "$project$",
                ],
                [
                    app.app_name,
                    app.app_name_lower,
                    self.__to_camel_case(app.model_name, True),
                    self.__to_camel_case(app.model_name, True),
                    app.model_name_lower,
                    app.model_name,
                    self.flutter_project,
                ],
                self.__get_snippet(file_name="detail_page.txt", state_manager=True),
            ).replace()

            with open(__detail_page_file, "w", encoding="utf-8") as page:
                page.write(content)

        except Exception as error:
            Utils.show_error(
                f"Error in __detailpage_parser {error}",
            )

    def __widget_parser(self, app):
        """Método responsável por criar o arquivo widget.dart de cada app do projeto Flutter mapeada do
        projeto Django."""
        try:
            __widget_file = Path(f"{app.get_path_views_dir()}/widget.dart")
            if Utils.check_file_is_locked(__widget_file):
                return
            content = ParserContent(
                ["$ModelClass$"],
                [app.model_name],
                self.__get_snippet(f"{self.snippet_dir}widget.txt"),
            ).replace()
            with open(__widget_file, "w", encoding="utf-8") as page:
                page.write(content)
        except Exception as error:
            Utils.show_error(
                f"Error in __widget_parser {error}",
            )

    def __build_auth_app(self):
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
            __file = ""
            __data_snippet = self.__get_snippet(file_name="auth_data.txt", state_manager=True)
            __model_snippet = self.__get_snippet(file_name="auth_model.txt", state_manager=True)

            __auth_file = Path(f"{self.flutter_dir}/lib/apps/auth")
            if Utils.check_dir(__auth_file):
                return None

            os.makedirs(__auth_file)

            __data_file = Path("{}/lib/apps/auth/data.dart".format(self.flutter_dir))
            __model_file = Path("{}/lib/apps/auth/model.dart".format(self.flutter_dir))
            __service_file = Path("{}/lib/apps/auth/service.dart".format(self.flutter_dir))

            __data_snippet = __data_snippet.replace("$project$", self.flutter_project)

            with open(__data_file, "w", encoding="utf-8") as data_file:
                data_file.write(__data_snippet)

            with open(__model_file, "w", encoding="utf-8") as model_file:
                model_file.write(__model_snippet)

            __snippet = self.__get_snippet(file_name="auth_app.txt", state_manager=True)

            __snippet_cubit_state = self.__get_snippet(file_name="auth_state.txt", state_manager=True)

            __cubit_state_file = Path("{}/lib/apps/auth/state.dart".format(self.flutter_dir))

            with open(__cubit_state_file, "w", encoding="utf-8") as cubit_state_file:
                cubit_state_file.write(__snippet_cubit_state)
            __file = Path("{}/lib/apps/auth/cubit.dart".format(self.flutter_dir))

            with open(__file, "w", encoding="utf-8") as provider_file:
                provider_file.write(__snippet)

            __service_snippet = self.__get_snippet(file_name="auth_service.txt", state_manager=True)

            with open(__service_file, "w", encoding="utf-8") as service_file:
                service_file.write(__service_snippet)

            # Criando o diretório pages
            os.makedirs(Path(__auth_file, "pages"))

            __auth_pages_names_list = ["index", "signin", "signup", "termo_uso"]
            __auth_snippets_list = [
                "auth_index_page",
                "auth_signin_page",
                "auth_signup_page",
                "auth_termo_uso_page",
            ]
            # Recuperando os snippets

            for auth_page in __auth_pages_names_list:
                __auth_file = Path("{}/lib/apps/auth/pages/{}.dart".format(self.flutter_dir, auth_page))
                __auth_snippet = self.__get_snippet(file_name=f"auth_{auth_page}_page.txt", state_manager=True)

                with open(__auth_file, "w", encoding="utf-8") as auth_page_file:
                    auth_page_file.write(__auth_snippet)

        except Exception as error:
            Utils.show_error(
                f"Error in __build_auth_app {error}",
            )

    def __data_parser(self, app):
        """Método responsável por criar o arquivo contendo o código para persistência de dados da app Flutter, utiliza
        o pacote Sembast como padrão."""
        try:
            __data_file = app.get_path_data_file()
            if Utils.check_file_is_locked(__data_file):
                return

            content = ParserContent(
                ["$ModelClass$", "$modelClass$", "$project$"],
                [app.model_name, app.model_name_lower, self.flutter_project],
                self.__get_snippet(f"{self.snippet_dir}data.txt"),
            ).replace()

            with open(__data_file, "w", encoding="utf-8") as data_helper:
                data_helper.write(content)

        except Exception as error:
            Utils.show_error(
                f"Error in __data_parser {error}",
            )

    """
    ÁREA PARA CRIAÇÃO DOS ARQUIVOS DO DIO
    """

    def __build_custom_dio(self):
        """Método para criar a classe customizada de comunicação HTTP no projeto Flutter"""
        try:
            # Verificando se o diretório dio existe
            _path_directory = Path(f"{self.flutter_dir}/lib/core/dio")
            if not Utils.check_dir(_path_directory):
                os.makedirs(_path_directory)

            __dio_file = Path(f"{self.flutter_dir}/lib/core/dio/custom_dio.dart")
            if Utils.check_file_is_locked(__dio_file):
                return
            content = ParserContent(
                [
                    "$project$",
                ],
                [
                    self.flutter_project,
                ],
                self.__get_snippet(f"{self.snippet_dir}/custom_dio.txt"),
            ).replace()
            with open(__dio_file, "w", encoding="utf-8") as http_request:
                http_request.write(content)
        except Exception as error:
            Utils.show_error(
                f"Error in __build_custom_dio {error}",
            )

    def __build_custom_dio_interceptors(self):
        """Método para criar a classe customizada de comunicação HTTP no projeto Flutter"""
        try:
            # Criando o diretório de interceptors
            __path_directory = Path(f"{self.flutter_dir}/lib/core/dio/interceptors")

            if not Utils.check_dir(__path_directory):
                os.makedirs(__path_directory)

            # Criando o interceptor de header
            __dio_interceptor_header = Path(f"{__path_directory}/header_token_interceptor.dart")
            __snippet_interceptor_header = self.__get_snippet(f"{self.snippet_dir}/dio_interceptor_header.txt")

            with open(__dio_interceptor_header, "w", encoding="utf-8") as dio_interceptor_header:
                dio_interceptor_header.write(__snippet_interceptor_header)

            # Criando o interceptor do refresh_token
            __dio_interceptor_token = Path(f"{__path_directory}/refresh_token_interceptor.dart")
            __snippet_interceptor_token = self.__get_snippet(f"{self.snippet_dir}/dio_interceptor_token.txt")

            with open(__dio_interceptor_token, "w", encoding="utf-8") as dio_interceptor_token:
                dio_interceptor_token.write(__snippet_interceptor_token)

        except Exception as error:
            Utils.show_error(
                f"Error in __build_custom_dio_interceptors {error}",
            )

    def __cubit_parser(self, app):
        """Método responsável por gerar a conversão da app Django para o projeto Flutter, quando for utilizada a
        gerência de estado Cubit/Bloc, essa gerência de estado é o padrão adotado por esse projeto."""
        try:
            if app.model is None:
                print("Informe o App")
                return
            __file_cubit = app.get_path_cubit_file()
            __file_cubit_state = app.get_path_cubit_state_file()
            if Utils.check_file_is_locked(__file_cubit):
                return
            content = ParserContent(
                [
                    "$ModelClass$",
                    "$ModelClassCamelCase$",
                ],
                [app.model_name, self.__to_camel_case(app.model_name, True)],
                self.__get_snippet(file_name="cubit.txt", state_manager=True),
            ).replace()
            with open(__file_cubit, "w", encoding="utf-8") as file_cubit:
                file_cubit.write(content)
            if Utils.check_file_is_locked(__file_cubit_state):
                print("Arquivo travado")
                return
            content = ParserContent(
                [
                    "$ModelClass$",
                    "$ModelClassCamelCase$",
                ],
                [app.model_name, self.__to_camel_case(app.model_name, True)],
                self.__get_snippet(file_name="state.txt", state_manager=True),
            ).replace()
            with open(__file_cubit_state, "w", encoding="utf-8") as file_sate_cubit:
                file_sate_cubit.write(content)
        except Exception as error:
            Utils.show_error(
                f"Error in __cubit_parser: {error}",
            )

    def __service_parser(self, app):
        """Método responsável por criar a classe de acesso à APIRest"""
        try:
            if app.model is None:
                return
            __service_file = app.get_path_service_file()
            if Utils.check_file_is_locked(__service_file):
                return
            content = ParserContent(
                [
                    "$ModelClass$",
                    "$App$",
                    "$Model$",
                    "$ModelClassCamelCase$",
                    "$project$",
                ],
                [
                    app.model_name,
                    app.app_name_lower,
                    app.model_name_lower,
                    self.__to_camel_case(app.model_name, True),
                    self.flutter_project,
                ],
                self.__get_snippet(file_name="service.txt", state_manager=True),
            ).replace()
            if not Utils.check_file(__service_file):
                os.makedirs(__service_file)
            with open(__service_file, "w", encoding="utf-8") as service_file:
                service_file.write(content)
        except Exception as error:
            Utils.show_error(
                f"Error in __service_parser: {error}",
            )

    def __model_parser(self, app):
        """Método responsável por criar a classe de modelo no projeto Flutter baseado na app do Django"""
        try:
            if app.model is None:
                return

            content = self.__get_snippet(f"{self.snippet_dir}model.txt")
            content_attributes = ""
            content_string_return = ""
            content_from_json = ""
            content_to_map = ""
            content_constructor = ""

            __model_file = app.get_path_model_file()

            if Utils.check_file_is_locked(__model_file):
                return

            for field in iter(app.model._meta.fields):
                __app, __model, __name = str(field).split(".")
                __name_dart = self.__to_camel_case(__name)

                if __name_dart in [f"id{app.model_name_lower}", "id"]:
                    continue

                field_type = str(str(type(field)).split(".")[-1:]).replace('["', "").replace("'>\"]", "")

                attribute = self._flutter_types[self._django_types.index(field_type)]

                # Verificando se o campo é: enabled, deleted, createdOn, updatedOn
                # Para não renderizar, já que estes campos são defaults de todas as classes das Apps Django
                if __name_dart not in ["enabled", "deleted", "createdOn", "updatedOn"]:
                    content_attributes += "{} {};\n  ".format(attribute, __name_dart)

                if __name_dart not in [
                    "djangoUser",
                    "token",
                    "firebase",
                    "device_id",
                    "id",
                    "enabled",
                    "deleted",
                    "createdOn",
                    "created_on",
                    "updatedOn",
                    "updatedOn",
                ]:
                    content_string_return += "{}: ${}\\n".format(__name_dart.upper(), __name_dart)

                if __name_dart not in ["enabled", "deleted", "createdOn", "updatedOn"]:
                    default_value = None
                    if str(attribute) == "int":
                        default_value = 0
                    if str(attribute) == "double":
                        default_value = 0.0
                    if str(attribute) == "bool":
                        default_value = "true"
                    if str(attribute) == "String":
                        default_value = "''"

                    if str(attribute) == "DateTime?":
                        content_constructor += f"DateTime? {__name_dart},"

                    if default_value is not None:
                        content_constructor += "this.{} = {},\n".format(__name_dart, default_value)

                if __name_dart not in ["enabled", "deleted", "createdOn", "updatedOn"]:
                    if str(attribute) == "DateTime?":
                        content_from_json += "{}: Util.convertDate(map['{}']) == null".format(__name_dart, __name)
                        content_from_json += "? null:  Util.convertDate(map['{}']),\n".format(__name, " " * 8)
                    elif str(attribute) == "double":
                        content_from_json += "{1}: map.containsKey('{2}') ? map['{2}'] ?? 0.0 : 0.0,\n{0}".format(
                            " " * 8, __name_dart, __name
                        )
                    elif str(attribute) == "bool":
                        content_from_json += "{1}: map.containsKey('{2}') ? map['{2}'] ?? false : false,\n{0}".format(
                            " " * 8, __name_dart, __name
                        )
                    else:
                        if __name_dart.startswith("fk"):
                            content_from_json += "{1}: map.containsKey('{2}') ? map['{2}'] ?? \"\" : \"\",\n{0}".format(
                                " " * 8, __name_dart, __name
                            )
                        else:
                            content_from_json += "{1}: map.containsKey('{2}') ? map['{2}'] ?? \"\" : \"\",\n{0}".format(
                                " " * 8, __name_dart, __name
                            )

                if str(field_type) == "DateTimeField":
                    content_to_map += "'{}': Util.stringDateTimeSplit".format(__name)
                    content_to_map += '(this.{}, returnType: "dt"),\n{}'.format(__name_dart, " " * 8)
                    continue
                if str(field_type) == "DateField":
                    content_to_map += "'{}': Util.stringDateTimeSplit".format(__name)
                    content_to_map += '(this.{}, returnType: "d"),\n{}'.format(__name_dart, " " * 8)
                    continue
                if str(field_type) == "TimeField":
                    content_to_map += "'{}': Util.stringDateTimeSplit".format(__name)
                    content_to_map += '(this.{}, returnType: "t"),\n{}'.format(__name_dart, " " * 8)
                    continue
                if str(field_type) in ["FloatField", "DecimalField"]:
                    content_to_map += "'{0}': this.{1},\n{2}".format(__name, __name_dart, " " * 8)
                    continue
                if str(attribute) == "bool":
                    content_to_map += "'{0}': this.{1},\n{2}".format(__name, __name_dart, " " * 8)
                    continue
                content_to_map += "'{0}': this.{1},\n{2}".format(__name, __name_dart, " " * 8)

            content = ParserContent(
                [
                    "$ModelClass$",
                    "$AttributeClass$",
                    "$StringReturn$",
                    "$Model$",
                    "$ParserfromMap$",
                    "$ParserToMap$",
                    "$project$",
                    "$ConstructorModelClass$",
                ],
                [
                    app.model_name,
                    content_attributes,
                    content_string_return,
                    app.model_name_lower,
                    content_from_json,
                    content_to_map,
                    self.flutter_project,
                    content_constructor,
                ],
                content,
            ).replace()

            if not Utils.check_file(__model_file):
                os.makedirs(__model_file)

            with open(__model_file, "w", encoding="utf-8") as model_file:
                model_file.write(content)

        except Exception as error:
            Utils.show_error(
                f"Error in __parser_model: {error}",
            )

    def __build_settings_controller(self):
        """Método responsável por criar a app no projeto Flutter responsável pelas configurações da App."""
        try:
            if not Utils.check_dir(self.app_configuration):
                os.makedirs(self.app_configuration)

                _content_page = self.__get_snippet(file_name="settings_page.txt", state_manager=True)
                _content_controller = self.__get_snippet(file_name="settings.txt", state_manager=True)

                with open(self.app_configuration_cubit_file, "w", encoding="utf-8") as arquivo:
                    arquivo.write(_content_controller)
                with open(self.app_configuration_cubit_state_file, "w", encoding="utf-8") as arquivo:
                    __content = self.__get_snippet(file_name="settings_state.txt", state_manager=True)
                    arquivo.write(__content)

                with open(self.app_configuration_page_file, "w", encoding="utf-8") as arquivo:
                    arquivo.write(_content_page)

        except Exception as error:
            Utils.show_error(
                f"Error in __build_settings_controller: {error}",
            )

    def __get_yaml_file(self):
        """Método responsável por gerar o arquivo de dependências do projeto Flutter"""
        try:
            return Path(f"{self.flutter_dir}/pubspec.yaml")
        except Exception as error:
            Utils.show_error(
                f"Error in __get_yaml_file:{error}",
            )

    def __add_packages(self):
        """Método responsável por atualizar o arquivo de gerenciamento de dependências com os pacotes padrões
        utilizado no projeto Flutter."""
        try:
            __path = self.__get_yaml_file()
            snippet = ParserContent(
                ["$AppPackage$", "$AppDescription$"],
                [
                    self.project.lower(),
                    f"Projeto Flutter do sistema Django {self.project}",
                ],
                self.__get_snippet(file_name="yaml.txt", state_manager=True),
            ).replace()
            with open(__path, "w", encoding="utf-8") as yaml_file:
                yaml_file.write(snippet)
        except Exception as error:
            Utils.show_error(
                f"Error in __add_packages: {error}",
            )

    def __build_utils(self):
        """Método responsável por criar os arquivos com configurações, variáveis e widgets no projeto Flutter."""
        try:
            if not Utils.check_dir(self.core_dir):
                os.makedirs(self.core_dir)
            __config_snippet = self.__get_snippet(f"{self.snippet_dir}config.txt")
            __util_snippet = self.__get_snippet(f"{self.snippet_dir}util.txt")
            # __controller_snippet = self.__get_snippet(file_name="process.txt", state_manager=True)
            if Utils.check_file(self.config_file) is False:
                __config_snippet = ParserContent(
                    ["$AppName$", "$DjangoAPIPath$"],
                    [SYSTEM_NAME, API_PATH],
                    __config_snippet,
                ).replace()
                with open(self.config_file, "w", encoding="utf-8") as config:
                    config.write(__config_snippet)
            else:
                if Utils.check_file_is_locked(self.config_file) is False:
                    __config_snippet = ParserContent(
                        ["$AppName$", "$DjangoAPIPath$"],
                        [SYSTEM_NAME, API_PATH],
                        __config_snippet,
                    ).replace()
                    with open(self.config_file, "w", encoding="utf-8") as config:
                        config.write(__config_snippet)

            if Utils.check_file(self.util_file) is False:
                with open(self.util_file, "w", encoding="utf-8") as config:
                    config.write(__util_snippet)
            else:
                if Utils.check_file_is_locked(self.util_file) is False:
                    with open(self.util_file, "w", encoding="utf-8") as config:
                        config.write(__util_snippet)

        except Exception as error:
            Utils.show_error(
                f"Error in __build_utils {error}",
            )

    def __build_custom_colors_file(self):
        """Método para criar o arquivo .dart com as configurações de cores
        do aplicativo
        """
        try:
            # Verificando se o diretório das extensions existe
            if not Utils.check_dir(self.ui_dir):
                os.makedirs(self.ui_dir)

            __snippet = self.__get_snippet(f"{self.snippet_dir}custom.colors.txt")
            __path = Path(f"{self.ui_dir}custom.colors.dart")

            with open(__path, "w", encoding="utf-8") as colors:
                colors.write(__snippet)

        except Exception as error:
            Utils.show_error(
                f"Error in __build_custom_colors_file {error}",
            )

    def __build_custom_style_file(self):
        """Método para criar o arquivo .dart com as configurações de estilo
        do aplicativo
        """
        try:
            # Verificando se o diretório das extensions existe
            if not Utils.check_dir(self.ui_dir):
                os.makedirs(self.ui_dir)

            __snippet = self.__get_snippet(f"{self.snippet_dir}custom.style.txt")
            __path = Path(f"{self.ui_dir}custom.style.dart")

            with open(__path, "w", encoding="utf-8") as colors:
                colors.write(__snippet)

        except Exception as error:
            Utils.show_error(
                f"Error in __build_custom_colors_file {error}",
            )

    """
    ÁREA DE CRIAÇÃO DOS ARQUIVOS DE CORE
    """

    def __build_logger_file(self):
        """
        Método para criar o arquivo de log customizando utilizando o pacote logger
        """
        try:
            # Verificando se o diretório core existe
            if not Utils.check_dir(self.core_dir):
                os.makedirs(self.core_dir)

            __snippet = self.__get_snippet(f"{self.snippet_dir}agtec.logger.txt")
            __path = Path(f"{self.core_dir}agtec.logger.dart")

            with open(__path, "w", encoding="utf-8") as arquivo:
                arquivo.write(__snippet)

        except Exception as error:
            Utils.show_error(
                f"Error in __build_logger_file {error}",
            )

    """
    ÁREA DE CRIAÇÃO DOS ARQUIVOS DE EXTENSIONS
    """

    def __build_sized_extensions(self):
        try:
            # Verificando se o diretório das extensions existe
            if not Utils.check_dir(self.ui_extensions):
                os.makedirs(self.ui_extensions)

            __snippet = self.__get_snippet(f"{self.snippet_dir}agtec.size_screen_extensions.txt")
            __path = self.ui_extensions_file

            with open(__path, "w", encoding="utf-8") as arquivo:
                arquivo.write(__snippet)

        except Exception as error:
            Utils.show_error(
                f"Error in __build_utils {error}",
            )

    def __build_string_extensions(self):
        try:
            # Verificando se o diretório das extensions existe
            if not Utils.check_dir(self.ui_extensions):
                os.makedirs(self.ui_extensions)

            __snippet = self.__get_snippet(f"{self.snippet_dir}agtec.string_methods_extensions.txt")
            __path = self.ui_string_extensions_file

            with open(__path, "w", encoding="utf-8") as arquivo:
                arquivo.write(__snippet)

        except Exception as error:
            Utils.show_error(
                f"Error in __build_utils {error}",
            )

    def __build_user_interface(self):
        """Método responsável por criar os elementos gráficos/visuais do projeto Flutter com os valores padrões"""
        try:
            if not Utils.check_dir(self.ui_dir):
                os.makedirs(self.ui_dir)

            for arquivo in ["widget", "font"]:
                __path = Path(f"{self.ui_dir}{arquivo}.dart")
                if arquivo == "font":
                    __snippet = self.__get_snippet(Path(f"{self.snippet_dir}ui_{arquivo}.txt"))
                else:
                    __snippet = self.__get_snippet(file_name="ui_widget.txt", state_manager=True)
                if Utils.check_file(__path) is False:
                    with open(__path, "w", encoding="utf-8") as arq:
                        arq.write(__snippet)
                else:
                    if Utils.check_file_is_locked(__path) is False:
                        with open(__path, "w", encoding="utf-8") as arq:
                            arq.write(__snippet)

        except Exception as error:
            Utils.show_error(
                f"Error in __build_user_interface: {error}",
            )

    def __create_source_from_model(self):
        """Método responsável por criar os arquivos do projeto Django baseados no models"""
        Utils.show_message("Criando as apps baseado na App e no Model")
        try:
            self.__create_source(self.current_app_model.app_name, self.current_app_model.model_name)
        except Exception as error:
            Utils.show_error(
                f"Error in __create_source_from_model: {error}",
            )

    def __create_source_from_generators(self):
        """Método responsável por criar os arquivos do projeto Django, quando não for informado o nome da App,
        nesse caso o método percorre todas as apps do projeto Django (deprecated)"""
        Utils.show_message("Criando as apps baseado na App e nos Generators")
        try:
            for model in self.current_app_model.models:
                self.__create_source(self.current_app_model.app_name, model[1])
        except Exception as error:
            Utils.show_error(
                f"Error in __create_source_from_generators: {error}",
            )

    def __create_source(self, app_name, model_name):
        """Método principal que chama os demais métodos para geração dos arquivos do projeto Django e do projeto
        Flutter"""
        try:
            if app_name is None:
                Utils.show_message("É necessário passar a App")
                return

            if model_name is None:
                Utils.show_message(f"É necessário passar o Model")
                return

            __source_class = AppModel(self.flutter_dir, app_name, model_name)
            __app_name = __source_class.app_name
            __model_name = __source_class.model_name
            __model = __source_class.model
            __model_dir = __source_class.get_path_app_model_dir()
            __views_dir = __source_class.get_path_views_dir()
            __data_file = __source_class.get_path_data_file()
            __model_file = __source_class.get_path_model_file()
            __service_file = __source_class.get_path_service_file()
            __cubit_file = __source_class.get_path_cubit_file()
            __cubit_state_file = __source_class.get_path_cubit_state_file()
            __views = __source_class.get_path_files_views()

            if not Utils.check_dir(__model_dir):
                Utils.show_message(f"Criando diretório source do {__app_name}.{__model_name}")
                os.makedirs(__model_dir)

            if not Utils.check_dir(__views_dir):
                os.makedirs(__views_dir)

                if __views is not None:
                    with open(__views[0], "w", encoding="utf-8") as pagina:
                        pagina.write(f"// Create Page {__app_name} {__model_name}")

                    with open(__views[1], "w", encoding="utf-8") as pagina:
                        pagina.write(f"// Detail Page {__app_name} {__model_name}")

                    with open(__views[2], "w", encoding="utf-8") as pagina:
                        pagina.write(f"// Index Page {__app_name} {__model_name}")

                    with open(__views[3], "w", encoding="utf-8") as pagina:
                        pagina.write(f"// List Page {__app_name} {__model_name}")

                    with open(__views[4], "w", encoding="utf-8") as pagina:
                        pagina.write(f"// Update Page {__app_name} {__model_name}")

            if not Utils.check_file(__model_file):
                with open(__model_file, "w", encoding="utf-8") as arquivo:
                    arquivo.write(f"// Modelo do {__model_name}")

            if not Utils.check_file(__data_file):
                with open(__data_file, "w", encoding="utf-8") as arquivo:
                    arquivo.write(f"// Persistência do {__model_name}")

            if not Utils.check_file(__service_file):
                with open(__service_file, "w", encoding="utf-8") as arquivo:
                    arquivo.write(f"// Service do {__model_name}")

            if not Utils.check_file(__cubit_file):
                with open(__cubit_file, "w", encoding="utf-8") as arquivo:
                    arquivo.write(f"// Cubit do {__model_name}")
            if not Utils.check_file(__cubit_state_file):
                with open(__cubit_state_file, "w", encoding="utf-8") as arquivo:
                    arquivo.write(f"// State Cubit do {__model_name}")

            self.__create_update_page_parser(__source_class)
            self.__detailpage_parser(__source_class)
            self.__indexpage_parser(__source_class)
            self.__listpage_parser(__source_class)
            self.__widget_parser(__source_class)
            self.__create_update_page_parser(__source_class, False)
            self.__model_parser(__source_class)
            self.__data_parser(__source_class)
            self.__service_parser(__source_class)
            self.__cubit_parser(__source_class)

        except Exception as error:
            Utils.show_error(
                f"Error in __create_source: {error}",
            )

    def __build_internationalization(self):
        """Método responsável por criar os arquivos de internacionalização dos textos no projeto Flutter"""
        try:
            snippet = self.__get_snippet(f"{self.snippet_dir}localization.txt")
            path_localization = os.path.join(self.core_dir, "localization.dart")

            if Utils.check_file_is_locked(path_localization):
                return

            with open(path_localization, "w", encoding="utf-8") as localizations:
                localizations.write(snippet)

            __lang_dir = Path(f"{self.flutter_dir}/lang")
            __pt_br = Path(f"{self.flutter_dir}/lang/pt.json")
            __en_us = Path(f"{self.flutter_dir}/lang/en.json")

            if not Utils.check_dir(__lang_dir):
                os.makedirs(__lang_dir)

            if not Utils.check_file(__pt_br):
                snippet = self.__get_snippet(f"{self.snippet_dir}pt_language.txt")
                with open(__pt_br, "w", encoding="utf-8") as pt_json:
                    pt_json.write(snippet)

            if not Utils.check_file(__en_us):
                snippet = self.__get_snippet(f"{self.snippet_dir}en_language.txt")
                with open(__en_us, "w", encoding="utf-8") as en_json:
                    en_json.write(snippet)

        except Exception as error:
            Utils.show_error(
                f"Error in _build_internationalization: {error}",
            )

    def __create_exception_class(self):
        """Método responsável por criar a classe de gerenciamento das Exceptions no projeto Flutter"""
        try:
            # Verificando se o diretório existe
            _path_directory = Path(f"{self.flutter_dir}/lib/core/exceptions")
            if not Utils.check_dir(_path_directory):
                os.makedirs(_path_directory)

            path_exceptions = Path(f"{self.flutter_dir}/lib/core/exceptions/exception.dart")
            if Utils.check_file_is_locked(path_exceptions):
                return

            snippet_exception = self.__get_snippet(f"{self.snippet_dir}exception.txt")
            with open(path_exceptions, "w", encoding="utf-8") as exception_file:
                exception_file.write(snippet_exception)
        except Exception as error:
            print(f"Error in __create_exception_class: {error}")
            Utils.show_message(f"Error in __create_exception_class: {error}")

    def __create_named_route(self):
        """Método responsável por criar as rotas de navegação nomeadas no projeto Flutter"""
        __pages_name_list = [
            "IndexPage",
            "DetailPage",
            "ListPage",
            "UpdatePage",
            "AddPage",
        ]
        __imports_name_list = ["index", "list", "detail", "update", "create"]
        __snippet_route = "case $ClassName$$PageName$.routeName:\n"
        __snippet_route += "    return CupertinoPageRoute(builder: (_) => $ClassName$$PageName$());\n"
        # Snippet para rotas de edição e detalhamento
        __snippet_route_created_updated = "case $ClassName$$PageName$.routeName:\n"
        __snippet_route_created_updated += "  if(args is $ClassName$Model)\n"
        __snippet_route_created_updated += (
            "    return CupertinoPageRoute(builder: (_) => $ClassName$$PageName$("
            "$ModelClassCamelCase$Model: args));\n"
        )
        __snippet_route_created_updated += "  return CupertinoPageRoute(builder: (_) => $ClassName$$PageName$($ModelClassCamelCase$Model: $ClassName$Model()));\n"
        __snippet_imports = "import 'apps/$APP$/$model$/pages/$page$.dart';"
        routers_apps = ""
        imports_apps = ""
        try:
            path_routes = Path(f"{self.flutter_dir}/lib/routers.dart")
            if Utils.check_file_is_locked(path_routes):
                return
            snippet = self.__get_snippet(f"{self.snippet_dir}named_route.txt")
            # Looping all apps Django project to get Pages
            for app in FLUTTER_APPS:
                __current_app = AppModel(self.flutter_project, app)
                __app = __current_app.app_name
                for model in __current_app.models:
                    __model = model[1]
                    for page_name in __pages_name_list:
                        if page_name in ["UpdatePage", "DetailPage"]:
                            routers_apps += (
                                __snippet_route_created_updated.replace("$ClassName$", __model)
                                .replace(
                                    "$ModelClassCamelCase$",
                                    self.__to_camel_case(__model, True),
                                )
                                .replace("$PageName$", page_name)
                            )
                        else:
                            routers_apps += __snippet_route.replace("$ClassName$", __model).replace(
                                "$PageName$", page_name
                            )
                        routers_apps += "\n"
                    for import_name in __imports_name_list:
                        imports_apps += (
                            __snippet_imports.replace("$APP$", __app.lower())
                            .replace("$model$", __model.lower())
                            .replace("$page$", import_name)
                        )
                        imports_apps += "\n"
                    imports_apps += "import 'apps/$APP$/$model$/model.dart';".replace("$APP$", __app.lower()).replace(
                        "$model$", __model.lower()
                    )
            if routers_apps != "":
                snippet = snippet.replace("$ROUTES_APPS$", routers_apps).replace("$IMPORTS$", imports_apps)
            else:
                print("Nada foi alterado no arquivo snippet")
            with open(path_routes, "w", encoding="utf-8") as route_named:
                route_named.write(snippet)
            pass
        except Exception as error:
            print(error)
            Utils.show_message(f"Error in __create_name_route: {error}")

    def __replace_main(self):
        """Método responsável por atualizar o conteúdo do arquivo main.dart no projeto Flutter contendo as estruturas
        de navegação para as apps geradas via projeto core."""
        __imports = ""
        __list_itens = []
        try:
            snippet = self.__get_snippet(file_name="main.txt", state_manager=True)

            path_main_dart = Path(f"{self.flutter_dir}/lib/main.dart")
            if Utils.check_file_is_locked(path_main_dart):
                return

            (
                __import_views,
                __import_controllers,
                __register_controller,
                __views,
            ) = self.__mapping_all_application()

            __import_controllers += f"import 'apps/configuracao/model.dart';"
            __import_views += f"import 'apps/configuracao/index.page.dart';\n"
            __register_controller += "getIt.registerSingleton<SettingsController>(SettingsController());"

            if __import_views is None or __import_controllers is None:
                return

            snippet = snippet.replace("$project$", self.flutter_project)

            __import_controllers += f"import 'apps/configuracao/cubit.dart';"
            __import, __register = self.__register_cubit()
            snippet = snippet.replace("$ImportController$", __import_controllers)
            snippet = snippet.replace("$ImportCubit$", __import)
            snippet = snippet.replace("$RegisterProviders$", __register)

            snippet = snippet.replace("$Listviews$", __views)

            with open(path_main_dart, "w", encoding="utf-8") as main_dart:
                main_dart.write(snippet)

            path_homepage = Path(f"{self.flutter_dir}/lib/home.page.dart")
            if Utils.check_file_is_locked(path_homepage):
                return
            __snippet_page = self.__get_snippet(file_name="home.page.txt", state_manager=True)
            __menu_home_page_itens = self.__build_menu_home_page_items()

            __snippet_page = __snippet_page.replace("$ImportViews$", __import_views)
            __snippet_page = __snippet_page.replace("$ItenMenu$", __menu_home_page_itens)

            with open(path_homepage, "w", encoding="utf-8") as home_page_dart:
                home_page_dart.write(__snippet_page)

        except Exception as error:
            Utils.show_error(
                f"Error in __replace_main: {error}",
            )

    def call_methods(self, options):
        """
        Método que identifica qual comando foi solicitado pelo usuário para ser executado, antes de chamar o método,
        as entradas informadas pelo usuário são validadas, evitando erros de execução do programa devido à ausência de
        parâmetros obrigatórios.
        """

        if options["main"]:
            self.__replace_main()
            return
        elif options["yaml"]:
            self.__add_packages()
            return
        elif options["routers"]:
            self.__create_named_route()
            return
        elif options["clear"]:
            self.__clear_project()
            sys.exit()

        else:
            self.__init_flutter()
            self.__build_settings_controller()
            self.__build_utils()
            self.__build_user_interface()
            self.__build_custom_colors_file()
            self.__build_custom_style_file()
            self.__build_sized_extensions()
            self.__build_string_extensions()
            self.__build_custom_dio()
            self.__build_custom_dio_interceptors()
            self.__build_internationalization()
            self.__build_logger_file()
            self.__build_auth_app()
            self.__build_flutter()
            self.__create_named_route()
            self.__create_exception_class()

    def handle(self, *args, **options):
        app = options["App"] or None
        model = options["Model"] or None

        if app is None and model is None and FLUTTER_APPS == []:
            Utils.show_error(
                f"Você não configurou o FLUTTER_APPS no settings e também não informou uma APP para ser gerada.",
            )
            return

        if app and model:
            if Utils.contain_number(app) or Utils.contain_number(model):
                Utils.show_message(f"Nome da app ou do model contendo números")
                return

            self.current_app_model = AppModel(self.flutter_project, app, model)
            self.__create_source_from_model()
            return

        if app and model is None:
            if Utils.contain_number(app):
                Utils.show_error(
                    f"Nome da app contendo números",
                )
                return

            self.current_app_model = AppModel(self.flutter_project, app)
            self.__create_source_from_generators()
            return

        if not FLUTTER_APPS:
            Utils.show_error(
                "Não foram informadas as APPS a serem mapeadas",
            )
            return
        else:
            self.call_methods(options)
            for __app in FLUTTER_APPS:
                self.current_app_model = AppModel(self.flutter_project, __app)
                self.__create_source_from_generators()

    def __clear_project(self, path=None):
        try:
            __path = path or f"{self.flutter_dir}"
            import shutil

            shutil.rmtree(__path)
        except Exception as error:
            Utils.show_message(f"Error in __clear_project: {error}")
