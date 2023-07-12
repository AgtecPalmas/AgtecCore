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
        self.path_serializer = self.command.path_serializer
        self.path_api_views = self.command.path_api_views
        self.path_api_urls = self.command.path_api_urls

        self.templates_dir = f"{self.command.path_template_dir}"
        self.snippets_dir = f"{self.path_core}/management/commands/snippets/django_api"
        self.snippet_serializer = f"{self.snippets_dir}/serializer.txt"
        self.snippet_serializer_url = f"{self.snippets_dir}/serializer_urls.txt"
        self.snippet_api_view = f"{self.snippets_dir}/api_view.txt"
        self.snippet_api_urls = f"{self.snippets_dir}/api_urls.txt"
        self.snippet_api_router = f"{self.snippets_dir}/api_router.txt"
        self.snippet_api_routers = f"{self.snippets_dir}/api_router_urls.txt"

        self.app = self.command.app
        self.model = self.command.model
        self.fields_list_serializer_mixin = (
            "from drf_jsonmask.serializers import FieldsListSerializerMixin"
        )

        if Utils.check_dir(self.path_api) is False:
            Utils.create_directory(self.path_api)

    def build(self):
        try:
            self.manage_serializers()
            self.manage_views()
            self.manage_router_urls()
            self.manage_urls_api()

        except Exception as error:
            Utils.show_message(f"Erro ao executar o DRFBuild.build: {error}", "error")

    def manage_serializers(self):
        try:
            content = Utils.get_snippet(self.snippet_serializer)
            content_urls = Utils.get_snippet(self.snippet_serializer_url)
            content = content.replace("$ModelName$", self.model)
            content = content.replace("$ModelClass$", self.model).replace(
                "$app_name$", self.app
            )
            content_urls = content_urls.replace("$ModelName$", self.model).replace(
                "$app_name$", self.app
            )
            if Utils.check_file(self.path_serializer) is False:
                with open(self.path_serializer, "w", encoding="utf-8") as arquivo:
                    arquivo.write(content_urls + "\n\n" + content)
                Utils.show_message("Serializers criados com sucesso")
                return

            if Utils.check_file_is_locked(self.path_serializer) is True:
                return

            if Utils.check_content(
                self.path_serializer, f"class {self.model}Serializer"
            ):
                Utils.show_message("[cyan]Serializers[/] já existem")
                return

            if Utils.check_content(
                self.path_serializer, self.fields_list_serializer_mixin
            ):
                content = content.replace(self.fields_list_serializer_mixin, "")

            if Utils.check_content(
                self.path_serializer,
                "from rest_framework.serializers import ModelSerializer",
            ):
                content_urls = content_urls.split("\n")[1]
                with open(self.path_serializer, "r") as serializer_file:
                    data = []
                    for line in serializer_file:
                        if line.startswith(f"from {self.app}.models import"):
                            models = line.split("import")[-1].rstrip()
                            import_model = f", {content_urls.split()[-1]}"
                            models += import_model
                            line = f"from {self.app}.models import{models}\n"
                        data.append(line)
                with open(
                    self.path_serializer, "w", encoding="utf-8"
                ) as serializer_file:
                    serializer_file.writelines(data)
            else:
                with open(self.path_serializer, "a", encoding="utf-8") as views:
                    views.write(content_urls)
            with open(self.path_serializer, "a", encoding="utf-8") as urls:
                urls.write("\n")
                urls.write(content)

        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o DRFBuild.manager_serializers {error} do models {self.model}",
            )

    def manage_views(self):
        try:
            content = Utils.get_snippet(self.snippet_api_view)
            content_urls = Utils.get_snippet(self.snippet_api_urls)
            content = content.replace("$ModelName$", self.model).replace(
                "$app_name$", self.app
            )
            content_urls = content_urls.replace("$ModelName$", self.model).replace(
                "$app_name$", self.app
            )

            if Utils.check_file(self.path_api_views) is False:
                with open(self.path_api_views, "w", encoding="utf-8") as api_views_file:
                    api_views_file.write(content_urls + content)
                Utils.show_message("Views API criados com sucesso")
                return

            if Utils.check_content(self.path_api_views, f" {self.model}ViewAPI"):
                Utils.show_message(
                    "[cyan]Views API[/] já existem",
                )
                return

            if Utils.check_content(
                self.path_api_views, "from rest_framework.viewsets import ModelViewSet"
            ):
                content = content.replace(
                    "from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet",
                    "",
                )
                content = content.strip()

            if Utils.check_content(
                self.path_api_views,
                "from drf_jsonmask.views import OptimizedQuerySetMixin",
            ):
                content = content.replace(
                    "from drf_jsonmask.views import OptimizedQuerySetMixin", ""
                )
                content = content.strip()

            if Utils.check_content(
                self.path_api_views, "from rest_framework import filters"
            ):
                content = content.replace(
                    "from rest_framework import filters, status", ""
                )
                content = content.strip()

            if Utils.check_content(
                self.path_api_views,
                "from rest_framework.permissions import IsAuthenticated",
            ):
                content = content.replace(
                    "from rest_framework.permissions import IsAuthenticated", ""
                )
                content = content.strip()

            if Utils.check_content(
                self.path_api_views,
                "from rest_framework.decorators import permission_classes",
            ):
                content = content.replace(
                    "from rest_framework.decorators import permission_classes", ""
                )
                content = content.strip()

            if (
                Utils.check_content(self.path_api_views, self.model, use_regex=True)
                is False
            ):
                content_models = content_urls.split("\n")[5]
                with open(self.path_api_views, "r", encoding="utf-8") as api_views_file:
                    data = []
                    for line in api_views_file:
                        if line.startswith(f"from {self.app}.models import"):
                            line = line.replace("\n", "") + f", {self.model} \n"
                        data.append(line)
                with open(self.path_api_views, "w", encoding="utf-8") as api_views_file:
                    api_views_file.writelines(data)
            else:
                content_urls = content_urls.rsplit("\n", 1)[0]

            if Utils.check_content(
                self.path_api_views, "from rest_framework.viewsets import ModelViewSet"
            ):
                content_urls = content_urls.split("\n")[4]
                with open(self.path_api_views, "r", encoding="utf-8") as api_views_file:
                    data = []
                    for line in api_views_file:
                        if line.startswith("from .serializers import"):
                            line = (
                                line.replace("\n", ", ")
                                + content_urls.replace("from .serializers import", "")
                                + "\n"
                            )
                        data.append(line)
                with open(self.path_api_views, "w", encoding="utf-8") as api_views_file:
                    api_views_file.writelines(data)
            else:
                with open(self.path_api_views, "a", encoding="utf-8") as views:
                    views.write("\n")
                    views.write(content_urls)

            with open(self.path_api_views, "a", encoding="utf-8") as api_views:
                api_views.write("\n")
                api_views.write(content)

        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o DRFBuild.manage_views {error} do models {self.model}",
            )

    def manage_router_urls(self):
        try:
            content = Utils.get_snippet(self.snippet_api_router)
            content = content.replace("$app_name$", self.app.lower())
            content = content.replace("$model_name$", self.model.lower())
            content = content.replace("$ModelName$", self.model)

            if Utils.check_file(self.path_api_urls) is False:
                api_url_file = open(self.path_api_urls, "w", encoding="utf-8")
                api_url_file.write(content)
                Utils.show_message("URLs API criados com sucesso")
                return
            content_file = open(self.path_api_urls, "r", encoding="utf-8")

            if content_file.read().find(f"{self.model}ViewAPI") != -1:
                Utils.show_message(
                    "[cyan]URLs API[/] já existem",
                )
                return

            # Variável que conterá o código sem o urlpatterns
            content_without_router = ""

            # Abrindo o arquivo para ler o conteúdo
            with open(
                self.path_api_urls, "r", encoding="utf-8"
            ) as read_api_urls_content:
                content_without_router = read_api_urls_content.read()

            # removendo o conteúdo router = router.urls
            content_without_router = content_without_router.replace(
                "urlpatterns = router.urls", ""
            )
            content_without_router = content_without_router.strip()

            # Abrindo o arquivo para gravar o novo valor
            with open(self.path_api_urls, "w", encoding="utf-8") as update_content_file:
                update_content_file.write(content_without_router)

            with open(self.path_api_urls, "a", encoding="utf-8") as api_url_file:
                content = content.replace("router = routers.DefaultRouter()", "")
                content = content.replace("from django.urls import include, path", "")
                content = content.replace("from rest_framework import routers", "")
                api_url_file.write(content)

        except Exception as error:
            Utils.show_error(
                f"Erro ao executar o DRFBuild.manage_urls {error} do models {self.model}",
            )

    def manage_urls_api(self):
        try:
            content_exist = False
            new_data = ""
            content_include = "    path('$app_name$/api/v1/', include('$app_name$.api.api_urls')),".replace(
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
