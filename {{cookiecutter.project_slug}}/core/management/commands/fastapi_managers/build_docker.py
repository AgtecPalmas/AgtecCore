"""
Classe responsável por realizar a configuração dos arquivos necessários
para executar o projeto em containers docker.
"""
from pathlib import Path

from django.utils.text import slugify

from base.settings import SYSTEM_NAME
from core.management.commands.utils import Utils


class DockerBuild:
    def __init__(self, command):
        self.command = command
        self.path_app = self.command.project
        self.slugify_project_name = slugify(str(SYSTEM_NAME))
        self.slugify_project_name = self.slugify_project_name.replace("-", "_")
        self.files = [
            "Dockerfile",
            "docker-compose.yml",
            "DockerfileDev",
            "docker-dev.yml",
        ]

    def build(self):
        # Lendo o conteúdo do arquivo Dockerfile
        for file_config in self.files:
            Utils.show_message(f"{file_config} pronto")

            __dockerfile = Path(f"{self.command.fastapi_dir}/{file_config}")
            with open(__dockerfile, "r") as file:
                dockerfile_content = file.read()

            # Substituindo o nome do projeto
            dockerfile_content = dockerfile_content.replace(
                "TROCAR_PELO_NOME_DO_SISTEMA", self.slugify_project_name
            )

            # Salvando o arquivo Dockerfile
            with open(__dockerfile, "w") as file:
                file.write(dockerfile_content)
