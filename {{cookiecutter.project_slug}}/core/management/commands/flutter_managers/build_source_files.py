import logging
import os

from core.management.commands.utils import Utils

logger = logging.getLogger("django_debug")


class SourceFileBuilder:
    def __init__(self, command, source_app, app_name, model_name) -> None:
        self.command = command
        self._flutter_dir = self.command.flutter_dir
        if app_name is None:
            Utils.show_error("É necessário passar a App", exit=True)
            return

        if model_name is None:
            Utils.show_error("É necessário passar o Model", exit=True)
            return

        self._source_app = source_app
        self._app_name = self._source_app.app_name
        self._model_name = self._source_app.model_name
        self._model = self._source_app.model
        self._model_dir = self._source_app.get_path_app_model_dir()
        self._views_dir = self._source_app.get_path_views_dir()
        self._data_file = self._source_app.get_path_data_file()
        self._model_file = self._source_app.get_path_model_file()
        self._service_file = self._source_app.get_path_service_file()
        self._controller_file = self._source_app.get_path_cubit_file()
        self._controller_state_file = self._source_app.get_path_cubit_state_file()
        self._views = self._source_app.get_path_files_views()

    def build(self):
        try:
            if Utils.check_dir(self._model_dir) is False:
                os.makedirs(self._model_dir)

            self._build_views()

            self._build_model_file()
            self._build_data_file()
            Utils.show_message("Source do Model criado com sucesso")

        except Exception as e:
            logger.error(
                f"Ocorreu o erro: {e} ao executar o build do SourceFileBuilder"
            )

    def _build_views(self):
        try:
            if Utils.check_dir(self._views_dir) is False:
                os.makedirs(self._views_dir)
                if self._views is not None:
                    with open(self._views[0], "w", encoding="utf-8") as _file:
                        _file.write(
                            f"// Create Page {self._app_name} {self._model_name}"
                        )

                    with open(self._views[1], "w", encoding="utf-8") as _file:
                        _file.write(
                            f"// Detail Page {self._app_name} {self._model_name}"
                        )

                    with open(self._views[2], "w", encoding="utf-8") as _file:
                        _file.write(
                            f"// Index Page {self._app_name} {self._model_name}"
                        )

                    with open(self._views[3], "w", encoding="utf-8") as _file:
                        _file.write(f"// List Page {self._app_name} {self._model_name}")

                    with open(self._views[4], "w", encoding="utf-8") as _file:
                        _file.write(
                            f"// Update Page {self._app_name} {self._model_name}"
                        )
        except Exception as e:
            Utils.show_error(
                f"Ocorreu o erro: {e} ao executar o _build_views do SourceFileBuilder"
            )

    def _build_model_file(self):
        try:
            if not Utils.check_file(self._model_file):
                with open(self._model_file, "w", encoding="utf-8") as _file:
                    _file.write(f"// Modelo do {self._model_name}")
        except Exception as e:
            Utils.show_error(
                f"Ocorreu o erro: {e} ao executar o _build_model_file do SourceFileBuilder"
            )

    def _build_data_file(self):
        try:
            if not Utils.check_file(self._data_file):
                with open(self._data_file, "w", encoding="utf-8") as _file:
                    _file.write(f"// Persistência do {self._model_name}")
        except Exception as e:
            Utils.show_error(
                f"Ocorreu o erro: {e} ao executar o _build_data_file do SourceFileBuilder"
            )

    def _build_service_file(self):
        try:
            if not Utils.check_file(self._service_file):
                with open(self._service_file, "w", encoding="utf-8") as _file:
                    _file.write(f"// Service do {self._model_name}")
        except Exception as e:
            Utils.show_error(
                f"Ocorreu o erro: {e} ao executar o _build_service_file do SourceFileBuilder"
            )

    def _build_controller_files(self):
        try:
            if not Utils.check_file(self._controller_file):
                with open(self._controller_file, "w", encoding="utf-8") as _file:
                    _file.write(f"// Controller do {self._model_name}")
            if not Utils.check_file(self._controller_state_file):
                with open(self._controller_state_file, "w", encoding="utf-8") as _file:
                    _file.write(f"// Controller do {self._model_name}")
        except Exception as e:
            Utils.show_error(
                f"Ocorreu o erro: {e} ao executar o _build_service_file do SourceFileBuilder"
            )
