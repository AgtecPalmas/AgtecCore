import logging

from ..utils import Utils

logger = logging.getLogger("django_debug")


class UrlsBuild:
    def __init__(self, command, apps):
        self.command = command
        self.apps = apps
        self.path_core = self.command.path_core
        self.path_base_urls = self.command.path_base_urls
        self.snippets_dir = f"{self.path_core}/management/commands/snippets/django"
        self.templates_dir = f"{self.command.path_template_dir}"
        self.path_urls = self.command.path_urls
        self.snippets_urls_imports = f"{self.snippets_dir}/url_imports.txt"
        self.snippets_url = f"{self.snippets_dir}/url.txt"
        self.app = self.command.app
        self.model = self.command.model

    def get_verbose_name(self) -> str:
        """Método para retornar o verbose_name da app"""
        return (
            Utils.get_verbose_name(self.apps, app_name=self.app.lower())
            or self.app.lower()
        )

    @staticmethod
    def __get_views_from_content_urls(content: str) -> str:
        content = content.replace("(", "").replace(")", "").split("from ")
        views = []

        for item in content:
            if item.startswith(".views"):
                item = item.split("import ")[1]
                views.extend(
                    view.strip() for view in item.split(",") if "AppIndex" not in view
                )
        return views

    def build(self):
        try:
            content = Utils.get_snippet(self.snippets_url)
            content_urls = Utils.get_snippet(self.snippets_urls_imports)
            # Verificando se existe a entrada do nome da app
            content_app_name = 'app_name = "{}"'.format(self.app.lower())
            if Utils.check_content(self.path_urls, content_app_name):
                content = content.replace('app_name = "$app_name$"', "")
            content = content.replace("$app_name$", self.app.lower())
            content = content.replace("$app_title$", self.app.lower().title())
            content = content.replace("$model_name$", self.model.lower())
            content = content.replace("$ModelClass$", self.model)
            content_urls = content_urls.replace("$ModelClass$", self.model)

            # Verificando se o arquivo está bloqueado para escrita
            if Utils.check_file_is_locked(f"{self.path_urls}"):
                return

            # Verificando se o arquivo já possui o conteúdo
            if Utils.check_content(self.path_urls, " {}ListView".format(self.model)):
                Utils.show_message("[cyan]URLs[/] já existem")
                return

            content_include = "path('api/$app_name$/', include('$app_name$.api_urls')),"
            content_include = content_include.replace("$app_name$", self.app.lower())
            if Utils.check_content(self.path_urls, content_include):
                content = content.replace(content_include, "").strip()

            if Utils.check_content(
                self.path_urls, "{}IndexTemplateView".format(self.app.title())
            ):
                content_urls = content_urls.replace(", $AppIndexTemplate$", "")
            else:
                content_urls = content_urls.replace(
                    "$AppIndexTemplate$", "{}IndexTemplateView".format(self.app.title())
                )
            if Utils.check_file(self.path_urls) is False:
                with open(self.path_urls, "w", encoding="utf-8") as url_file:
                    url_file.write(content_urls + "\n" + content)
                return

            if Utils.check_content(self.path_urls, "from .views import"):
                content_views = self.__get_views_from_content_urls(content_urls)
                url_file = open(self.path_urls, "r", encoding="utf-8")
                data = []
                for line in url_file:
                    if line.startswith("from .views import"):
                        models = line.split("import")[-1].rstrip()
                        import_model = ", ".join(content_views)
                        models += f", {import_model}"
                        line = "from .views import{}\n".format(models)
                    data.append(line)
                url_file.close()
                url_file = open(self.path_urls, "w", encoding="utf-8")
                url_file.writelines(data)
                url_file.close()
            else:
                with open(self.path_urls, "a", encoding="utf-8") as views:
                    views.write(content_urls)

            if Utils.check_content(self.path_urls, "urlpatterns = ["):
                content = content.replace("urlpatterns = [", "urlpatterns += [")
                content = content.replace(
                    "path('api/{}/', include(router.urls)),\n    ".format(
                        self.app.lower()
                    ),
                    "",
                )
                _url_index_page = "path('{}/', {}IndexTemplateView.as_view(), name='{}-index'),\n    ".format(
                    self.app.lower(), self.app.title(), self.app.lower()
                )
                content = content.replace(_url_index_page, "")

            if Utils.check_content(self.path_urls, "app_name = '{}'".format(self.app)):
                content = content.replace("app_name = '{}'".format(self.app), "")

            if Utils.check_file_is_locked(self.path_urls) is True:
                return

            with open(self.path_urls, "a", encoding="utf-8") as urls:
                urls.write(content)

        except Exception as error:
            Utils.show_error(
                f"Erro ao criar o arquivo de urls: {error} do models {self.model}",
            )

    def add_url_to_base(self):
        """Método para adicionar a url da app ao arquivo base/urls.py"""

        insert_content = f'path("core/", include("{self.app.lower()}.urls", namespace="{self.app.lower()}")),'

        try:
            if Utils.check_file_is_locked(self.path_base_urls):
                return

            if Utils.check_content(
                self.path_base_urls, f'namespace="{self.app.lower()}"'
            ):
                Utils.show_message("[cyan]URLs[/] já fazem parte do Base")
                return

            with open(self.path_base_urls, "r", encoding="utf-8") as urls:
                content = urls.read().replace(
                    "# Urls do Swagger", f"{insert_content}\n# Urls do Swagger"
                )

            with open(self.path_base_urls, "w", encoding="utf-8") as urls:
                urls.write(content)
                Utils.show_message(
                    "[cyan]URLs[/] adicionadas ao base/urls.py",
                )

        except Exception as error:
            Utils.show_error(
                f"Erro ao adicionar a url da app {self.app} ao arquivo base/urls.py: {error}",
            )
