#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import os
import re
import shutil
from pathlib import Path

import tomllib


def read_setting(setting_name: str, project_path: Path) -> str:
    value = os.getenv(setting_name, "").strip()
    if value:
        return value

    env_file = project_path / ".env"
    if not env_file.exists():
        return ""

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, raw_value = line.split("=", 1)
        if key.strip() != setting_name:
            continue
        return raw_value.strip().strip('"').strip("'")

    return ""


def get_default_devbrain_vault(project_path: Path) -> str:
    vault = read_setting("OBSIDIAN_DEV_VAULT", project_path)
    if vault:
        return vault

    legacy_vault = read_setting("DEVBRAIN_VAULT", project_path)
    if legacy_vault:
        return legacy_vault

    raise ValueError(
        "Configure OBSIDIAN_DEV_VAULT no arquivo .env ou informe --vault explicitamente."
    )


def get_default_system_name(project_path: Path) -> str:
    system_name = read_setting("OBSIDIAN_DEV_SYSTEM_NAME", project_path)
    if system_name:
        return system_name

    legacy_system_name = read_setting("DEVBRAIN_SYSTEM_NAME", project_path)
    if legacy_system_name:
        return legacy_system_name

    return normalize_system_name(project_path.resolve().name)


def normalize_system_name(raw_name: str) -> str:
    normalized = " ".join(raw_name.replace("-", " ").replace("_", " ").split())
    if not normalized:
        normalized = "Projeto"

    words = [word.capitalize() for word in normalized.split()]
    if not words or words[-1].lower() != "django":
        words.append("Django")

    return " ".join(words)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Exporta o contexto operacional do projeto para o vault DevBrain."
    )
    parser.add_argument(
        "--vault",
        default=None,
        help="Caminho raiz do vault DevBrain.",
    )
    parser.add_argument(
        "--project-path",
        default=os.getcwd(),
        help="Caminho do repositório a ser analisado.",
    )
    parser.add_argument(
        "--system-name",
        default=None,
        help="Nome do sistema dentro do vault. Por padrão usa o nome da pasta.",
    )
    args = parser.parse_args()
    project_path = Path(args.project_path).resolve()
    if args.vault is None:
        args.vault = get_default_devbrain_vault(project_path)
    if args.system_name is None:
        args.system_name = get_default_system_name(project_path)
    return args


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_note(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def load_pyproject(path: Path) -> dict:
    if not path.exists():
        return {}
    return tomllib.loads(path.read_text(encoding="utf-8"))


def parse_python_source(path: Path) -> ast.AST | None:
    if not path.exists():
        return None
    try:
        return ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError:
        return None


def clean_markdown_text(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[[^\]]+\]\([^)]+\)", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[#*_`>-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def summarize_readme(readme_text: str) -> tuple[str, str]:
    lines = [line.strip() for line in readme_text.splitlines() if line.strip()]
    title = "Projeto"
    for line in lines:
        if line.startswith("#"):
            title = clean_markdown_text(line)
            break

    fragments: list[str] = []
    for line in lines:
        if line.startswith("#") or line.startswith("[") or line.startswith("```"):
            continue
        fragments.append(line)
        summary = clean_markdown_text(" ".join(fragments))
        if len(summary) > 260:
            return title, summary[:260]

    return title, clean_markdown_text(" ".join(fragments))[:260]


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- Nenhum item identificado."


def extract_string_list(tree: ast.AST | None, variable_name: str) -> list[str]:
    if tree is None or not isinstance(tree, ast.Module):
        return []
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == variable_name:
                if isinstance(node.value, (ast.List, ast.Tuple)):
                    values: list[str] = []
                    for item in node.value.elts:
                        if isinstance(item, ast.Constant) and isinstance(item.value, str):
                            values.append(item.value)
                    return values
    return []


def collect_local_apps(repo_path: Path, installed_apps: list[str]) -> list[str]:
    apps: list[str] = []
    ignored_prefixes = (
        "django.",
        "rest_framework",
        "dj_rest_auth",
        "drf_spectacular",
        "tempus_dominus",
        "debug_toolbar",
    )
    for app_name in installed_apps:
        root_name = app_name.split(".")[0]
        if app_name.startswith(ignored_prefixes):
            continue
        if (repo_path / root_name).is_dir() and root_name not in apps:
            apps.append(root_name)
    return apps


def collect_taskipy_tasks(pyproject: dict) -> dict[str, str]:
    return pyproject.get("tool", {}).get("taskipy", {}).get("tasks", {})


def collect_ia_docs(repo_path: Path, max_items: int = 12) -> list[str]:
    docs_root = repo_path / ".ia" / "docs"
    if not docs_root.exists():
        return []
    items: list[str] = []
    for path in sorted(docs_root.rglob("*.md")):
        items.append(f"`{path.relative_to(repo_path)}`")
        if len(items) >= max_items:
            break
    return items


def collect_root_integrations(urls_text: str, local_apps: list[str]) -> list[str]:
    findings: list[str] = []
    if "swagger" in urls_text.lower():
        findings.append("documentação de API via Swagger/Redoc")
    if "TokenObtainPairView" in urls_text:
        findings.append("autenticação JWT")
    if "dj_rest_auth.urls" in urls_text:
        findings.append("autenticação via dj-rest-auth")
    if "django_ckeditor_5.urls" in urls_text:
        findings.append("edição rica com CKEditor 5")
    if "hotsite_evento" in local_apps:
        findings.append("hotsite de eventos")
    if "website" in local_apps:
        findings.append("website público")
    return findings


def sync_markdown_tree(source_dir: Path, target_dir: Path) -> int:
    if not source_dir.exists():
        if target_dir.exists():
            shutil.rmtree(target_dir)
        return 0

    target_dir.mkdir(parents=True, exist_ok=True)
    copied = 0
    expected_files: set[Path] = set()

    for source_file in sorted(source_dir.rglob("*.md")):
        relative_path = source_file.relative_to(source_dir)
        target_file = target_dir / relative_path
        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target_file)
        expected_files.add(target_file.resolve())
        copied += 1

    for existing_file in sorted(target_dir.rglob("*.md")):
        if existing_file.resolve() not in expected_files:
            existing_file.unlink()

    for existing_dir in sorted(
        [path for path in target_dir.rglob("*") if path.is_dir()],
        key=lambda item: len(item.parts),
        reverse=True,
    ):
        if not any(existing_dir.iterdir()):
            existing_dir.rmdir()

    return copied


def collect_markdown_links(base_dir: Path) -> list[str]:
    if not base_dir.exists():
        return []
    links: list[str] = []
    for path in sorted(base_dir.rglob("*.md")):
        if path.name.startswith("00-Index"):
            continue
        relative_path = path.relative_to(base_dir)
        label = str(relative_path.with_suffix(""))
        links.append(f"[{label}]({relative_path.as_posix()})")
    return links


def main() -> int:
    args = parse_args()

    repo_path = Path(args.project_path).resolve()
    vault_path = Path(args.vault).resolve()
    system_name = normalize_system_name(args.system_name)
    system_dir = vault_path / "01-Sistemas" / system_name

    readme_text = read_text(repo_path / "README.md")
    root_title, readme_summary = summarize_readme(readme_text)
    pyproject = load_pyproject(repo_path / "pyproject.toml")
    settings_tree = parse_python_source(repo_path / "base" / "settings.py")
    urls_text = read_text(repo_path / "base" / "urls.py")

    installed_apps = extract_string_list(settings_tree, "INSTALLED_APPS")
    fastapi_apps = extract_string_list(settings_tree, "FASTAPI_APPS")
    doc_apps = extract_string_list(settings_tree, "DOC_APPS")
    ignored_apps = extract_string_list(settings_tree, "IGNORED_APPS")
    local_apps = collect_local_apps(repo_path, installed_apps)
    taskipy_tasks = collect_taskipy_tasks(pyproject)
    ia_docs = collect_ia_docs(repo_path)
    integrations = collect_root_integrations(urls_text, local_apps)
    specs_count = sync_markdown_tree(
        repo_path / ".ia" / "docs" / "specs",
        system_dir / "specs",
    )
    tasks_todo_count = sync_markdown_tree(
        repo_path / ".ia" / "docs" / "tasks" / "todo",
        system_dir / "tasks" / "todo",
    )
    tasks_done_count = sync_markdown_tree(
        repo_path / ".ia" / "docs" / "tasks" / "done",
        system_dir / "tasks" / "done",
    )

    python_version = pyproject.get("project", {}).get("requires-python", "não definido")
    stack = [
        "`Django 4.2`",
        f"`Python {python_version}`",
        "`PostgreSQL`",
        "`Docker`",
        "`DRF`",
        "`Taskipy`",
        "`Pytest`",
    ]

    write_note(
        system_dir / "00-Visao-Geral.md",
        f"""
# {system_name}

## Objetivo
{readme_summary or "Resumo não encontrado no README."}

## Nome raiz identificado
`{root_title}`

## Repositório
`{repo_path}`

## Stack principal
{bullet_list(stack)}

## Apps locais detectadas
{bullet_list([f"`{app}`" for app in local_apps])}

## Apps expostas em FASTAPI_APPS
{bullet_list([f"`{app}`" for app in fastapi_apps])}

## Apps ignoradas no menu
{bullet_list([f"`{app}`" for app in ignored_apps])}
""",
    )

    write_note(
        system_dir / "03-Runbooks.md",
        f"""
# Runbooks - {system_name}

## Subir localmente
{bullet_list([
    "`python manage.py migrate`",
    "`python manage.py runserver`",
    "`task run`",
])}

## Qualidade e testes
{bullet_list([
    "`task lint`",
    "`task test`",
    "`pytest -s -x --cov=AgtecCore -vv`",
])}

## Comandos operacionais identificados
{bullet_list([f"`task {name}`: `{command}`" for name, command in sorted(taskipy_tasks.items())])}

## Referências internas úteis
{bullet_list([
    "`README.md`",
    "`pyproject.toml`",
    "`base/settings.py`",
    "`base/urls.py`",
    "`.ia/skills/obsidian-sync/export_devbrain.py`",
])}
""",
    )

    write_note(
        system_dir / "08-Agentes.md",
        f"""
# Agentes - {system_name}

## O que os agentes podem fazer
{bullet_list([
    "ler o repositório e consolidar contexto técnico no vault",
    "atualizar `03-Runbooks.md`, `04-Incidentes.md` e `06-Debugging.md`",
    "processar material bruto em `raw/` e propor notas permanentes",
    "usar `.ia/skills/obsidian-sync/export_devbrain.py` para sincronizar visão operacional",
])}

## O que exige cuidado
{bullet_list([
    "não reescrever integralmente `01-Arquitetura.md` sem revisão humana",
    "não apagar histórico operacional automaticamente",
    "não mover a estrutura de apps sem tarefa explícita",
    "não alterar `.env` ou segredos ao documentar o sistema",
])}

## Fontes de verdade do projeto
{bullet_list([
    "`README.md`",
    "`base/settings.py`",
    "`base/urls.py`",
    "`pyproject.toml`",
    "arquivos em `.ia/docs/`",
])}

## Documentação assistida por IA já existente
{bullet_list(ia_docs)}
""",
    )

    write_note(
        system_dir / "09-Integracoes.md",
        f"""
# Integracoes - {system_name}

## Integracoes identificadas
{bullet_list(integrations)}

## Sinais estruturais relevantes
{bullet_list([
    "área administrativa em `/core/`",
    "rotas públicas de website na raiz",
    "rotas públicas de eventos em `/evento/`",
    "documentação OpenAPI em `/swagger/`, `/swagger-ui/` e `/redoc/`",
])}

## Apps com documentação formal em DOC_APPS
{bullet_list([f"`{app}`" for app in doc_apps])}

## Próximos mapeamentos recomendados
{bullet_list([
    "inventariar dependências externas por app",
    "mapear integrações entre `assinatura_documento`, `website` e `hotsite_evento`",
    "registrar jobs, webhooks e fluxos de autenticação",
])}
""",
    )

    write_note(
        system_dir / "10-Especificacoes-e-Tasks.md",
        f"""
# Especificacoes e Tasks - {system_name}

## Espelhamento sincronizado da pasta `.ia/docs`

### Especificacoes tecnicas
- Origem: `{repo_path / ".ia" / "docs" / "specs"}`
- Destino: `specs/`
- Arquivos sincronizados: `{specs_count}`

### Tasks abertas
- Origem: `{repo_path / ".ia" / "docs" / "tasks" / "todo"}`
- Destino: `tasks/todo/`
- Arquivos sincronizados: `{tasks_todo_count}`

### Tasks concluidas
- Origem: `{repo_path / ".ia" / "docs" / "tasks" / "done"}`
- Destino: `tasks/done/`
- Arquivos sincronizados: `{tasks_done_count}`

## Regra de uso
- `specs/` preserva as especificações técnicas do projeto dentro do cérebro.
- `tasks/todo/` preserva o trabalho em andamento.
- `tasks/done/` preserva o histórico operacional e técnico.
""",
    )

    write_note(
        system_dir / "specs" / "00-Index.md",
        f"""
# Index - Specs - {system_name}

## Especificacoes tecnicas sincronizadas
{bullet_list(collect_markdown_links(system_dir / "specs"))}
""",
    )

    write_note(
        system_dir / "tasks" / "todo" / "00-Index.md",
        f"""
# Index - Tasks Todo - {system_name}

## Tasks abertas sincronizadas
{bullet_list(collect_markdown_links(system_dir / "tasks" / "todo"))}
""",
    )

    write_note(
        system_dir / "tasks" / "done" / "00-Index.md",
        f"""
# Index - Tasks Done - {system_name}

## Tasks concluidas sincronizadas
{bullet_list(collect_markdown_links(system_dir / "tasks" / "done"))}
""",
    )

    write_note(
        system_dir / "00-Index.md",
        f"""
# Index - {system_name}

## Navegacao principal
- [Visao Geral](00-Visao-Geral.md)
- [Runbooks](03-Runbooks.md)
- [Agentes](08-Agentes.md)
- [Integracoes](09-Integracoes.md)
- [Especificacoes e Tasks](10-Especificacoes-e-Tasks.md)

## Navegacao por acervo sincronizado
- [Index de Specs](specs/00-Index.md)
- [Index de Tasks Todo](tasks/todo/00-Index.md)
- [Index de Tasks Done](tasks/done/00-Index.md)

## Contadores rapidos
- Specs sincronizadas: `{specs_count}`
- Tasks abertas sincronizadas: `{tasks_todo_count}`
- Tasks concluidas sincronizadas: `{tasks_done_count}`
""",
    )

    for dirname in ("raw", "logs", "anexos"):
        (system_dir / dirname).mkdir(parents=True, exist_ok=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
