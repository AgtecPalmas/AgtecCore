import os
from pathlib import Path

from ..utils import Utils


class DRFBuild:
    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )

    def __init__(self, command, apps):
        self.command = command
        self.apps = apps

        self.path_core = self.command.path_core
        self.path_base = f"{self.command.path_root}/base"
        self.path_api = self.command.path_api
        self.path_serializer = Path(
            f"{self.command.path_api_serializers}/{self.command.model_lower}.py"
        )
        self.path_views = Path(
            f"{self.command.path_api_views}/{self.command.model_lower}.py"
        )
        self.path_router = self.command.path_api_routers

        self.templates_dir = f"{self.command.path_template_dir}"
        self.snippets_dir = f"{self.path_core}/management/commands/snippets/django/api"
        self.snippet_serializer = f"{self.snippets_dir}/serializer.txt"
        self.snippet_view = f"{self.snippets_dir}/view.txt"
        self.snippet_router = f"{self.snippets_dir}/router.txt"

        self.app = self.command.app
        self.model = self.command.model

        if Utils.check_dir(self.path_api) is False:
            Utils.create_directory(self.path_api)

    def build(self):
        try:
            self.create_folders()
            self.manage_serializers()
            self.manage_views()
            self.manage_routers()
            self.manage_routers_base()

        except Exception as error:
            Utils.show_message(f"Erro ao executar o DRFBuild.build: {error}", "error")

    def create_folders(self) -> None:
        folders: list = [
            "views",
            "serializers",
        ]

        for folder in folders:
            if Utils.check_dir(f"{self.path_api}/{folder}") is False:
                Utils.create_directory(f"{self.path_api}/{folder}", True)

    def manage_serializers(self):
        try:
            content = Utils.get_snippet(self.snippet_serializer)
            content = (
                content.replace("$ModelClass$", self.model)
                .replace("$app_name$", self.app)
                .replace("$ModelName$", self.model)
            )

            if Utils.check_file(self.path_serializer) is False:
                with open(self.path_serializer, "w", encoding="utf-8") as arquivo:
                    arquivo.write(f"\n{content}")
                Utils.show_message("Serializers criados com sucesso")
                return

            if Utils.check_file_is_locked(self.path_serializer) is True:
                return

            if Utils.check_content(
                self.path_serializer, f"class {self.model}Serializer"
            ):
                Utils.show_message("[cyan]Serializers[/] já existem")
                return

            with open(self.path_serializer, "a", encoding="utf-8") as urls:
                urls.write(f"\n{content}")

        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o DRFBuild.manager_serializers {error} do models {self.model}",
            )

    def manage_views(self):
        try:
            content = Utils.get_snippet(self.snippet_view)
            content = content.replace("$ModelName$", self.model).replace(
                "$app_name$", self.app
            ).replace("$model_name$", self.model.lower())

            if Utils.check_file(self.path_views) is False:
                with open(self.path_views, "w", encoding="utf-8") as api_views_file:
                    api_views_file.write(content)

                Utils.show_message("Views API criados com sucesso")
                return

            if Utils.check_content(self.path_views, f" {self.model}ViewAPI"):
                Utils.show_message(
                    "[cyan]Views API[/] já existem",
                )
                return

            with open(self.path_views, "a", encoding="utf-8") as api_views:
                api_views.write(f"\n{content}")

        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o DRFBuild.manage_views {error} do models {self.model}",
            )

    def manage_routers(self):
        try:
            content = Utils.get_snippet(self.snippet_router)
            content = (
                content.replace("$app_name$", self.app.lower())
                .replace("$ModelName$", self.model)
                .replace("$model_name$", self.model.lower())
            )

            if Utils.check_file(self.path_router) is False:
                with open(self.path_router, "w", encoding="utf-8") as api_url_file:
                    api_url_file.write(content)
                Utils.show_message("URLs API criados com sucesso")
                return

            if Utils.check_content(self.path_router, f"{self.model}ViewAPI"):
                Utils.show_message(
                    "[cyan]URLs API[/] já existem",
                )
                return

            content = content.replace("router = routers.DefaultRouter()", "").replace(
                "urlpatterns = router.urls", ""
            )

            with open(self.path_router, "r", encoding="utf-8") as api_url_file:
                old_content = api_url_file.read()
                old_content = old_content.replace("urlpatterns = router.urls", "")

            with open(self.path_router, "w", encoding="utf-8") as api_url_file:
                api_url_file.write(
                    old_content + "\n" + content + "\nurlpatterns = router.urls"
                )

        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o DRFBuild.manage_router_urls {error} do models {self.model}",
            )

    def manage_routers_base(self):
        try:
            content_exist = False
            new_data = ""
            content_include = "    path('$app_name$/api/v1/', include('$app_name$.api.routers')),".replace(
                "$app_name$", self.app.lower()
            )
            with open(
                Path(f"{self.path_base}/urls_api.py"), "r", encoding="utf-8"
            ) as urlsapi:
                new_data = urlsapi.read()
                if self.app.lower() in new_data:
                    return
                new_data = new_data.replace("]", f"{content_include}\n]")
            if content_exist:
                return
            with open(
                Path(f"{self.path_base}/urls_api.py"), "w", encoding="utf-8"
            ) as urlsapi:
                urlsapi.write(new_data)
        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o DRFBuild.manage_api {error} do models {self.model}",
            )
