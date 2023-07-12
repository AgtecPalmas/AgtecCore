import json
import os
import random
import sys
from pathlib import Path


def create_cookiecutter_json_file_backup(path_cookiecutter_json_file):
    """ Método para criar o arquivo cookiecutter_backup.json """
    try:
        path_root = os.getcwd()
        path_path = Path(path_root)
        path_cookiecutter_json_file_backup = Path(f"{path_path.parent.parent}/AgtecCore/cookiecutter_backup.json")
        with open(path_cookiecutter_json_file, "r") as json_file:
            json_data = json.load(json_file)

        with open(path_cookiecutter_json_file_backup, "w") as json_file:
            json.dump(json_data, json_file, indent=4)

    except Exception as e:
        print(f"Erro ao criar o arquivo cookiecutter_backup.json: {e}")
        sys.exit(1)


def update_cookiecutter_key_docker_port():
    """ Método para atualizar o arquivo cookiecutter.json """
    try:
        path_root = os.getcwd()
        path_path = Path(path_root)
        path_cookiecutter_json_file = Path(f"{path_path.parent.parent}/AgtecCore/cookiecutter.json")
        create_cookiecutter_json_file_backup(path_cookiecutter_json_file)
        docker_post = str(random.randint(8100, 9000))
        postgre_port = str(random.randint(5500, 6500))
        with open(path_cookiecutter_json_file, "r") as json_file:
            json_data = json.load(json_file)

        json_data["docker_port"] = docker_post
        json_data["postgre_port"] = postgre_port

        with open(path_cookiecutter_json_file, "w") as json_file:
            json.dump(json_data, json_file, indent=4)

        sys.exit(0)
    except Exception as e:
        print(f"Erro ao atualizar a porta do docker: {e}")
        sys.exit(1)
