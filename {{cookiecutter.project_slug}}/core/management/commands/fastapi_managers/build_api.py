import os
from pathlib import Path

from ..formatters import PythonFormatter
from ..utils import Utils


class ApiBuild:
    def __init__(self, command, apps):
        self.command = command
        self.apps = apps
        self.app = self.command.app
        self.model = self.command.model
        self.model_lower = self.model.lower()
        self.snippet_dir = Path(f"{self.command.path_command}/snippets/fastapi/")
        self.path_app = os.path.join(self.command.fastapi_dir, self.app)
        self.path_api: Path = Path(f"{self.path_app}/{self.model_lower}/api.py")
        self.path_core_api = Path(f"{self.command.fastapi_dir}/core/api.py")

    def build(self):
        try:
            content = Utils.get_snippet(str(Path(f"{self.snippet_dir}/api.txt")))
            if self.app.lower() == "usuario" and self.model.lower() == "usuario":
                content = Utils.get_snippet(
                    str(Path(f"{self.snippet_dir}/api_user.txt"))
                )

            content = content.replace("$ModelClass$", self.model)
            content = content.replace("$app$", self.app)
            content = content.replace("$model$", self.model_lower)

            if Utils.check_file(self.path_api) is False:
                with open(self.path_api, "w") as arquivo:
                    arquivo.write(content)
                PythonFormatter(self.path_api).format()
                Utils.show_message("[cyan]APIs[/] criadas com sucesso")
                return

            if Utils.check_content(self.path_api, f"@router_{self.model_lower}"):
                Utils.show_message("[cyan]APIs[/] já existem")
                return

            if Utils.check_content(self.path_api, "router = APIRouter()"):
                content = content.replace("router = APIRouter()", "")

            with open(self.path_api, "a") as crud:
                crud.write("\n")
                crud.write(content)

            PythonFormatter(self.path_api).format()
            Utils.show_message("[cyan]APIs[/] criadas com sucesso")

        except Exception as error:
            Utils.show_error(f"Erro ao criar o arquivo api.py: {error}")

    def add_route_core(self):
        if not Utils.check_content(
            self.path_core_api,
            f"from {self.app}.api import router as {self.app}_router",
        ):
            with open(self.path_core_api, "a") as core_api:
                core_api.write(
                    f"from {self.app}.{self.model_lower}.api import router as {self.app}_{self.model_lower}_router\n"
                )
                core_api.write(
                    f'api_router.include_router({self.app}_{self.model_lower}_router, prefix="/{self.app}")\n'
                )

            PythonFormatter(self.path_core_api).format()
            Utils.show_message("[cyan]APIs[/] adicionadas ao base")
            return

        Utils.show_message("[cyan]APIs[/] já existem no base")
