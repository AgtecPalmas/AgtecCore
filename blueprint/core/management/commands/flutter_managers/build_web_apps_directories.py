"""
Arquivo para gerar os diretórios de cada App e
internamente os subdiretórios:

    controllers,
    data,
    models,
    pages,
    repositories,
    services e
    states

Os diretório serão utilizados para armazenar os arquivos
de cada model da App, que serão criados dentro pelo manager
build_web_apps_files
"""
from pathlib import Path

from core.management.commands.utils import Utils

from .build_web_apps_files import AppsWebFilesBuilder
from .build_web_model_cubit import AppsWebCubitStateManagerBuilder
from .build_web_model_models import AppsWebModelBuilder
from .build_web_model_pages import AppsWebPagesBuilder
from .build_web_model_router import AppsWebRouterBuilder
from .build_web_model_service import AppsWebServiceBuilder
from .build_web_model_widget_form import AppsWebWidgetFormBuilder


class AppsWebDirectoriesBuilder:
    def __init__(self, command, app) -> None:
        self.command = command
        self.app = app
        self.flutter_web_dir = self.command.flutter_dir
        self.flutter_project_path = Path(f"{self.command.path_command}/snippets/flutter_web_project/")

    def build(self):
        """
        build _summary_
        """
        try:

            # Criando o diretório da app dentro de lib/apps
            Utils.show_message(f"Criando o diretório da app: {self.app.name}")
            _app_dir = Path(f"{self.flutter_web_dir}/lib/apps/{self.app.name.lower()}")
            if Utils.check_dir(_app_dir) is False:
                _app_dir.mkdir(parents=True, exist_ok=True)
                # Criando os subdiretórios
                _sub_dirs = [
                    "controllers", "data", "models",
                    "pages", "repositories",
                    "services", "states", 
                    "widgets", "routes"
                ]
                # Criando os subdiretórios da app
                for sub_dir in _sub_dirs:
                    Utils.show_message(f"Criando o diretório: {sub_dir}")
                    Path(f"{_app_dir}/{sub_dir}").mkdir(parents=True, exist_ok=True)
                
                # Chamando o método para criar os arquivos das apps/models
                AppsWebFilesBuilder(self.command, self.app).build()

                # Chamando o método para criar os services das apps/models
                AppsWebServiceBuilder(self.command, self.app).build()

                # Chamando o método para criar os models das apps/models
                AppsWebModelBuilder(self.command, self.app).build()

                # Chamando o método para criar as páginas das apps/models
                AppsWebPagesBuilder(self.command, self.app).build()

                # Chamando o método para criar o widget form das apps/models
                AppsWebWidgetFormBuilder(self.command, self.app).build()

                # Chamando o método para criar o state do gerenciador de estado Cubit
                AppsWebCubitStateManagerBuilder(self.command, self.app).build()

                # Chamando o método para criar o router das apps/models
                AppsWebRouterBuilder(self.command, self.app).build()

        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o build de AppsWebDirectoriesBuilder: {error}"
            )
            return
