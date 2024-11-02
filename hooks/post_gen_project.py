import os
import shutil
import subprocess
import sys
import typing as t
from pathlib import Path
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TimeRemainingColumn,
)
from subprocess import DEVNULL, PIPE

INSTALL_REQUIREMENTS = "{{ cookiecutter.install_requirements }}" == "Sim"

GIT_INIT = "{{ cookiecutter.git_init }}" == "Sim"

BUILD_APPS = "{{ cookiecutter.build_apps }}" == "Sim"

PYTHON = "py" if sys.platform.startswith("win") else "python"

DEFAULT_APPS = ["usuario", "configuracao_core"]

PROJECT_DIRECTORY = Path(os.path.realpath(os.path.curdir)).parent

REQUIREMENTS = [
    Path(f"{PROJECT_DIRECTORY}/requirements.txt"),
    Path(f"{PROJECT_DIRECTORY}/requirements-dev.txt"),
]

SECRET_COMMAND = [PYTHON, "contrib/secret_gen.py"]

EMOJIS = {"success": "\u2705", "error": "\u274C", "wait": "\u231B"}

GIT_COMMANDS = [
    "git init --initial-branch=master",
    "git add .",
    'git commit -am "Primeiro Commit"',
    "git checkout -b desenvolvimento",
]

VENV_ACTIVATED = os.environ.get("VIRTUAL_ENV")


def run_command(
    command: t.Union[str, list], silent: bool = False, exit_on_fail=False
) -> bool:
    """Método para executar um comando, retorna True se sucedido"""

    if not VENV_ACTIVATED:
        print(f"{EMOJIS['error']} Virtualenv desativado, comando ignorado")
        return False

    try:
        if silent:
            command = subprocess.run(
                command.split(" "),
                cwd=PROJECT_DIRECTORY,
                stdin=DEVNULL,
                stdout=DEVNULL,
                stderr=DEVNULL,
            )
        else:
            command = subprocess.run(command.split(" "), cwd=PROJECT_DIRECTORY)

        return command.returncode == 0

    except Exception as e:
        if exit_on_fail:
            raise subprocess.SubprocessError(f"Erro ao executar {command}: {e}") from e

        print(f"{EMOJIS['error']} Erro ao executar {command}: {e}")

        return False


def init_git() -> None:
    """Método para inicializar o git"""

    print(f"{EMOJIS['wait']} Inicializando o git")

    for command in GIT_COMMANDS:
        if run_command(command, silent=True):
            print(f"{EMOJIS['success']} {command}")


def get_secret_key() -> str:
    """Executa o comando python contrib/secrets.py
    para gerar uma SECRET_KEY e retorna a mesma"""

    process = subprocess.run(SECRET_COMMAND, stdout=PIPE, cwd=PROJECT_DIRECTORY)
    return process.stdout.decode("utf-8").strip()


def update_env_file(file) -> None:
    """Atualiza o arquivo inserindo a SECRET KEY gerada"""

    secret = get_secret_key()

    with open(file, "r+") as f:
        env_file = f.read()
        f.seek(0)

        for line in env_file.splitlines():
            if line.startswith("SECRET_KEY"):
                env_file = env_file.replace(line, f"SECRET_KEY={secret}")

        f.write(env_file)
        f.truncate()


def copy_file_env_example_to_env() -> None:
    """Método para copiar o arquivo .env.example para .env"""

    try:
        path_env_example = Path(PROJECT_DIRECTORY, ".env.example")
        path_env = Path(PROJECT_DIRECTORY, ".env")
        if not path_env.exists():
            shutil.copyfile(path_env_example, path_env)
            update_env_file(path_env)

    except Exception as e:
        print(f"{EMOJIS['error']} Erro ao copiar o arquivo .env.example para .env: {e}")
        sys.exit(1)


def remove_subdirectory_project() -> None:
    """Método para remover a subpasta do projeto"""

    try:
        source = Path.cwd()

        if sys.platform.startswith("win"):
            print(f"{EMOJIS['error']} Remova a pasta {source} manualmente")
            return

        os.chdir("..")
        shutil.rmtree(source, ignore_errors=True)

    except Exception as e:
        print(f"{EMOJIS['error']} Erro ao remover a subpasta do projeto: {e}")


def copy_all_files_to_root_dir() -> None:
    """Método responsável para copiar todos os arquivos
    da subpasta para a pasta principal"""

    try:
        print(f"{EMOJIS['success']} Copiando arquivos para a pasta principal")

        path_root = Path.cwd()
        source_dir = Path(path_root)

        for file_name in Path(source_dir).glob("*"):
            shutil.move(source_dir.joinpath(file_name), PROJECT_DIRECTORY)

    except Exception as e:
        print(f"{EMOJIS['error']} Erro ao obter o caminho do projeto: {e}")
        sys.exit(1)


def pip_install_requirements() -> bool:
    """Método para instalar as dependências do projeto"""

    try:
        print(f"{EMOJIS['wait']} Instalando as dependências do projeto")

        with Progress(
            SpinnerColumn(spinner_name="bouncingBall", speed=0.3),
            "[progress.description]{task.description}",
            BarColumn(),
            TimeRemainingColumn(),
            transient=True,
        ) as progress_bar:
            task = progress_bar.add_task(
                "Instalando as dependências do projeto",
                total=len(REQUIREMENTS),
                start=False,
            )

            for requirement in REQUIREMENTS:
                if not requirement.exists():
                    print(f"{EMOJIS['error']} O arquivo {requirement} não existe")
                    return False

                returncode = run_command(
                    f"{PYTHON} -m pip install -r {requirement}", silent=True
                )

                if returncode is False:
                    print(
                        f"{EMOJIS['error']} Erro ao instalar requirements,\
                        instale manualmente e faça o build dos apps padrões"
                    )
                    return False

                print(f"{EMOJIS['success']} {requirement} instalado com sucesso")
                progress_bar.advance(task)

        print(f"{EMOJIS['success']} Requirements instalados com sucesso")
        return True

    except Exception as e:
        print(f"{EMOJIS['error']} Erro ao instalar as dependências do projeto: {e}")
        sys.exit(1)


def build_default_apps() -> None:
    """Método para construir as apps padrões do projeto"""
    try:
        for app in DEFAULT_APPS:
            returncode = run_command(f"{PYTHON} manage.py build {app} --all")

            if returncode is False:
                print(
                    f"{EMOJIS['error']} Erro ao construir as apps padrões\
                    do projeto: {app}"
                )

    except Exception as e:
        print(f"{EMOJIS['error']} Erro ao construir as apps padrões do projeto: {e}")
        sys.exit(1)

def restore_cookiecutter_json_file_backup():
    """ Método para restaurar o arquivo cookiecutter_backup.json """
    try:
        path_root = os.getcwd()
        path_path = Path(path_root)
        path_cookiecutter_json_file = Path(f"{path_path.parent.parent}/AgtecCore/cookiecutter.json")
        path_cookiecutter_json_file_backup = Path(f"{path_path.parent}/AgtecCore/cookiecutter_backup.json")

        # Atualizando o conteúdo do arquivo cookiecutter.json com o conteúdo do arquivo cookiecutter_backup.json
        shutil.copyfile(path_cookiecutter_json_file_backup, path_cookiecutter_json_file)

        # Removendo o arquivo cookiecutter_backup.json
        os.remove(path_cookiecutter_json_file_backup)

    except OSError as os_error:
        print(f"{EMOJIS['error']} Erro ao remover o arquivo cookiecutter do projeto: {os_error}")
        sys.exit(0)
    except Exception as e:
        print(f"{EMOJIS['error']} Erro ao remover o arquivo cookiecutter do projeto: {e}")
        sys.exit(1)

copy_all_files_to_root_dir()
copy_file_env_example_to_env()

if INSTALL_REQUIREMENTS and pip_install_requirements() and BUILD_APPS:
    build_default_apps()

if GIT_INIT:
    init_git()

# restore_cookiecutter_json_file_backup()
remove_subdirectory_project()
