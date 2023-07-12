import os
from pathlib import Path

from ..formatters import PythonFormatter
from ..utils import Utils


class CrudsBuild:
    def __init__(self, command):
        self.command = command
        self.app = self.command.app
        self.model = self.command.model
        self.model_lower = self.model.lower()
        self.snippet_dir = Path(f"{self.command.path_command}/snippets/fastapi/")
        self.path_app = os.path.join(self.command.fastapi_dir, self.app)
        self.path_crud: Path = Path(f"{self.path_app}/{self.model_lower}/cruds.py")

    def build(self):
        try:
            content = Utils.get_snippet(str(Path(f"{self.snippet_dir}/cruds.txt")))
            content = content.replace("$ModelClass$", self.model)
            content = content.replace("$app$", self.app)
            content = content.replace("$model$", self.model_lower)

            if Utils.check_file(self.path_crud) is False:
                with open(self.path_crud, "w") as arquivo:
                    arquivo.write(content)
                Utils.show_message("[cyan]CRUDs[/] criados com sucesso")
                return

            if Utils.check_content(self.path_crud, f"class CRUD{self.model}"):
                Utils.show_message("[cyan]CRUDs[/] já existem")
                return

            with open(self.path_crud, "a") as crud:
                crud.write("\n")
                crud.write(content)
            PythonFormatter(self.path_crud).format()
            Utils.show_message("[cyan]CRUDs[/] criados com sucesso")

        except Exception as error:
            Utils.show_error(f"Erro ao criar o arquivo crud.py: {error}")
