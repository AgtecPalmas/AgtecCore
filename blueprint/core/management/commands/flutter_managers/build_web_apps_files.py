from pathlib import Path

from core.management.commands.utils import Utils


class AppsWebFilesBuilder:
    def __init__(self, command, app, model=None) -> None:
        self.command = command
        self.app = app
        self.model = model
        self.flutter_web_dir = self.command.flutter_dir
        self.flutter_project_path = Path(f"{self.command.path_command}/snippets/flutter_web_project/")

    def build(self):
        """
        build _summary_
        """
        try:
            # Criando o diretório da app dentro de lib/apps
            _sub_dirs = [
                "controllers",
                "data", "models", "pages", "repositories",
                "services", "states", "widgets"
            ]
            _app_dir = Path(f"{self.flutter_web_dir}/lib/apps/{self.app.name.lower()}")

            with Utils.ProgressBar() as bar:
                task = bar.add_task("", total=len(self.app.models))
                for i, model in enumerate(self.app.models):
                    bar.update(
                        task,
                        description=f"Gerando arquivos do [b green]{self.app.name}[/]:[b cyan]{model[1]}[/] - [{i + 1}/{len(self.app.models)}]",
                    )
                    for sub_dir in _sub_dirs:
                        if Utils.check_dir(_app_dir) is True:
                            if (
                                self.model is not None
                                and model.lower() != self.model.lower()
                            ):
                                continue
                            # Tratando quando forem gerados os arquivos de pages
                            if sub_dir == "pages":
                                _app_file = f"{_app_dir}/{sub_dir}/{model.lower()}.list.dart"
                                Path(f"{_app_file}").touch()
                                _app_file = f"{_app_dir}/{sub_dir}/{model.lower()}.content.dart"
                                Path(f"{_app_file}").touch()
                                continue

                            # Tratando quando forem gerados os arquivos do widgets
                            if sub_dir == "widgets":
                                _app_file = f"{_app_dir}/{sub_dir}/{model.lower()}.form.dart"
                                Path(f"{_app_file}").touch()
                                continue

                            _app_file = f"{_app_dir}/{sub_dir}/{model.lower()}.dart"
                            # Criando o arquivo de cada camada da app/models
                            Utils.show_message(
                                f"Criando {_app_file}"
                            )
                            Path(f"{_app_file}").touch()
                    bar.advance(task, 1)


        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o build de AppsWebDirectoriesBuilder: {error}"
            )
            return
