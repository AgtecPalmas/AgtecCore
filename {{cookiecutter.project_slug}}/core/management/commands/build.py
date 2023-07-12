"""Esse manager é responsável por gerar os arquivos padrões de um projeto Django (templates, urls, views, forms)
baseado nas informações contidas na classe da App do projeto Django.
"""

import os
from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand
from rich import box, print
from rich.panel import Panel
from rich.text import Text

from .django_managers import (
    DRFBuild,
    FormsBuild,
    ParserHTMLBuild,
    StaticsBuild,
    TemplatesBuild,
    TestsBuild,
    UrlsBuild,
    ViewsBuild,
)
from .formatters import HtmlFormatter, PythonFormatter
from .utils import Utils


class Command(BaseCommand):
    help = "Manager responsável por gerar os arquivos padrões de um projeto Django."

    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )

    def __init__(self):
        super().__init__()
        self.path_root: Path = os.getcwd()
        self.path_core: Path = os.path.join(self.BASE_DIR, "core")

        self.path_base: Path = Path(f"{self.path_root}/base")
        self.path_base_urls: Path = Path(f"{self.path_base}/urls.py")
        self.path_base_api_urls: Path = Path(f"{self.path_base}/api_urls.py")

        self.app: str = None
        self.app_lower: str = None
        self.app_instance: object = None
        self.path_app: Path = None

        self.model: str = None
        self.model_lower: str = None
        self.path_model: Path = None

        self.path_form: Path = None
        self.path_views: Path = None
        self.path_urls: Path = None
        self.path_template_dir: Path = None
        self.path_api: Path = None
        self.path_serializer: Path = None
        self.path_api_views: Path = None
        self.path_api_urls: Path = None
        self.path_tests: Path = None

        self.force_templates: bool = False
        self.options: dict = None

    def add_arguments(self, parser):
        parser.add_argument("App", type=str)
        parser.add_argument("Model", type=str, nargs="?")
        parser.add_argument(
            "--templates",
            action="store_true",
            dest="templates",
            help="Criar apenas os Templates",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            dest="force",
            help="Forçar a criação dos Templates ignorando o #FileLocked",
        )
        parser.add_argument(
            "--api", action="store_true", dest="api", help="Criar apenas a API"
        )
        parser.add_argument(
            "--urls", action="store_true", dest="url", help="Criar apenas as Urls"
        )
        parser.add_argument(
            "--forms", action="store_true", dest="forms", help="Criar apenas o Form"
        )
        parser.add_argument(
            "--views",
            action="store_true",
            dest="views",
            help="Criar apenas as Views (CRUD)",
        )
        parser.add_argument(
            "--parserhtml",
            action="store_true",
            dest="parserhtml",
            help="Renderizar os fields do models para HTML",
        )
        parser.add_argument(
            "--tests",
            action="store_true",
            dest="tests",
            help="Criar apenas os Testes (CRUD)",
        )
        parser.add_argument(
            "--format",
            action="store_true",
            dest="format",
            help="Aplicar Black, isort e flake8 nos arquivos .py e djlint nos arquivos .html",
        )
        parser.add_argument(
            "--static",
            action="store_true",
            dest="static",
            help="Criar o diretório static da app/models",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            dest="all",
            help="Criar todos os arquivos padrões [forms, views, urls, templates, parserhtml, static, api, tests]",
        )

    """
    [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
    [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
    [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
            Começo dos método refatorados para as classes XPTOBuild
    [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
    [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
    [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
    """

    def __manage_form(self):
        """Método responsável por repassar para a class FormsBuild a
        responsabilidade de criar os forms dos models da app
        """
        try:
            FormsBuild(self, apps).build()
            PythonFormatter(self.path_form).format()

        except Exception as error:
            Utils.show_error(f"Error in __manage_form : {error}")

    def __manage_views(self):
        """Método responsável por repassar a criação das views para a classe ViewsBuild
        a responsabilidade de criar as views dos models da app"""
        try:
            ViewsBuild(self, apps).build()
            ViewsBuild(self, apps).build_init_file()
            PythonFormatter(self.path_views).format()

        except Exception as error:
            Utils.show_error(f"Error in __manage_views : {error}")

    def __manage_url(self):
        """Método para criar/configurar o arquivo urls.py do model"""
        try:
            UrlsBuild(self, apps).build()
            UrlsBuild(self, apps).add_url_to_base()
            PythonFormatter(self.path_urls).format()
            PythonFormatter(self.path_base_urls).format()

        except Exception as error:
            Utils.show_error(f"Error in __manage_url : {error}")

    def __manage_statics(self):
        """Método responsável por repasar a criação dos arquivos estáticos para a classe StaticBuild"""
        try:
            StaticsBuild(self).build()

        except Exception as error:
            Utils.show_error(f"Error in __manage_statics: {error}")

    def __manage_templates(self):
        """
        Método que repassa para a class TemplatesBuild a responsabilidade de criar os templates
        """
        try:
            if Utils.check_dir(self.path_template_dir) is False:
                Utils.show_message("Criando o diretório dos Templates")
                os.makedirs(self.path_template_dir)
            if Utils.check_dir(f"{self.path_template_dir}/{self.model_lower}") is False:
                os.makedirs(f"{self.path_template_dir}/{self.model_lower}")
            TemplatesBuild(self, apps, self.force_templates).build()

        except Exception as error:
            Utils.show_error(f"Error in __manage_templates : {error}")

    def __manage_parser_html(self):
        """Método para renderizar o código HTML a ser inserido nos arquivos de template do models."""
        try:
            ParserHTMLBuild(self, apps).build()

        except Exception as error:
            Utils.show_error(f"Error in __manage_parser_html : {error}")

    def __manage_tests(self):
        """Método responsável por repassar a criação dos testes para a classe TestsBuild"""
        try:
            TestsBuild(self, apps).build()
            PythonFormatter(self.path_tests).format()

        except Exception as error:
            Utils.show_error(f"Error in __manage_tests : {error}")

    # Métodos da APIRest

    def __manage_serializer(self):
        """Método responsável por criar/configurar o arquivo de serializer para a APIRest (DRF)"""
        try:
            DRFBuild(self, apps).manage_serializers()
            PythonFormatter(self.path_serializer).format()

        except Exception as error:
            Utils.show_error(f"Error in __manage_serializer : {error}")

    def __manage_api_view(self):
        """Método responsável por criar/configurar o arquivo de views para a APIRest (DRF)"""
        try:
            DRFBuild(self, apps).manage_views()
            PythonFormatter(self.path_api_views).format()

        except Exception as error:
            Utils.show_error(f"Error in __manage_api_view: {error}")

    def __manage_api_url(self):
        """Método responsável por criar/configurar o arquivo de urls para a APIRest (DRF)"""
        try:
            DRFBuild(self, apps).manage_router_urls()
            PythonFormatter(self.path_api_urls).format()

        except Exception as error:
            Utils.show_error(f"Ocorreu o erro : {error} no __manage_api_url")

    def __manage_urls_api_app(self):
        """Método para adicionar o path da app ao arquivo urls_api.py"""
        try:
            DRFBuild(self, apps).manage_urls_api()
            PythonFormatter(self.path_base_api_urls).format()

        except Exception as error:
            Utils.show_error(f"Error in __manage_urls_api_app : {error}")

    def __manage_api(self):
        """Método que chama os métodos responsáveis por criar os arquivos da APIRest"""
        try:
            self.__manage_serializer()
            self.__manage_api_view()
            self.__manage_api_url()
            self.__manage_urls_api_app()

        except Exception as error:
            Utils.show_error(f"Error in __manage_api : {error}")

    def __manage_format_code(self):
        """Método responsável por formatar o código fonte da app"""
        try:
            Utils.show_message("Formatando o código [cyan b]Python[/]")
            PythonFormatter(self.path_model).format()
            PythonFormatter(self.path_form).format()
            PythonFormatter(self.path_views).format()
            PythonFormatter(self.path_urls).format()
            PythonFormatter(self.path_base_urls).format()
            PythonFormatter(self.path_serializer).format()
            PythonFormatter(self.path_api_views).format()
            PythonFormatter(self.path_api_urls).format()
            PythonFormatter(self.path_base_api_urls).format()
            PythonFormatter(self.path_tests).format()

            Utils.show_message("Formatando o código [cyan b]HTML[/]")
            HtmlFormatter(Path(f"{self.path_template_dir}/{self.model_lower}")).format()

        except Exception as error:
            Utils.show_error(f"Error in __manage_format_code : {error}")

    """
    [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
    [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
                Fim dos método refatorados para as classes XPTOBuild
    [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
    [[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
    """

    @staticmethod
    def __verify_model(path_model, model):
        if Utils.contain_number(model):
            Utils.show_error("O nome do Model não pode conter números")

        if Utils.check_content(path_model, f"class {model}") is False:
            Utils.show_error(f"Modelo {model} não encontrado")

    @staticmethod
    def __verify_app(path_root, app_name):
        if not app_name:
            Utils.show_error("Você deve informar o nome da App")

        if Utils.contain_number(app_name):
            Utils.show_error("O nome da App não pode conter números")

        if apps.is_installed(app_name) is False:
            Utils.show_error(
                f"App [b cyan]{app_name}[/] deve estar no [b cyan]INSTALLED_APPS[/] do settings"
            )

        if Utils.check_dir(f"{path_root}/{app_name}") is False:
            Utils.show_error(f"Diretório da App [b cyan]{app_name}[/] não encontrado")

    def __verify_valid_flags(self, options):
        __flags = [
            "all",
            "templates",
            "api",
            "url",
            "forms",
            "views",
            "parserhtml",
            "static",
            "force",
            "format",
            "tests",
        ]
        result = False
        try:
            for flag in __flags:
                if options[flag] is True:
                    result = True
        finally:
            if options.get("force"):
                self.force_templates = True

            if not result:
                Utils.show_error(
                    "Para gerar os arquivos de uma app, é necessário informar um dos parâmetros abaixo:\n\
                    \n[b cyan]--all\n--api\n--force\n--forms\n--parserhtml\n--static\n--templates\n--url\
                    \n--format\n--views\n--tests[/]",
                    emoji="warning",
                )
                return

            return result

    def call_methods(self, options):
        if not any(options.values()):
            Utils.show_error(
                "Nenhuma flag foi passada, utilize [b cyan]--help[/] para ver as opções disponíveis",
            )
            return

        if options["force"]:
            self.force_templates = True
            if (
                not options["templates"]
                and not options["all"]
                and not options["parserhtml"]
            ):
                Utils.show_error(
                    """A flag [b cyan]--force[/] só pode ser utilizado em conjunto com as flags
                        \n[b cyan]--templates[/], [b cyan]--parserhtml[/] ou [b cyan]--all[/]""",
                )
                return

        if options["all"]:
            Utils.show_message("Configurando [b cyan]todos[/] os arquivos")
            self.__manage_form()
            self.__manage_views()
            self.__manage_url()
            self.__manage_api()
            self.__manage_templates()
            self.__manage_parser_html()
            self.__manage_statics()
            self.__manage_tests()
            self.__manage_format_code()
            return

        if options["templates"]:
            Utils.show_message("Configurando [b cyan]Templates[/]")
            self.__manage_templates()

        if options["api"]:
            Utils.show_message("Configurando [b cyan]API[/]")
            self.__manage_api()

        if options["url"]:
            Utils.show_message("Configurando [b cyan]URLs[/]")
            self.__manage_url()

        if options["forms"]:
            Utils.show_message("Configurando [b cyan]Forms[/]")
            self.__manage_form()

        if options["views"]:
            Utils.show_message("Configurando [b cyan]Views[/]")
            self.__manage_views()

        if options["parserhtml"]:
            Utils.show_message("Configurando [b cyan]Parser HTML[/]")
            self.__manage_parser_html()

        if options["format"]:
            Utils.show_message("[b cyan]Formatando[/] código")
            self.__manage_format_code()

        if options["static"]:
            Utils.show_message("Configurando arquivos [b cyan]estáticos[/]")
            self.__manage_statics()

        if options["tests"]:
            Utils.show_message("Configurando arquivos [b cyan]tests[/]")
            self.__manage_tests()

        return

    def handle(self, *args, **options):
        print(
            Panel(
                Text("AGTEC CORE", justify="center", style="cyan bold"),
                border_style="cyan",
            )
        )

        self.options = options
        app = Utils.clear_string(options.get("App"))
        self.__verify_app(self.path_root, app)
        self.__verify_valid_flags(options)

        self.app = app.strip()
        self.app_lower = app.lower()
        self.path_app = Path(f"{self.path_root}/{app}")
        self.app_instance = apps.get_app_config(self.app_lower)

        self.path_model = Path(f"{self.path_app}/models.py")
        self.path_form = Path(f"{self.path_app}/forms.py")
        self.path_views = Path(f"{self.path_app}/views")
        self.path_urls = Path(f"{self.path_app}/urls.py")
        self.path_template_dir = Path(f"{self.path_app}/templates/{self.app}")
        self.path_tests = Path(f"{self.path_app}/tests/")

        self.path_api = Path(f"{self.path_app}/api")
        self.path_api_views = Path(f"{self.path_api}/api_views.py")
        self.path_api_urls = Path(f"{self.path_api}/api_urls.py")
        self.path_serializer = Path(f"{self.path_api}/serializers.py")

        Utils.show_message(
            f"App {self.app}", title=True, emoji="toolbox", box_style=box.ASCII2
        )

        models = []

        if model := options.get("Model"):
            self.__verify_model(self.path_model, model)
            models.append(self.app_instance.get_model(model))

        else:
            models = list(self.app_instance.get_models())

        with Utils.ProgressBar() as bar:
            task = bar.add_task(
                f"Gerando [b green]{self.app}[/]",
                total=len(models),
            )

            for model in models:
                Utils.show_message(
                    f"Model {self.app}:{model.__name__}",
                    title=True,
                    emoji="hourglass_flowing_sand",
                )
                model = model.__name__
                self.model = model.strip()
                self.model_lower = model.lower()
                self.call_methods(options)

                bar.advance(task, 1)

        Utils.show_message("Processo concluído", title=True, emoji="rocket")
        return
