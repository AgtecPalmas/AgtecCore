from pathlib import Path

from core.management.commands.flutter_managers.utils import convert_to_camel_case
from core.management.commands.utils import Utils


class NamedRoutesBuilder:
    def __init__(self, command, app) -> None:
        self.command = command
        self.app = app
        self._app_name = self.app.app_name
        self._app_name_lower = self._app_name.lower()
        self._snippet_dir = self.command.snippet_dir
        self._flutter_dir = self.command.flutter_dir
        self._current_model = None
        self._current_page_name = None
        self._content = None

        self._pages_name = ["IndexPage", "DetailPage", "ListPage", "UpdatePage", "AddPage"]
        self._imports_name = ["index", "list", "detail", "update", "create"]
        self._routers_apps = ""
        self._imports_apps = ""
        self._snippet_imports = "import 'apps/$APP$/$model$/pages/$page$.dart';"
        self._snippet_route = "case $ClassName$$PageName$.routeName:\n"
        self._snippet_route += "    return CupertinoPageRoute(builder: (_) => $ClassName$$PageName$());\n"

        # Snippet para rotas de edição e detalhamento
        self._snippet_route_created_updated = "case $ClassName$$PageName$.routeName:\n"
        self._snippet_route_created_updated += "  if(args is $ClassName$Model)\n"
        self._snippet_route_created_updated += (
            "    return CupertinoPageRoute(builder: (_) => $ClassName$$PageName$("
            "$ModelClassCamelCase$Model: args));\n"
        )
        self._snippet_route_created_updated += "  return CupertinoPageRoute(builder: (_) => $ClassName$$PageName$($ModelClassCamelCase$Model: $ClassName$Model()));\n"

        self._routes_target_file = Path(f"{self._flutter_dir}/lib/routers.dart")
        self._routes_snippet_file = Path(f"{self._snippet_dir}/named_route.txt")

    def build(self):
        try:
            self._content = Utils.get_snippet(str(self._routes_snippet_file))
            for _model in self.app.models:
                self._current_model = _model[1]
                for _page_name in self._pages_name:
                    self._current_page_name = _page_name
                    self._build_routers()
                self._build_import_names()
                self._save_file()
        except Exception as e:
            Utils.show_error(f"Erro ao executar o build de NamedRoutesBuilder: {e}")
            raise e

    def _save_file(self):
        try:
            if self._routers_apps != "":
                _content = self._content.replace("$ROUTES_APPS$", self._routers_apps).replace(
                    "$IMPORTS$", self._imports_apps
                )
                with open(self._routes_target_file, "w", encoding="utf-8") as _file:
                    _file.write(_content)
        except Exception as e:
            Utils.show_error(f"Erro ao executar o _save_file de NamedRoutesBuilder: {e}", exit=True)
            raise e

    def _build_import_names(self):
        try:
            for _import_name in self._imports_name:
                self._imports_apps += (
                    self._snippet_imports.replace("$APP$", self._app_name_lower)
                    .replace("$model$", self._current_model.lower())
                    .replace("$page$", _import_name)
                )
                self._imports_apps += "\n"
            _import_string = "import 'apps/$APP$/$model$/model.dart';\n"
            self._imports_apps += _import_string.replace("$APP$", self._app_name_lower).replace(
                "$model$", self._current_model.lower()
            )
        except Exception as e:
            Utils.show_error(f"Erro ao executar o _build_import_names de NamedRoutesBuilder: {e}")
            raise e

    def _build_routers(self):
        try:
            if self._current_page_name in ["UpdatePage", "DetailPage"]:
                self._routers_apps += (
                    self._snippet_route_created_updated.replace("$ClassName$", self._current_model)
                    .replace("$ModelClassCamelCase$", convert_to_camel_case(self._current_model))
                    .replace("$PageName$", self._current_page_name)
                )
            else:
                self._routers_apps += self._snippet_route.replace("$ClassName$", self._current_model).replace(
                    "$PageName$", self._current_page_name
                )
            self._routers_apps += "\n"
        except Exception as e:
            Utils.show_error(f"Erro ao executar o _build_routers de NamedRoutesBuilder: {e}")
            raise e
