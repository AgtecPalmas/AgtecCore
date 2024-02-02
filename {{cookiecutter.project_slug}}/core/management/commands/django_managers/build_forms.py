from ..utils import Utils


class FormsBuild:
    def __init__(self, command, apps):
        self.command = command
        self.apps = apps
        self.path_core = self.command.path_core
        self.snippet_form = (
            f"{self.path_core}/management/commands/snippets/django/forms/form.txt"
        )
        self.snippet_form_url = (
            f"{self.path_core}/management/commands/snippets/django/forms/form_urls.txt"
        )
        self.path_form = f"{self.command.path_form}/{self.command.model_lower}.py"
        self.path_root_form = self.command.path_form
        self.app = self.command.app
        self.model = self.command.model

    def build(self):
        try:
            content = Utils.get_snippet(str(self.snippet_form))
            content_urls = Utils.get_snippet(str(self.snippet_form_url))
            content = content.replace("$ModelClass$", self.model)
            content_urls = content_urls.replace("$ModelClass$", self.model)
            content_urls = content_urls.replace("$app$", self.app)

            if Utils.check_dir(self.path_root_form) is False:
                Utils.create_directory(self.path_root_form, True)

            if Utils.check_file(self.path_form) is False:
                with open(self.path_form, "w", encoding="utf-8") as arquivo:
                    arquivo.write(content_urls + "\n" + content)
                Utils.show_message("Forms criados com sucesso")
                return

            if Utils.check_file_is_locked(self.path_form) is True:
                return

            if Utils.check_content(self.path_form, f"class {self.model}Form"):
                Utils.show_message("[cyan]Forms[/] já existem")
                return

            if Utils.check_content(self.path_form, "from core.forms import BaseForm"):
                content_urls = content_urls.split("\n")[1]
                with open(self.path_form, "r", encoding="utf-8") as arquivo:
                    data = []
                    for line in arquivo:
                        if line.startswith("from .models import"):
                            models = line.split("import")[-1].rstrip()
                            import_model = f", {content_urls.split()[-1]}"
                            models += import_model
                            line = f"from .models import{models}\n"
                        data.append(line)
                with open(self.path_form, "w", encoding="utf-8") as arquivo:
                    arquivo.writelines(data)
            else:
                with open(self.path_form, "a", encoding="utf-8") as views:
                    views.write(content_urls)
            with open(self.path_form, "a", encoding="utf-8") as form:
                form.write("\n")
                form.write(content)
        except Exception as error:
            Utils.show_error(f"Erro ao criar os FormsBuild.build: {error}")
