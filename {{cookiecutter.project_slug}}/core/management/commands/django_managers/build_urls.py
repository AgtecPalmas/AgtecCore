import logging

from ..utils import Utils

logger = logging.getLogger("django_debug")


class UrlsBuild:
    def __init__(self, command, apps):
        self.command = command
        self.apps = apps
        self.path_core = self.command.path_core
        self.path_base_urls = self.command.path_base_urls
        self.snippets_dir = f"{self.path_core}/management/commands/snippets/django/urls"
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

    def __build_index_view_url(self):
        if Utils.check_content(
            self.path_urls, f"{self.app.title()}IndexTemplateView.as_view()"
        ):
            return

        content = (
            f"from {self.app}.views.index import {self.app.title()}IndexTemplateView\n"
        )
        content += f"app_name = '{self.app}'\n"
        content += f"urlpatterns = [path('{self.app.lower()}/', {self.app.title()}IndexTemplateView.as_view(), name='{self.app.lower()}-index'),]\n"

        Utils.append_file(self.path_urls, content)
        Utils.show_message("[cyan]IndexView[/] adicionada à urls.py")

    def build(self):
        try:
            content = Utils.get_snippet(self.snippets_url)
            new_imports = Utils.get_snippet(self.snippets_urls_imports)

            # Verificando se existe a entrada do nome da app
            content_app_name = 'app_name = "{}"'.format(self.app.lower())
            if Utils.check_content(self.path_urls, content_app_name):
                content = content.replace('app_name = "$app_name$"', "")

            content = content.replace("$app_name$", self.app.lower())
            content = content.replace("$app_title$", self.app.lower().title())
            content = content.replace("$model_name$", self.model.lower())
            content = content.replace("$ModelClass$", self.model)

            new_imports = new_imports.replace("$ModelClass$", self.model)
            new_imports = new_imports.replace("$app_name$", self.app.lower())
            new_imports = new_imports.replace("$model_name$", self.model.lower())

            if Utils.check_file(self.path_urls) is False:
                Utils.write_file(self.path_urls, "")

            # Verificando se o arquivo está bloqueado para escrita
            if Utils.check_file_is_locked(f"{self.path_urls}"):
                return

            self.__build_index_view_url()

            # Verificando se o arquivo já possui o conteúdo
            if Utils.check_content(self.path_urls, " {}ListView".format(self.model)):
                Utils.show_message("[cyan]URLs[/] já existem")
                return

            Utils.append_file(self.path_urls, f"{new_imports}\n{content}")

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
