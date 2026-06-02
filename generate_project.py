#!/usr/bin/env python3
"""AgtecCore project generator — substitui o CookieCutter."""
from __future__ import annotations

import argparse
import os
import re
import secrets
import shutil
import subprocess
import sys
from datetime import datetime
from fnmatch import fnmatch
from pathlib import Path
from types import SimpleNamespace
from typing import Any

try:
    import jinja2
except ImportError:
    sys.exit("Jinja2 não encontrado. Ative o virtualenv do projeto antes de executar.")

# ─── Constantes ───────────────────────────────────────────────────────────────

TEMPLATE_DIR = Path(__file__).parent / "{{cookiecutter.project_slug}}"

COPY_WITHOUT_RENDER: list[str] = [
    "core/**",
    "usuario/**",
    "atendimento/**",
    "configuracao_core/**",
    "scanapi_exemplo.yaml",
    "docs/**",
    "contrib/**",
    ".coveragerc",
    ".prospector.yaml",
]

DEFAULT_APPS = ["usuario", "configuracao_core"]

PYTHON = "py" if sys.platform.startswith("win") else "python"

OK = "✅"
ERR = "❌"
WAIT = "⏳"


# ─── Contexto ─────────────────────────────────────────────────────────────────

def _slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[-\s]+", "-", value)
    return value.strip("-")


def _build_context(args: argparse.Namespace) -> dict[str, Any]:
    """Coleta interativa de inputs com defaults do argparse."""

    def ask(prompt: str, default: str = "") -> str:
        display = f" [{default}]" if default else ""
        value = input(f"  {prompt}{display}: ").strip()
        return value or default

    print("\n── AgtecCore — Novo Projeto ─────────────────────────────────")

    project_name = args.project_name or ask("Nome do projeto", "Projeto Base")
    project_slug = _slugify(project_name).replace("-", "_")

    client_name = args.client_name or ask("Nome do cliente", "Nome do Cliente")
    description = args.description or ask("Descrição", "Projeto base para os novos projetos")
    author_name = args.author_name or ask("Nome do autor", "Informe seu nome")
    domain_name = args.domain_name or ask("Domínio", "palmas.to.gov.br")
    email = args.email or ask("E-mail", "agtec@palmas.to.gov.br")
    flutter_org = args.flutter_org or ask("Flutter organization name", "Agtec")
    docker_port = args.docker_port or ask("Porta Docker", "8000")
    postgre_port = args.postgre_port or ask("Porta PostgreSQL", "5432")

    flutter_org_domain = ".".join(reversed(domain_name.split(".")))

    return {
        "project_name": project_name,
        "project_slug": project_slug,
        "main_app": project_slug,
        "client_name": client_name,
        "docker_port": docker_port,
        "postgre_port": postgre_port,
        "created_date_project": datetime.now().strftime("%d/%m/%Y"),
        "description": description,
        "author_name": author_name,
        "domain_name": domain_name,
        "email": email,
        "flutter_organization_name": flutter_org,
        "flutter_organization_domain": flutter_org_domain,
        "django_version": "5.2.12",
        "python_version": "3.12.*",
        "postgresql_version": "14.2",
        "drf_version": "3.16.1",
    }


# ─── Renderização ─────────────────────────────────────────────────────────────

_JINJA_ENV = jinja2.Environment(
    undefined=jinja2.Undefined,
    keep_trailing_newline=True,
    autoescape=False,
)


def _render(content: str, jinja_ctx: dict) -> str:
    try:
        return _JINJA_ENV.from_string(content).render(jinja_ctx)
    except (jinja2.TemplateSyntaxError, jinja2.UndefinedError):
        return content


def _should_skip_render(rel_path: str) -> bool:
    for pattern in COPY_WITHOUT_RENDER:
        if pattern.endswith("/**"):
            prefix = pattern[:-3]
            if rel_path == prefix or rel_path.startswith(prefix + os.sep) or rel_path.startswith(prefix + "/"):
                return True
        elif fnmatch(rel_path, pattern) or fnmatch(Path(rel_path).name, pattern):
            return True
    return False


# ─── Scaffold ─────────────────────────────────────────────────────────────────

def scaffold_project(ctx: dict, dest: Path) -> None:
    """Copia e renderiza o template para o diretório destino."""
    if dest.exists():
        sys.exit(f"{ERR} Destino já existe: {dest}")

    jinja_ctx = {"cookiecutter": SimpleNamespace(**ctx)}

    total = sum(1 for _ in TEMPLATE_DIR.rglob("*") if _.is_file())
    copied = 0

    for src_file in TEMPLATE_DIR.rglob("*"):
        if not src_file.is_file():
            continue

        rel = src_file.relative_to(TEMPLATE_DIR)
        dst_file = dest / rel
        dst_file.parent.mkdir(parents=True, exist_ok=True)

        skip_render = _should_skip_render(str(rel))

        try:
            raw = src_file.read_bytes()
            text = raw.decode("utf-8")
            is_binary = False
        except UnicodeDecodeError:
            is_binary = True

        if is_binary or skip_render or "cookiecutter" not in (text if not is_binary else ""):
            shutil.copy2(src_file, dst_file)
        else:
            rendered = _render(text, jinja_ctx)
            dst_file.write_text(rendered, encoding="utf-8")

        copied += 1
        if copied % 50 == 0 or copied == total:
            print(f"  {WAIT} {copied}/{total} arquivos processados...", end="\r")

    print(f"  {OK} {total} arquivos copiados.             ")


# ─── Pós-geração ──────────────────────────────────────────────────────────────

def _run(cmd: str | list[str], cwd: Path, silent: bool = False) -> bool:
    """Executa comando e retorna True se bem-sucedido."""
    kwargs: dict = {"cwd": cwd}
    if silent:
        kwargs["stdout"] = subprocess.DEVNULL
        kwargs["stderr"] = subprocess.DEVNULL

    if isinstance(cmd, str):
        cmd = cmd.split()

    try:
        result = subprocess.run(cmd, **kwargs)
        return result.returncode == 0
    except Exception as exc:
        print(f"  {ERR} {exc}")
        return False


def _generate_secret_key() -> str:
    return secrets.token_urlsafe(50)


def setup_env_file(dest: Path) -> None:
    env_example = dest / ".env.example"
    env_file = dest / ".env"

    if not env_example.exists():
        print(f"  {ERR} .env.example não encontrado — .env não criado")
        return

    if env_file.exists():
        print(f"  {OK} .env já existe — mantendo")
        return

    secret = _generate_secret_key()
    content = env_example.read_text(encoding="utf-8")
    lines = []
    for line in content.splitlines():
        if line.startswith("SECRET_KEY="):
            lines.append(f"SECRET_KEY={secret}")
        else:
            lines.append(line)
    env_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  {OK} .env criado com SECRET_KEY gerada")


def install_dependencies(dest: Path) -> bool:
    print(f"  {WAIT} Instalando dependências via uv sync...")
    ok = _run(["uv", "sync", "--all-extras"], cwd=dest, silent=True)
    if ok:
        print(f"  {OK} Dependências instaladas")
    else:
        print(f"  {ERR} Falha no uv sync — instale manualmente")
    return ok


def build_default_apps(dest: Path) -> None:
    for app in DEFAULT_APPS:
        print(f"  {WAIT} Construindo app: {app}")
        ok = _run([PYTHON, "manage.py", "build", app, "--all"], cwd=dest)
        if not ok:
            print(f"  {ERR} Falha ao construir {app} — execute manualmente")


def init_git(dest: Path) -> None:
    print(f"  {WAIT} Inicializando git...")
    cmds = [
        "git init --initial-branch=master",
        "git add .",
        'git commit -am "Primeiro Commit"',
        "git checkout -b desenvolvimento",
    ]
    for cmd in cmds:
        ok = _run(cmd, cwd=dest, silent=True)
        status = OK if ok else ERR
        print(f"  {status} {cmd}")


# ─── CLI ──────────────────────────────────────────────────────────────────────

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera um novo projeto Django baseado no AgtecCore.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--project-name", dest="project_name", default="")
    parser.add_argument("--client-name", dest="client_name", default="")
    parser.add_argument("--description", dest="description", default="")
    parser.add_argument("--author-name", dest="author_name", default="")
    parser.add_argument("--domain-name", dest="domain_name", default="")
    parser.add_argument("--email", dest="email", default="")
    parser.add_argument("--flutter-org", dest="flutter_org", default="")
    parser.add_argument("--docker-port", dest="docker_port", default="")
    parser.add_argument("--postgre-port", dest="postgre_port", default="")
    parser.add_argument("--no-install", action="store_true", help="Não instalar dependências")
    parser.add_argument("--no-git", action="store_true", help="Não inicializar git")
    parser.add_argument("--no-build-apps", action="store_true", help="Não construir apps padrão")
    return parser.parse_args()


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    if not TEMPLATE_DIR.exists():
        sys.exit(f"{ERR} Template não encontrado: {TEMPLATE_DIR}\nExecute a partir da raiz do AgtecCore.")

    args = _parse_args()
    ctx = _build_context(args)

    project_slug = ctx["project_slug"]
    dest_base = Path(__file__).parent.parent
    dest = dest_base / project_slug

    print(f"\n  Projeto : {ctx['project_name']}")
    print(f"  Slug    : {project_slug}")
    print(f"  Destino : {dest}")
    confirm = input("\n  Confirmar geração? [S/n]: ").strip().lower()
    if confirm and confirm not in ("s", "sim", "y", "yes"):
        print("Abortado.")
        return

    print(f"\n── Copiando template ────────────────────────────────────────")
    scaffold_project(ctx, dest)

    print(f"\n── Pós-geração ──────────────────────────────────────────────")
    setup_env_file(dest)

    if not args.no_install:
        deps_ok = install_dependencies(dest)
        if deps_ok and not args.no_build_apps:
            build_default_apps(dest)
    else:
        print(f"  ⏭  Instalação de dependências ignorada (--no-install)")

    if not args.no_git:
        init_git(dest)
    else:
        print(f"  ⏭  Git ignorado (--no-git)")

    print(f"\n{OK} Projeto '{project_slug}' gerado em: {dest}")
    print(f"   Próximos passos:")
    print(f"   1. cd {dest}")
    print(f"   2. source .venv/bin/activate")
    print(f"   3. Ajuste o .env com as credenciais do banco")
    print(f"   4. python manage.py migrate\n")


if __name__ == "__main__":
    main()
