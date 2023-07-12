from pathlib import Path

from ..utils import Utils


class TestsBuild:
    def __init__(self, command, apps):
        self.command = command
        self.apps = apps
        self.path_core = self.command.path_core

        self.core_snippets: Path = Path(
            f"{self.path_core}/management/commands/snippets/"
        )
        self.snippet_forms: Path = Path(f"{self.core_snippets}/django_tests/forms.txt")
        self.snippet_views: Path = Path(f"{self.core_snippets}/django_tests/views.txt")
        self.snippet_models: Path = Path(
            f"{self.core_snippets}/django_tests/models.txt"
        )
        self.snippet_models_import: Path = Path(
            f"{self.core_snippets}/django_tests/models_import.txt"
        )
        self.snippet_views_import: Path = Path(
            f"{self.core_snippets}/django_tests/views_import.txt"
        )
        self.snippet_forms_import: Path = Path(
            f"{self.core_snippets}/django_tests/forms_import.txt"
        )
        self.snippet_views_index: Path = Path(
            f"{self.core_snippets}/django_tests/views_index.txt"
        )

        self.path_tests: Path = self.command.path_tests
        self.path_tests_model: Path = Path(f"{self.path_tests}/tests_{self.command.model_lower}")
        self.app = self.command.app
        self.model = self.command.model
        self.model_lower = self.command.model_lower

        self.build_types: list = ["forms", "views", "models"]

    def build(self):
        Utils.create_directory(self.path_tests)
        Utils.create_directory(self.path_tests_model)
        Utils.create_file(f"{self.path_tests_model}/__init__.py")

        for build_type in self.build_types:
            novo_conteudo = Utils.get_snippet(
                str(getattr(self, f"snippet_{build_type}"))
            )
            novo_import = Utils.get_snippet(
                str(getattr(self, f"snippet_{build_type}_import"))
            )

            novo_conteudo = Utils.replace_content(
                novo_conteudo, self.model, self.app, self.model_lower
            )
            novo_import = Utils.replace_content(
                novo_import, self.model, self.app, self.model_lower
            )

            # Test da Index View
            if (
                Utils.check_content(
                    f"{self.path_tests_model}/tests_views.py", f"test_{self.app}_index"
                )
                is False
                and build_type == "views"
            ):
                views_index_template = Utils.get_snippet(str(self.snippet_views_index))
                views_index_template = Utils.replace_content(
                    views_index_template, self.model, self.app, self.model_lower
                )

                novo_conteudo = novo_conteudo + "\n" + views_index_template

            # Verifica se o arquivo já existe
            if Utils.check_file(f"{self.path_tests_model}/tests_{build_type}.py") is False:
                Utils.write_file(
                    f"{self.path_tests_model}/tests_{build_type}.py",
                    novo_import + "\n" + novo_conteudo,
                )
                Utils.show_message(
                    f"Testes de [cyan]{build_type}[/] criados com sucesso"
                )
                continue

            # Verifica se o arquivo está bloqueado
            if (
                Utils.check_file_is_locked(f"{self.path_tests_model}/tests_{build_type}.py")
                is True
            ):
                return

            # Verifica se o arquivo já possui o conteúdo do Model
            if Utils.check_content(
                f"{self.path_tests_model}/tests_{build_type}.py",
                f"class Test{self.model}{build_type.capitalize()}",
            ):
                Utils.show_message(f"Testes de [cyan]{build_type}[/] já existem")
                continue

            # Adiciona e organiza o conteúdo do Model
            if Utils.check_content(
                f"{self.path_tests_model}/tests_{build_type}.py",
                "import pytest",
            ):
                arquivo = Utils.read_file(f"{self.path_tests_model}/tests_{build_type}.py")
                data = []

                for line in arquivo:
                    # Adiciona os novos imports
                    if f"{self.app}.{build_type} import" in line:
                        imports_extraidos = Utils.get_item_from_imports(
                            novo_import, f"{self.app}.{build_type}"
                        )
                        imports_arquivo = line.split("import ")[-1].rstrip()
                        imports_combinados = (
                            f"{imports_arquivo}, {', '.join(imports_extraidos)}"
                        )
                        line = f"from {self.app}.{build_type} import {imports_combinados}\n"
                    data.append(line)

                    # Tratamento especial para Views pois importa Models
                    if build_type == "views" and f"{self.app}.models import" in line:
                        imports_extraidos = Utils.get_item_from_imports(
                            novo_import, f"{self.app}.models"
                        )
                        imports_arquivo = line.split("import ")[-1].rstrip()
                        imports_combinados = (
                            f"{imports_arquivo}, {', '.join(imports_extraidos)}"
                        )
                        line = f"from {self.app}.models import {imports_combinados}\n"
                        data.append(line)

                data.append("\n")

                Utils.write_file(
                    f"{self.path_tests_model}/tests_{build_type}.py",
                    "".join(data),
                )

            else:
                Utils.append_file(
                    f"{self.path_tests_model}/tests_{build_type}.py", "\n" + novo_import
                )

            Utils.append_file(
                f"{self.path_tests_model}/tests_{build_type}.py", "\n" + novo_conteudo
            )

            Utils.show_message(f"Testes de [cyan]{build_type}[/] criados com sucesso")
