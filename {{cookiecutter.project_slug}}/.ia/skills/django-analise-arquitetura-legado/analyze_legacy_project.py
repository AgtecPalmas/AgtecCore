#!/usr/bin/env python3
"""Analise automatizada de arquitetura para projetos Django + PostgreSQL legados.

Gera um relatorio Markdown estruturado em `.ia/docs/reports/` contendo:

- inventario de dependencias e versoes detectadas
- extracao de `INSTALLED_APPS` do(s) arquivo(s) de settings
- catalogo de apps proprios com presenca/ausencia dos arquivos esperados
- contagem e classificacao de migrations (operacoes de risco)
- deteccao heuristica de campos sensiveis (LGPD) por nome de campo
- deteccao heuristica de N+1 em views/serializers
- configuracoes Django relevantes (DEBUG, REST_FRAMEWORK, CELERY, CACHES, MIDDLEWARE)

O relatorio gerado e **insumo factual** para o agente preencher os quatro arquivos
de `.ia/docs/architecture/`. O script nunca altera codigo do projeto analisado.

Uso tipico:

    python .ia/skills/django-analise-arquitetura-legado/analyze_legacy_project.py \\
        --project-path /caminho/do/projeto/django

Quando executado dentro do proprio projeto Django, `--project-path .` e o padrao.
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path


# ----------------------------------------------------------------------------
# Constantes e padroes
# ----------------------------------------------------------------------------

EXPECTED_APP_FILES = (
    "models.py",
    "managers.py",
    "views.py",
    "api/views",
    "serializers.py",
    "api/serializers",
    "services.py",
    "use_cases.py",
    "tasks.py",
    "urls.py",
    "api/routers.py",
    "admin.py",
    "tests",
    "migrations",
)

DEPENDENCY_FILES = (
    "pyproject.toml",
    "requirements.txt",
    "requirements/base.txt",
    "requirements/production.txt",
    "requirements/dev.txt",
    "requirements/local.txt",
    "Pipfile",
    "poetry.lock",
)

KNOWN_DEPENDENCY_TOPICS = {
    "django": "framework_web",
    "djangorestframework": "api_rest",
    "drf-spectacular": "api_rest",
    "dj-rest-auth": "autenticacao",
    "djangorestframework-simplejwt": "autenticacao",
    "django-allauth": "autenticacao",
    "celery": "tarefa_assincrona",
    "django-celery-beat": "tarefa_assincrona",
    "django-celery-results": "tarefa_assincrona",
    "redis": "cache_ou_broker",
    "django-redis": "cache_ou_broker",
    "elasticsearch": "busca_textual",
    "elasticsearch-dsl": "busca_textual",
    "django-elasticsearch-dsl": "busca_textual",
    "sentry-sdk": "observabilidade",
    "loguru": "observabilidade",
    "structlog": "observabilidade",
    "psycopg2": "driver_postgres",
    "psycopg2-binary": "driver_postgres",
    "psycopg": "driver_postgres",
    "django-cors-headers": "seguranca_cors",
    "django-environ": "configuracao_ambiente",
    "python-decouple": "configuracao_ambiente",
    "django-filter": "filtros_api",
    "django-storages": "armazenamento_externo",
    "boto3": "armazenamento_externo",
    "gunicorn": "wsgi",
    "uvicorn": "asgi",
}

THIRD_PARTY_APP_PREFIXES = (
    "django.",
    "rest_framework",
    "corsheaders",
    "allauth",
    "dj_rest_auth",
    "django_celery_beat",
    "django_celery_results",
    "django_filters",
    "drf_spectacular",
    "django_extensions",
    "storages",
)

PII_FIELD_HINTS = (
    "cpf",
    "cnpj",
    "rg",
    "passaporte",
    "telefone",
    "celular",
    "email",
    "senha",
    "password",
    "token",
    "cartao",
    "credit_card",
    "data_nascimento",
    "birth",
    "endereco",
    "logradouro",
    "cep",
    "ip_address",
)

RISKY_MIGRATION_OPS = (
    "RemoveField",
    "AlterField",
    "DeleteModel",
    "RenameModel",
    "RenameField",
    "RunSQL",
    "RunPython",
    "SeparateDatabaseAndState",
)

VIEWSET_HINT = re.compile(r"class\s+\w+\s*\(([^)]*)\)\s*:")
SELECT_RELATED_HINT = re.compile(r"select_related\(|prefetch_related\(")
QUERYSET_IN_LOOP_HINT = re.compile(r"for\s+\w+\s+in\s+[\w.]+\.objects\.")


# ----------------------------------------------------------------------------
# Dataclasses
# ----------------------------------------------------------------------------

@dataclass
class DependencyInfo:
    file: Path
    raw_name: str
    version: str | None
    topic: str


@dataclass
class AppFinding:
    name: str
    path: Path | None
    third_party: bool
    builtin: bool
    files_present: dict[str, bool] = field(default_factory=dict)
    migrations_total: int = 0
    migrations_risky: list[tuple[str, str]] = field(default_factory=list)
    pii_candidates: list[tuple[Path, int, str]] = field(default_factory=list)
    n_plus_1_candidates: list[tuple[Path, int, str]] = field(default_factory=list)


@dataclass
class SettingsFindings:
    settings_files: list[Path] = field(default_factory=list)
    installed_apps: list[str] = field(default_factory=list)
    auth_user_model: str | None = None
    debug_literal: str | None = None
    allowed_hosts_literal: str | None = None
    rest_framework: dict[str, str] = field(default_factory=dict)
    celery: dict[str, str] = field(default_factory=dict)
    caches: dict[str, str] = field(default_factory=dict)
    middleware: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


@dataclass
class AnalysisResult:
    project_path: Path
    is_django_project: bool
    dependencies: list[DependencyInfo] = field(default_factory=list)
    settings: SettingsFindings = field(default_factory=SettingsFindings)
    apps: list[AppFinding] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


# ----------------------------------------------------------------------------
# Deteccao do projeto
# ----------------------------------------------------------------------------

def detect_django_markers(project_path: Path) -> tuple[bool, list[str]]:
    markers: list[str] = []
    if (project_path / "manage.py").is_file():
        markers.append("manage.py")
    for candidate in project_path.rglob("settings.py"):
        if any(part.startswith(".") for part in candidate.parts):
            continue
        markers.append(str(candidate.relative_to(project_path)))
        break
    for candidate in project_path.rglob("settings"):
        if not candidate.is_dir():
            continue
        if any(part.startswith(".") for part in candidate.parts):
            continue
        if (candidate / "__init__.py").exists() or list(candidate.glob("*.py")):
            markers.append(str(candidate.relative_to(project_path)) + "/")
            break
    return (bool(markers), markers)


# ----------------------------------------------------------------------------
# Dependencias
# ----------------------------------------------------------------------------

def parse_pyproject_dependencies(text: str, file: Path) -> list[DependencyInfo]:
    findings: list[DependencyInfo] = []
    pattern = re.compile(
        r'^\s*"?([A-Za-z0-9_.\-]+)"?\s*[=~<>]+\s*"?([A-Za-z0-9_.\-+*<>=, ]*)"?',
        re.MULTILINE,
    )
    for match in pattern.finditer(text):
        name = match.group(1).lower()
        version = match.group(2).strip(' "') or None
        topic = KNOWN_DEPENDENCY_TOPICS.get(name)
        if topic is None:
            continue
        findings.append(DependencyInfo(file=file, raw_name=name, version=version, topic=topic))
    return findings


def parse_requirements_dependencies(text: str, file: Path) -> list[DependencyInfo]:
    findings: list[DependencyInfo] = []
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or line.startswith("-"):
            continue
        match = re.match(r"^([A-Za-z0-9_.\-]+)\s*([=~<>!]+)?\s*([A-Za-z0-9_.\-+*]*)", line)
        if not match:
            continue
        name = match.group(1).lower()
        version = match.group(3) or None
        topic = KNOWN_DEPENDENCY_TOPICS.get(name)
        if topic is None:
            continue
        findings.append(DependencyInfo(file=file, raw_name=name, version=version, topic=topic))
    return findings


def collect_dependencies(project_path: Path) -> list[DependencyInfo]:
    results: list[DependencyInfo] = []
    for relative in DEPENDENCY_FILES:
        path = project_path / relative
        if not path.is_file():
            continue
        text = read_text_safe(path)
        if path.name == "pyproject.toml":
            results.extend(parse_pyproject_dependencies(text, path))
        elif path.name.endswith(".txt") or path.name == "Pipfile":
            results.extend(parse_requirements_dependencies(text, path))
    # remove duplicatas por nome, preservando primeiro registro
    seen: set[str] = set()
    unique: list[DependencyInfo] = []
    for dep in results:
        if dep.raw_name in seen:
            continue
        seen.add(dep.raw_name)
        unique.append(dep)
    return unique


# ----------------------------------------------------------------------------
# Settings
# ----------------------------------------------------------------------------

def find_settings_files(project_path: Path) -> list[Path]:
    found: list[Path] = []
    for candidate in project_path.rglob("settings.py"):
        if any(part.startswith(".") for part in candidate.parts):
            continue
        found.append(candidate)
    for candidate in project_path.rglob("settings"):
        if not candidate.is_dir():
            continue
        if any(part.startswith(".") for part in candidate.parts):
            continue
        for sub in sorted(candidate.glob("*.py")):
            found.append(sub)
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in found:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        unique.append(path)
    return unique


def extract_list_assign(tree: ast.AST, target_name: str) -> list[str] | None:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == target_name:
                return _flatten_string_collection(node.value)
    return None


def _flatten_string_collection(value: ast.AST) -> list[str]:
    items: list[str] = []
    if isinstance(value, (ast.List, ast.Tuple)):
        for element in value.elts:
            if isinstance(element, ast.Constant) and isinstance(element.value, str):
                items.append(element.value)
    elif isinstance(value, ast.BinOp) and isinstance(value.op, ast.Add):
        items.extend(_flatten_string_collection(value.left))
        items.extend(_flatten_string_collection(value.right))
    elif isinstance(value, ast.Name):
        # nao resolve referencias a variaveis; sinaliza limitacao
        items.append(f"<referencia: {value.id}>")
    return items


def extract_string_assign(tree: ast.AST, target_name: str) -> str | None:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == target_name:
                if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                    return node.value.value
                return ast.unparse(node.value) if hasattr(ast, "unparse") else None
    return None


def extract_dict_assign(tree: ast.AST, target_name: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == target_name:
                if isinstance(node.value, ast.Dict):
                    for key, value in zip(node.value.keys, node.value.values):
                        if isinstance(key, ast.Constant):
                            result[str(key.value)] = _ast_value_to_str(value)
    return result


def _ast_value_to_str(node: ast.AST) -> str:
    if isinstance(node, ast.Constant):
        return repr(node.value)
    if hasattr(ast, "unparse"):
        try:
            return ast.unparse(node)
        except Exception:  # noqa: BLE001
            return "<expr>"
    return "<expr>"


def analyze_settings(project_path: Path) -> SettingsFindings:
    findings = SettingsFindings()
    settings_files = find_settings_files(project_path)
    findings.settings_files = [path.relative_to(project_path) for path in settings_files]

    for path in settings_files:
        text = read_text_safe(path)
        try:
            tree = ast.parse(text)
        except SyntaxError as exc:
            findings.notes.append(
                f"falha ao parsear {path.relative_to(project_path)}: {exc.msg} (linha {exc.lineno})"
            )
            continue

        installed = extract_list_assign(tree, "INSTALLED_APPS")
        if installed:
            findings.installed_apps = installed

        auth = extract_string_assign(tree, "AUTH_USER_MODEL")
        if auth:
            findings.auth_user_model = auth

        debug = extract_string_assign(tree, "DEBUG")
        if debug:
            findings.debug_literal = debug

        allowed = extract_string_assign(tree, "ALLOWED_HOSTS")
        if allowed:
            findings.allowed_hosts_literal = allowed

        rest_framework = extract_dict_assign(tree, "REST_FRAMEWORK")
        if rest_framework:
            findings.rest_framework = rest_framework

        celery_dict = extract_dict_assign(tree, "CELERY")
        if celery_dict:
            findings.celery.update({f"CELERY[{k}]": v for k, v in celery_dict.items()})
        for celery_var in ("CELERY_BROKER_URL", "CELERY_RESULT_BACKEND", "CELERY_TIMEZONE"):
            value = extract_string_assign(tree, celery_var)
            if value:
                findings.celery[celery_var] = value

        caches = extract_dict_assign(tree, "CACHES")
        if caches:
            findings.caches = caches

        middleware = extract_list_assign(tree, "MIDDLEWARE")
        if middleware:
            findings.middleware = middleware

    return findings


# ----------------------------------------------------------------------------
# Apps proprios
# ----------------------------------------------------------------------------

def is_third_party_app(label: str) -> bool:
    return any(label.startswith(prefix) for prefix in THIRD_PARTY_APP_PREFIXES)


def is_builtin_app(label: str) -> bool:
    return label.startswith("django.contrib.")


def resolve_app_path(project_path: Path, app_label: str) -> Path | None:
    parts = app_label.split(".")
    candidates: list[Path] = []
    candidates.append(project_path / "/".join(parts))
    if len(parts) > 1:
        candidates.append(project_path / "/".join(parts[:-1]))
    candidates.append(project_path / parts[-1])
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return None


def inspect_app(app_label: str, app_path: Path | None) -> dict[str, bool]:
    files_present: dict[str, bool] = {}
    if app_path is None:
        return {item: False for item in EXPECTED_APP_FILES}
    for item in EXPECTED_APP_FILES:
        target = app_path / item
        files_present[item] = target.exists()
    return files_present


def analyze_migrations(app_path: Path | None) -> tuple[int, list[tuple[str, str]]]:
    if app_path is None:
        return (0, [])
    migrations_dir = app_path / "migrations"
    if not migrations_dir.is_dir():
        return (0, [])
    total = 0
    risky: list[tuple[str, str]] = []
    for migration_file in sorted(migrations_dir.glob("*.py")):
        if migration_file.name == "__init__.py":
            continue
        total += 1
        text = read_text_safe(migration_file)
        for op in RISKY_MIGRATION_OPS:
            if op in text:
                risky.append((migration_file.name, op))
                break
    return (total, risky)


def scan_pii(app_path: Path | None) -> list[tuple[Path, int, str]]:
    if app_path is None:
        return []
    targets: list[Path] = []
    for name in ("models.py",):
        candidate = app_path / name
        if candidate.exists():
            targets.append(candidate)
    models_dir = app_path / "models"
    if models_dir.is_dir():
        targets.extend(models_dir.glob("*.py"))
    candidates: list[tuple[Path, int, str]] = []
    for file in targets:
        text = read_text_safe(file)
        for idx, line in enumerate(text.splitlines(), start=1):
            lower = line.lower()
            for hint in PII_FIELD_HINTS:
                if hint in lower and "=" in line and "models." in line:
                    candidates.append((file, idx, line.strip()))
                    break
    return candidates


def scan_n_plus_1(app_path: Path | None) -> list[tuple[Path, int, str]]:
    if app_path is None:
        return []
    targets: list[Path] = []
    for name in ("views.py", "serializers.py"):
        candidate = app_path / name
        if candidate.exists():
            targets.append(candidate)
    for sub in ("api/views", "api/serializers"):
        sub_path = app_path / sub
        if sub_path.is_dir():
            targets.extend(sub_path.rglob("*.py"))
    findings: list[tuple[Path, int, str]] = []
    for file in targets:
        text = read_text_safe(file)
        if SELECT_RELATED_HINT.search(text):
            continue
        for idx, line in enumerate(text.splitlines(), start=1):
            if QUERYSET_IN_LOOP_HINT.search(line):
                findings.append((file, idx, line.strip()))
    return findings


# ----------------------------------------------------------------------------
# Pipeline principal
# ----------------------------------------------------------------------------

def read_text_safe(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1", errors="ignore")
    except OSError:
        return ""


def analyze_project(project_path: Path) -> AnalysisResult:
    result = AnalysisResult(project_path=project_path, is_django_project=False)
    has_markers, markers = detect_django_markers(project_path)
    result.is_django_project = has_markers
    if not has_markers:
        result.warnings.append(
            "Nenhum marcador Django encontrado (manage.py ou settings). "
            "O projeto pode nao ser Django ou a estrutura nao foi reconhecida."
        )
        return result

    result.dependencies = collect_dependencies(project_path)
    result.settings = analyze_settings(project_path)

    apps_seen: set[str] = set()
    for label in result.settings.installed_apps:
        if label in apps_seen:
            continue
        apps_seen.add(label)
        third_party = is_third_party_app(label)
        builtin = is_builtin_app(label)
        path = None if builtin else resolve_app_path(project_path, label)
        finding = AppFinding(
            name=label,
            path=path,
            third_party=third_party and not builtin,
            builtin=builtin,
        )
        if not builtin:
            finding.files_present = inspect_app(label, path)
            finding.migrations_total, finding.migrations_risky = analyze_migrations(path)
            finding.pii_candidates = scan_pii(path)
            finding.n_plus_1_candidates = scan_n_plus_1(path)
        result.apps.append(finding)

    return result


# ----------------------------------------------------------------------------
# Geracao do relatorio
# ----------------------------------------------------------------------------

def relative_or_str(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def render_report(result: AnalysisResult) -> str:
    today = date.today().isoformat()
    lines: list[str] = []
    lines.append(f"# Relatorio de Analise Arquitetural - Projeto Django Legado")
    lines.append("")
    lines.append(f"- Data de geracao: `{today}`")
    lines.append(f"- Projeto analisado: `{result.project_path.name}`")
    lines.append(f"- Marcadores Django detectados: `{result.is_django_project}`")
    lines.append("")
    lines.append("> Este relatorio e gerado pelo script ")
    lines.append("> `.ia/skills/django-analise-arquitetura-legado/analyze_legacy_project.py`.")
    lines.append("> Ele e **insumo factual** para o preenchimento dos quatro arquivos de ")
    lines.append("> `.ia/docs/architecture/`. Todo julgamento arquitetural continua sendo do agente humano ou de IA.")
    lines.append("")

    if not result.is_django_project:
        lines.append("## Bloqueio")
        lines.append("")
        for warning in result.warnings:
            lines.append(f"- {warning}")
        lines.append("")
        return "\n".join(lines)

    lines.append("## 1. Dependencias detectadas")
    lines.append("")
    if not result.dependencies:
        lines.append("Nenhuma dependencia conhecida foi reconhecida. Verificar arquivos de dependencias manualmente.")
    else:
        lines.append("| Pacote | Versao declarada | Topico | Arquivo |")
        lines.append("|---|---|---|---|")
        for dep in result.dependencies:
            version = dep.version or "n/d"
            file = relative_or_str(dep.file, result.project_path)
            lines.append(f"| `{dep.raw_name}` | `{version}` | {dep.topic} | `{file}` |")
    lines.append("")

    lines.append("## 2. Configuracoes Django")
    lines.append("")
    settings = result.settings
    if settings.settings_files:
        lines.append("Arquivos de settings encontrados:")
        for file in settings.settings_files:
            lines.append(f"- `{file}`")
    else:
        lines.append("Nenhum arquivo de settings localizado.")
    lines.append("")
    lines.append(f"- `AUTH_USER_MODEL`: `{settings.auth_user_model or 'nao declarado (usa default)'}`")
    lines.append(f"- `DEBUG`: `{settings.debug_literal or 'nao detectado por leitura estatica'}`")
    lines.append(f"- `ALLOWED_HOSTS`: `{settings.allowed_hosts_literal or 'nao detectado por leitura estatica'}`")
    lines.append("")
    if settings.rest_framework:
        lines.append("### REST_FRAMEWORK")
        lines.append("")
        lines.append("| Chave | Valor |")
        lines.append("|---|---|")
        for key, value in settings.rest_framework.items():
            lines.append(f"| `{key}` | `{value}` |")
        lines.append("")
    if settings.celery:
        lines.append("### Celery")
        lines.append("")
        lines.append("| Chave | Valor |")
        lines.append("|---|---|")
        for key, value in settings.celery.items():
            lines.append(f"| `{key}` | `{value}` |")
        lines.append("")
    if settings.caches:
        lines.append("### CACHES")
        lines.append("")
        lines.append("| Chave | Valor |")
        lines.append("|---|---|")
        for key, value in settings.caches.items():
            lines.append(f"| `{key}` | `{value}` |")
        lines.append("")
    if settings.middleware:
        lines.append("### MIDDLEWARE")
        lines.append("")
        for item in settings.middleware:
            lines.append(f"- `{item}`")
        lines.append("")
    if settings.notes:
        lines.append("### Observacoes sobre settings")
        lines.append("")
        for note in settings.notes:
            lines.append(f"- {note}")
        lines.append("")

    lines.append("## 3. Catalogo de apps")
    lines.append("")
    own_apps = [app for app in result.apps if not app.builtin and not app.third_party]
    third_party_apps = [app for app in result.apps if app.third_party]
    builtin_apps = [app for app in result.apps if app.builtin]

    lines.append(f"- Apps proprios identificados: `{len(own_apps)}`")
    lines.append(f"- Apps de terceiros reconhecidos: `{len(third_party_apps)}`")
    lines.append(f"- Apps built-in Django: `{len(builtin_apps)}`")
    lines.append("")

    if own_apps:
        lines.append("### Apps proprios - inventario por arquivo")
        lines.append("")
        header = ["App"] + list(EXPECTED_APP_FILES)
        lines.append("| " + " | ".join(header) + " |")
        lines.append("|" + "|".join(["---"] * len(header)) + "|")
        for app in own_apps:
            row = [f"`{app.name}`"]
            for item in EXPECTED_APP_FILES:
                present = app.files_present.get(item, False)
                row.append("OK" if present else "-")
            lines.append("| " + " | ".join(row) + " |")
        lines.append("")

    if third_party_apps:
        lines.append("### Apps de terceiros declarados")
        lines.append("")
        for app in third_party_apps:
            lines.append(f"- `{app.name}`")
        lines.append("")

    lines.append("## 4. Migrations")
    lines.append("")
    risky_total = 0
    rows: list[str] = []
    for app in own_apps:
        if app.migrations_total == 0 and not app.migrations_risky:
            continue
        rows.append(
            f"| `{app.name}` | {app.migrations_total} | {len(app.migrations_risky)} |"
        )
        risky_total += len(app.migrations_risky)
    if rows:
        lines.append("| App | Total | Migrations com operacao de risco |")
        lines.append("|---|---|---|")
        lines.extend(rows)
    else:
        lines.append("Nenhuma migration identificada nos apps proprios.")
    lines.append("")

    if risky_total:
        lines.append("### Detalhe das migrations de risco")
        lines.append("")
        for app in own_apps:
            for migration_name, op in app.migrations_risky:
                lines.append(f"- `{app.name}` / `{migration_name}` -> `{op}`")
        lines.append("")

    lines.append("## 5. Campos candidatos a LGPD")
    lines.append("")
    pii_any = False
    for app in own_apps:
        if not app.pii_candidates:
            continue
        pii_any = True
        lines.append(f"### `{app.name}`")
        lines.append("")
        for file, line_no, snippet in app.pii_candidates:
            relative = relative_or_str(file, result.project_path)
            lines.append(f"- `{relative}:{line_no}` -> `{snippet[:120]}`")
        lines.append("")
    if not pii_any:
        lines.append("Nenhum campo candidato a LGPD detectado por heuristica de nome.")
        lines.append("Conferencia manual recomendada nos models.")
        lines.append("")

    lines.append("## 6. Candidatos a N+1")
    lines.append("")
    n1_any = False
    for app in own_apps:
        if not app.n_plus_1_candidates:
            continue
        n1_any = True
        lines.append(f"### `{app.name}`")
        lines.append("")
        for file, line_no, snippet in app.n_plus_1_candidates:
            relative = relative_or_str(file, result.project_path)
            lines.append(f"- `{relative}:{line_no}` -> `{snippet[:120]}`")
        lines.append("")
    if not n1_any:
        lines.append("Nenhum candidato a N+1 detectado pela heuristica.")
        lines.append("Heuristica e conservadora; revisao manual continua necessaria em views e serializers.")
        lines.append("")

    lines.append("## 7. Avisos e limitacoes do script")
    lines.append("")
    if result.warnings:
        for warning in result.warnings:
            lines.append(f"- {warning}")
    lines.append("- A deteccao de `INSTALLED_APPS` por AST nao resolve concatenacoes via variaveis externas; verificar `<referencia: NOME>` na lista.")
    lines.append("- Heuristicas de LGPD usam nome de campo; campos genericos com PII podem nao ser detectados.")
    lines.append("- Heuristicas de N+1 ignoram arquivos com `select_related`/`prefetch_related` em qualquer parte.")
    lines.append("- O script nao executa o projeto; configuracoes calculadas em tempo de execucao nao sao visiveis.")
    lines.append("")

    lines.append("## 8. Proximos passos para o agente")
    lines.append("")
    lines.append("1. Revisar este relatorio inteiro.")
    lines.append("2. Preencher `.ia/docs/architecture/overview.md` com stack e objetivos confirmados.")
    lines.append("3. Preencher `.ia/docs/architecture/system-architecture.md` com catalogo de apps e fluxos.")
    lines.append("4. Atualizar `.ia/docs/architecture/modules.md` com desvios reais por app.")
    lines.append("5. Atualizar `.ia/docs/architecture/security.md` com mecanismos confirmados de autenticacao, dados sensiveis e riscos.")
    lines.append("6. Abrir task de analise em `.ia/docs/tasks/` registrando premissas e itens nao confirmaveis sem execucao do projeto.")
    lines.append("")

    return "\n".join(lines)


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Coleta evidencias estaticas de um projeto Django legado e gera relatorio Markdown.",
    )
    parser.add_argument(
        "--project-path",
        default=".",
        help="Caminho do projeto Django alvo. Padrao: diretorio atual.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Caminho do relatorio Markdown gerado. Padrao: .ia/docs/reports/<data>-relatorio-analise-arquitetura.md no diretorio atual.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Apenas detecta o projeto Django sem gerar relatorio.",
    )
    parser.add_argument(
        "--print",
        dest="print_report",
        action="store_true",
        help="Imprime o relatorio em stdout em vez de gravar em arquivo.",
    )
    return parser.parse_args(argv)


def resolve_output_path(custom_output: str | None) -> Path:
    if custom_output:
        return Path(custom_output).expanduser().resolve()
    today = date.today().isoformat()
    default = Path.cwd() / ".ia" / "docs" / "reports" / f"{today}-relatorio-analise-arquitetura.md"
    return default


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    project_path = Path(args.project_path).expanduser().resolve()
    if not project_path.is_dir():
        print(f"Erro: caminho do projeto nao e diretorio: {project_path}", file=sys.stderr)
        return 2

    if args.dry_run:
        has_markers, markers = detect_django_markers(project_path)
        if has_markers:
            print(f"OK: projeto Django detectado em {project_path}")
            for marker in markers:
                print(f"  - marcador: {marker}")
            return 0
        print(f"Aviso: nenhum marcador Django encontrado em {project_path}", file=sys.stderr)
        return 1

    result = analyze_project(project_path)
    report = render_report(result)

    if args.print_report:
        print(report)
        return 0 if result.is_django_project else 1

    output_path = resolve_output_path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Relatorio gerado em: {output_path}")
    return 0 if result.is_django_project else 1


if __name__ == "__main__":
    raise SystemExit(main())
