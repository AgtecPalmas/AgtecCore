import os
from pathlib import Path

from ..formatters import PythonFormatter
from ..utils import Utils


class RoutersBuild:
    def __init__(self, command, apps):
        self.command = command
        self.apps = apps
        self.app = self.command.app
        self.model = self.command.model
        self.model_lower = self.model.lower()
        self.snippet_dir = Path(f"{self.command.path_command}/snippets/fastapi/")
        self.path_app = os.path.join(self.command.fastapi_dir, self.app)
        self.path_model_router: Path = Path(
            f"{self.path_app}/{self.model_lower}/routers.py"
        )
        self.path_app_router: Path = Path(f"{self.path_app}/routers.py")
        self.path_core_router = Path(f"{self.command.fastapi_dir}/core/routers.py")

    def __create_app_router(self):
        if Utils.check_file(self.path_app_router):
            return

        content = "from fastapi import APIRouter\n\nrouter = APIRouter()\n"

        with open(self.path_app_router, "w") as arquivo:
            arquivo.write(content)

        PythonFormatter(self.path_app_router).format()

    def build(self):
        try:
            self.__create_app_router()

            if Utils.check_content(
                self.path_model_router, f"@router_{self.model_lower}"
            ):
                Utils.show_message("[cyan]APIs[/] já existem")

            if Utils.check_content(
                self.path_app_router,
                f"router.include_router({self.model_lower}_router)",
            ):
                return

            self.__add_router_to_app()

            content = Utils.get_snippet(str(Path(f"{self.snippet_dir}/routers.txt")))
            content = content.replace("$ModelClass$", self.model)
            content = content.replace("$app$", self.app)
            content = content.replace("$model$", self.model_lower)

            if Utils.check_file(self.path_model_router) is False:
                with open(self.path_model_router, "w") as arquivo:
                    arquivo.write(content)
                PythonFormatter(self.path_model_router).format()
                Utils.show_message("[cyan]APIs[/] criadas com sucesso")
                return

            if Utils.check_content(self.path_model_router, "router = APIRouter()"):
                content = content.replace("router = APIRouter()", "")

            with open(self.path_model_router, "a") as crud:
                crud.write("\n")
                crud.write(content)

            PythonFormatter(self.path_model_router).format()
            Utils.show_message("[cyan]APIs[/] criadas com sucesso")

        except Exception as error:
            Utils.show_error(f"Erro ao criar o arquivo routers.py: {error}")

    def __add_router_to_app(self):
        try:
            _str_from_import = (
                f"from .{self.model_lower} import router as {self.model_lower}_router"
            )
            if not Utils.check_content(self.path_app_router, _str_from_import):
                content = Utils.get_snippet(
                    str(Path(f"{self.snippet_dir}/routers_app.txt"))
                )
                content = content.replace("$model$", self.model_lower)

                with open(self.path_app_router, "a") as app_api:
                    app_api.write(content)

                PythonFormatter(self.path_app_router).format()
                Utils.show_message("[cyan]APIs[/] adicionadas ao app")
                return

            Utils.show_message("[cyan]APIs[/] já existem no app")
        except Exception as error:
            Utils.show_error(f"Erro ao adicionar as APIs ao app: {error}")
            return

    def add_route_to_core(self):
        try:
            _str_from_import = (
                f"from {self.app}.routers import router as {self.app}_router"
            )
            if not Utils.check_content(self.path_core_router, _str_from_import):
                content = Utils.get_snippet(
                    str(Path(f"{self.snippet_dir}/routers_core.txt"))
                )
                content = content.replace("$app$", self.app)

                with open(self.path_core_router, "a") as core_api:
                    core_api.write(content)

                PythonFormatter(self.path_core_router).format()
                Utils.show_message("[cyan]APIs[/] adicionadas ao base")
                return

            Utils.show_message("[cyan]APIs[/] já existem no base")
        except Exception as error:
            Utils.show_error(f"Erro ao adicionar as APIs ao base: {error}")
            return
