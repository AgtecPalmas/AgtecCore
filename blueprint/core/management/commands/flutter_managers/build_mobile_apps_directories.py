"""
Arquivo para gerar os diretórios de cada App e
internamente os subdiretórios:

    controllers,
    data,
    models,
    routes,
    pages,
    repositories,
    services e
    states

Os diretório serão utilizados para armazenar os arquivos
de cada model da App, que serão criados dentro pelo manager
build_mobile_apps_files
"""
from pathlib import Path

from core.management.commands.utils import Utils

from .build_mobile_apps_files import AppsMobileFilesBuilder
from .build_mobile_model_cubit import AppsMobileCubitStateManagerBuilder
from .build_mobile_model_models import AppsMobileModelBuilder
from .build_mobile_model_pages import AppsMobilePagesBuilder
from .build_mobile_model_router import AppsMobileRouterBuilder
from .build_mobile_model_service import AppsMobileServiceBuilder
from .build_mobile_model_widget_form import AppsMobileWidgetFormBuilder
from .build_mobile_model_data import AppsMobileDataBuilder

class AppsMobileDirectoriesBuilder:
    def __init__(self, command, app) -> None:
        self.command = command
        self.app = app
        self.flutter_dir = self.command.flutter_dir

    def build(self):
        """
        build _summary_
        """
        try:
            # Criando o diretório da app dentro de lib/apps
            Utils.show_message(f"Criando o diretório da app: {self.app.name}")
            _app_dir = Path(f"{self.flutter_dir}/lib/apps/{self.app.name.lower()}")
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
                AppsMobileFilesBuilder(self.command, self.app).build()

                # Chamando o método para criar os services das apps/models
                AppsMobileServiceBuilder(self.command, self.app).build()

                # Chamando o método para criar os models das apps/models
                AppsMobileModelBuilder(self.command, self.app).build()

                # Chamando o método para criar as páginas das apps/models
                AppsMobilePagesBuilder(self.command, self.app).build()

                # Chamando o método para criar o widget form das apps/models
                AppsMobileWidgetFormBuilder(self.command, self.app).build()

                # Chamando o método para criar o state do gerenciador de estado Cubit
                AppsMobileCubitStateManagerBuilder(self.command, self.app).build()

                # Chamando o método para criar o router das apps/models
                AppsMobileRouterBuilder(self.command, self.app).build()

                # Chamando o método para criar os arquivos de persistencia de dados local
                AppsMobileDataBuilder(self.command, self.app).build()

        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o build de AppsMobileDirectoriesBuilder: {error}"
            )
            return
