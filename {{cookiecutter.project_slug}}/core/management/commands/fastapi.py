import os
import platform
from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand

from base.settings import FASTAPI_APPS

from .fastapi_managers import (
    DockerBuild,
    ModelsBuild,
    ProjetoBuild,
    RoutersBuild,
    SchemasBuild,
    UseCasesBuild,
)
from .formatters import PythonFormatter
from .utils import Utils


class Command(BaseCommand):
    help = """Manager responsável por analisar as classes de modelos do projeto Django para gerar os arquivos
    do projeto FastAPI correspondente às apps do Django"""

    def __init__(self):
        super().__init__()
        self.model_lower = None
        self.model = None
        self.app_instance = None
        self.path_api = None
        self.path_crud = None
        self.path_model_fastapi = None
        self.path_schema = None
        self.app_lower = None
        self.path_model = None
        self.path_app_local = None
        self.path_app = None
        self.app = None
        self.operation_system = platform.system().lower()
        self.path_core = Path(__file__).parent.parent.parent
        self.path_management_directory = Path(__file__).parent.parent
        self.path_root = Path(__file__).parent.parent.parent.parent
        self.project_dir = Path(__file__).parent.parent.parent.parent.parent.parent
        self.path_command = Path(__file__).parent
        self.project = str(self.path_root).split("\\")[-1]
        if self.operation_system != "windows":
            self.project = str(self.path_root).split("/")[-1]
        self.fastapi_dir = Path(f"{self.project_dir}/FastAPI/{self.project}")
        self.snippet_dir = Path(f"{self.path_command}/snippets/fastapi/")

        self.current_app_model = None

    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )

    def add_arguments(self, parser):
        parser.add_argument("App", type=str, nargs="?")
        parser.add_argument("Model", type=str, nargs="?")

        parser.add_argument(
            "--all",
            action="store_true",
            dest="all",
            help="Criar o projeto com as apps informadas na constante FASTAPI_APPS no settings.py",
        )
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
            "--schemas",
            action="store_true",
            dest="schemas",
            help="Criar apenas os Schemas",
        )
        parser.add_argument(
            "--api",
            action="store_true",
            dest="api",
            help="Criar apenas as rotas da api",
        )
        parser.add_argument(
            "--cruds", action="store_true", dest="cruds", help="Criar apenas os cruds"
        )
        parser.add_argument(
            "--models",
            action="store_true",
            dest="models",
            help="Criar apenas os models",
        )
        parser.add_argument(
            "--docker", action="store_true", dest="docker", help="Configurar o docker"
        )
        parser.add_argument(
            "--base",
            action="store_true",
            dest="base",
            help="Criar apenas o projeto base",
        )
        parser.add_argument(
            "--format",
            action="store_true",
            dest="format",
            help="Aplica Black, isort e flake8 nos arquivos",
        )

    @staticmethod
    def __init_app(app_path):
        try:
            if not Utils.check_dir(app_path):
                os.makedirs(app_path)
        except Exception as error:
            Utils.show_error(f"Error in __init_Fastapi: {error}")

    def __manage_projeto(self):
        try:
            ProjetoBuild(self).build()
        except Exception as error:
            Utils.show_error(f"Error in __manage_projeto: {error}")

    def __manage_schema(self):
        try:
            SchemasBuild(self).build()
        except Exception as error:
            Utils.show_error(f"Error in __manage_schema: {error}")

    def __manage_model(self):
        try:
            ModelsBuild(self).build()
        except Exception as error:
            Utils.show_error(f"Error in __manage_model: {error}")

    def __manage_cruds(self):
        try:
            UseCasesBuild(self).build()
        except Exception as error:
            Utils.show_error(f"Error in __manage_crud: {error}")

    def __manage_api(self):
        try:
            RoutersBuild(self, apps).build()
            RoutersBuild(self, apps).add_route_to_core()
        except Exception as error:
            Utils.show_error(f"Error in __manage_crud: {error}")

    def __manage_docker(self):
        """
        Manager para configurar os arquivos de desenvolvimento e produção
        do projeto para rodar em docker
        """
        try:
            DockerBuild(self).build()
        except Exception as error:
            Utils.show_error(f"Error in __manage_docker: {error}")

    def __manage_format_code(self):
        """
        Manager para formatar os arquivos do projeto
        """
        try:
            PythonFormatter(self.path_model_fastapi).format()
            PythonFormatter(self.path_schema).format()
            PythonFormatter(self.path_crud).format()
            PythonFormatter(self.path_api).format()

        except Exception as error:
            Utils.show_error(f"Error in __manage_format_code: {error}")

    def __set_paths(self, app):
        self.app = app.strip()
        self.path_root = os.path.normpath(os.getcwd() + os.sep)
        self.path_app = os.path.join(self.fastapi_dir, app)
        self.path_app_local = os.path.join(self.path_root, app)
        self.path_core = os.path.join(self.BASE_DIR, "core")
        self.path_model = os.path.join(self.path_app_local, "models.py")
        self.app_lower = app.lower()
        self.path_schema = os.path.join(self.path_app, "schemas.py")
        self.path_model_fastapi = os.path.join(self.path_app, "models.py")
        self.path_crud = os.path.join(self.path_app, "cruds.py")
        self.path_api = os.path.join(self.path_app, "api.py")
        self.app_instance = apps.get_app_config(self.app_lower)

    def call_methods(self, options):
        if options["cruds"]:
            Utils.show_message("Trabalhando apenas os cruds.")
            self.__manage_cruds()

        elif options["api"]:
            Utils.show_message("Trabalhando apenas a api.")
            self.__manage_api()

        elif options["schemas"]:
            Utils.show_message("Trabalhando apenas os schemas.")
            self.__manage_schema()

        elif options["models"]:
            Utils.show_message("Trabalhando apenas os models.")
            self.__manage_model()

        elif options["docker"]:
            Utils.show_message("Trabalhando apenas no docker.")
            self.__manage_docker()

        elif options["format"]:
            Utils.show_message("[b cyan]Formatando[/] código")
            self.__manage_format_code()

        elif options["all"]:
            self.__manage_api()
            self.__manage_schema()
            self.__manage_model()
            self.__manage_cruds()
            self.__manage_format_code()
        return

    def __verify_valid_flags(self, options):
        """Verificações comuns para as flags"""
        if not bool(
            (
                options.get("cruds")
                or options.get("api")
                or options.get("schemas")
                or options.get("models")
                or options.get("docker")
                or options.get("format")
                or options.get("all")
                or options.get("base")
            )
        ):
            Utils.show_error(
                "Para gerar o projeto é necessário informar uma das flags:\
                \n[b cyan]--cruds\n--api\n--schemas\n--models\n--docker\n--format\
                \n--all\n--base[/]"
            )

    @staticmethod
    def __verify_app(path_root, app):
        """Verificações comuns para App"""
        if not app:
            Utils.show_error("Você deve informar o nome da App")

        if Utils.contain_number(app):
            Utils.show_error("O nome da App não pode conter números")

        if apps.is_installed(app) is False:
            Utils.show_error(
                f"App [b cyan]{app}[/] deve estar no [b cyan]INSTALLED_APPS[/] do settings"
            )

        if app not in FASTAPI_APPS:
            Utils.show_error(
                f"App [b cyan]{app}[/] deve estar no [b cyan]FASTAPI_APPS[/] do settings"
            )

        if Utils.check_dir(Path(f"{path_root}/{app}")) is False:
            Utils.show_error(f"Diretório da App [b cyan]{app}[/] não encontrado")

    @staticmethod
    def __verify_model(path_root: Path, app: str, model: str) -> None:
        """Verificações comuns para Model"""
        if Utils.contain_number(model):
            Utils.show_error("O nome do Model não pode conter números")

        if (
            Utils.check_content(Path(f"{path_root}/{app}/models.py"), f"class {model}")
            is False
        ):
            Utils.show_error(
                f"Modelo [b red]{model}[/] não encontrado na App [b red]{app}[/]"
            )

        try:
            apps.get_app_config(app).get_model(model)
        except LookupError:
            Utils.show_error(f"Modelo [b red]{model}[/] não pode ser abstrato")

    def __get_apps_and_models_to_generate(self, app: str, model: str) -> dict:
        """Método responsável por retornar as apps e models que serão gerados"""
        generate_these: dict = {}
        # { app : [model1, model2, model3] }

        if app:
            self.__verify_app(self.path_root, app)
            generate_these[app] = []

        else:
            for work_app in FASTAPI_APPS:
                self.__verify_app(self.path_root, work_app)
                generate_these[work_app] = []

        if model:
            self.__verify_model(self.path_root, app, model)
            self.app_instance = apps.get_app_config(app)
            model = self.app_instance.get_model(model)
            generate_these[app].append(model)

        else:
            for work_app in generate_these:
                self.app_instance = apps.get_app_config(work_app)
                for work_model in self.app_instance.get_models():
                    generate_these[work_app].append(work_model)

        return generate_these

    def __generate_app_models(self, app: str, models: list, options: dict) -> None:
        """Método responsável por gerar os models"""

        Utils.show_core_box(f"App {app}", tipo="app")

        self.__set_paths(app)
        self.app_instance = apps.get_app_config(app)
        self.__init_app(self.path_app)

        with Utils.ProgressBar() as bar:
            task = bar.add_task("", total=len(models))
            for i, model in enumerate(models):
                bar.update(
                    task,
                    description=f"Gerando App [b green]{self.app}[/]:[b cyan]{model.__name__}[/] - [{i+1}/{len(models)}]",
                )
                Utils.show_core_box(
                    f"Model {app}:{model.__name__}",
                    tipo="model",
                )
                self.model: str = model.__name__.strip()
                self.model_lower: str = model.__name__.lower().strip()
                Utils.create_directory(f"{self.path_app}/{self.model_lower}")
                self.call_methods(options)

                bar.advance(task, 1)

    def handle(self, *args, **options):
        Utils.show_core_box("", tipo="core")
        app = options["App"] or None
        model = options["Model"] or None

        self.__verify_valid_flags(options)

        if options["base"]:
            self.__manage_projeto()
            return

        if options["docker"]:
            self.__manage_docker()
            return

        if not app and not model and not FASTAPI_APPS:
            Utils.show_error(
                "Você não informou uma APP para ser gerada e não existe nenhuma app na constante FASTAPI_APPS"
            )
            return

        if app is not None:
            self.app_lower = app.lower()

        if model is not None:
            self.model_lower = model.lower()

        if app and FASTAPI_APPS is None:
            Utils.show_error(
                "Você informou uma APP para ser gerada, mas não existe nenhuma app na constante FASTAPI_APPS"
            )
            return

        generate_these = self.__get_apps_and_models_to_generate(app, model)

        self.__manage_projeto()

        for app, models in generate_these.items():
            self.__generate_app_models(app, models, options)

        Utils.show_message("Processo concluído", title=True, emoji="rocket")
