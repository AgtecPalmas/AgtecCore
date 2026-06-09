#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ALLOWED_DONE_STATUS = "done"
PLACEHOLDER_PATTERNS = (
    re.compile(r"_\[[^\n]+\]_"),
    re.compile(r"^\| \.\.\. \|.*$", re.MULTILINE),
    re.compile(r"Preencher ao concluir a demanda\."),
)
PLACEHOLDER_DOC_GLOBS = (
    "AGENTS.md",
    ".ia/README.md",
    ".ia/docs/architecture/*.md",
    ".ia/docs/guides/*.md",
    ".ia/docs/reports/*.md",
    ".ia/skills/*/SKILL.md",
)
CURRENT_DOC_GLOBS = (
    "AGENTS.md",
    ".ia/README.md",
    ".ia/docs/architecture/*.md",
    ".ia/docs/guides/*.md",
    ".ia/docs/templates/*.md",
    ".ia/docs/reports/*.md",
    ".ia/docs/tasks/todo/*.md",
    ".ia/skills/*/SKILL.md",
)
GOVERNANCE_SCRIPT_GLOBS = (
    ".ia/skills/**/*.py",
)
DUPLICATE_DOC_GLOBS = (
    ".ia/*.md",
    ".ia/docs/architecture/*.md",
    ".ia/docs/guides/*.md",
    ".ia/docs/templates/*.md",
    ".ia/skills/*/SKILL.md",
    ".ia/skills/*/*.md",
)
DUPLICATE_DOC_MIN_BYTES = 100
DUPLICATE_DOC_MIN_GROUP_SIZE = 2
STALE_TECH_TERMS = ("Redis", "Celery", "Elasticsearch")
DENIAL_MARKERS = (
    "nao ha",
    "não há",
    "sem ",
    "não está",
    "nao esta",
    "não existe",
    "nao existe",
    "não presente",
    "nao presente",
    "ausente",
    "ausentes",
    "obsoleto",
    "fallback",
)
PATH_REFERENCE_PATTERN = re.compile(
    r"(?P<path>AGENTS\.md|pyproject\.toml|base/settings\.py|\.ia/[A-Za-z0-9_./-]+)"
)
OPTIONAL_WORKSPACE_REFERENCES = {
    "pyproject.toml",
    "base/settings.py",
}
SKILL_NAME_PATTERN = re.compile(r"`([a-z][a-z0-9_-]+)`")
README_SKILL_ROW_PATTERN = re.compile(r"^\| `([^`]+)` \|", re.MULTILINE)
DONE_STATUS_PATTERN = re.compile(r"^- Status da task: `([^`]*)`$", re.MULTILINE)
TASKIPY_SECTION_PATTERN = re.compile(
    r"^\[tool\.taskipy\.tasks\]\n(?P<body>.*?)(?=^\[|\Z)",
    re.MULTILINE | re.DOTALL,
)
TASKIPY_COMMAND_PATTERN = re.compile(r'^(?P<name>[A-Za-z0-9_-]+)\s*=\s*"(?P<command>[^"]+)"')
TASKIPY_LOCAL_PATH_PATTERN = re.compile(r"(?:python\s+)?(?P<path>(?:\.ia|scripts)/[A-Za-z0-9_./-]+\.py)")
AGENT_COMMAND_SNIPPET_PATTERN = re.compile(r"`([^`\n]+)`")
AGENT_COMMAND_LINE_PATTERN = re.compile(r"^\s*(?P<command>(?:python|uv|docker-compose|task|pytest|source)\s+.+)$")
COMMANDS_REQUIRING_RTK = (
    "python .ia/skills/",
    "python manage.py",
    "uv sync",
    "docker-compose ",
    "task lint",
    "task test",
    "python -m pytest",
    "source .venv/bin/activate",
)

SKILL_REQUIRED_SECTIONS = ("# Objetivo", "# Regras obrigatórias")
SKILL_DESCRIPTION_TRIGGER_PATTERN = re.compile(
    r"(?:[Uu]sar quando|[Uu]sar sempre que|[Uu]se quando|[Uu]se esta skill|[Aa]tiva em)"
)
PLACEHOLDER_TERM_PATTERN = re.compile(
    r"\b(?:XPTO|LOREM IPSUM|LOREM|TODO_FIXME)\b"
)
PLACEHOLDER_TERM_DOC_GLOBS = (
    "AGENTS.md",
    ".ia/skills/*/SKILL.md",
)
AGENT_COMMAND_DOC_GLOBS = (
    "AGENTS.md",
    ".ia/skills/*/SKILL.md",
)
TASK_TEMPLATE_PATH = Path(".ia/docs/templates/task-template.md")
TASK_TEMPLATE_REQUIRED_SNIPPETS = (
    "- Branch base da implementacao:",
    "- Branch de implementacao:",
    "- Status de aprovacao:",
    "## Descricao da solucao implementada",
    "## Trade-offs",
    "## Arquivos alterados",
)
PLACEHOLDER_TERM_EXEMPT_PATHS = (
    Path(".ia/skills/governanca-compliance/SKILL.md"),
)
GENERATOR_PLACEHOLDER_EXEMPT_PATHS = (
    Path(".ia/skills/governanca-compliance/check_ia_governance.py"),
)
CURRENT_TASK_FILENAME_PATTERN = re.compile(
    r"^task-(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d{4})-[A-Za-z0-9]{10}\.md$"
)
CURRENT_DONE_TASK_FILENAME_PATTERN = re.compile(
    r"^done-task-(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d{4})-[A-Za-z0-9]{10}\.md$"
)
LEGACY_DONE_TASK_FILENAME_PATTERN = re.compile(
    r"^done-task-(?P<day>\d{2})_(?P<month>\d{2})_(?P<year>\d{4})-.+\.md$"
)
LEGACY_TASK_FILENAME_PATTERN = re.compile(
    r"^task-(?P<day>\d{2})_(?P<month>\d{2})_(?P<year>\d{4})-.+\.md$"
)
CONTRACT_START_DATE = date(2026, 5, 30)
CONTRACT_DATE_PATTERN = re.compile(r"^(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d{4})$")
TEMPLATE_DATE_VALUES = {"DD-MM-YYYY", "<DD-MM-YYYY>"}
SPEC_STATUS_VALUES = {
    "draft",
    "approved",
    "in_progress",
    "in_review",
    "done",
    "cancelled",
    "superseded",
}
SPEC_DONE_STATUS_VALUES = {"done", "superseded"}
REPORT_STATUS_VALUES = {"draft", "in_review", "done", "superseded"}
ROOT_SPEC_FILENAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*-spec-\d{2}-\d{2}-\d{4}\.md$")
FASTAPI_SPEC_FILENAME_PATTERN = re.compile(
    r"^[a-z0-9][a-z0-9-]*-fastapi-spec-\d{2}-\d{2}-\d{4}\.md$"
)
FASTAPI_LEGACY_SPEC_FILENAME_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}-spec-[A-Za-z0-9_.-]+\.md$")
ACTIVE_SPEC_SUBDIR_EXEMPTIONS = {"done", "legacy", "fastapi"}
LEGACY_ACTIVE_SPEC_SUBDIRS = {"api", "flutter", "bb-api-pix"}
LEGACY_DATE_TOKEN_PATTERN = re.compile(
    r"DD_MM_YYYY|DD/MM/YYYY|YYYY-MM-DD|data_dd_mm_yyyy|dd_mm_yyyy|task-DD_MM"
)
LEGACY_DATE_REFERENCE_GLOBS = (
    "AGENTS.md",
    ".ia/README.md",
    ".ia/docs/templates/*.md",
    ".ia/skills/*/SKILL.md",
)
LEGACY_DATE_ALLOWED_CONTEXT_MARKERS = (
    "legado",
    "legada",
    "legadas",
    "historico",
    "historica",
    "historicas",
    "histórico",
    "histórica",
    "históricas",
    "bloquear",
    "bloqueio",
    "falhar",
    "falha",
    "proibido",
    "proibida",
    "nao canonico",
    "não canonico",
    "não canônico",
    "antigo",
    "antiga",
    "retrocompat",
    "permitido",
    "permitida",
    "leitura",
    "exige",
    "exigir",
    "instruirem",
    "instruírem",
)


@dataclass
class Finding:
    category: str
    file_path: Path
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Valida a governanca documental e operacional de AGENTS.md e .ia/."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Raiz do repositório a ser validado.",
    )
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def gather_files(root: Path, patterns: tuple[str, ...]) -> list[Path]:
    files: list[Path] = []
    for pattern in patterns:
        files.extend(sorted(root.glob(pattern)))
    unique: list[Path] = []
    seen: set[Path] = set()
    for file_path in files:
        resolved = file_path.resolve()
        if resolved in seen or not file_path.is_file():
            continue
        seen.add(resolved)
        unique.append(file_path)
    return unique


def normalize_reference(raw_path: str) -> str:
    return raw_path.rstrip(").,;:")


def is_placeholder_reference(text: str, match: re.Match[str], raw_reference: str) -> bool:
    if "..." in raw_reference:
        return True
    end = match.end("path")
    return end < len(text) and text[end] == "<"


def actual_skill_names(root: Path) -> set[str]:
    skill_root = root / ".ia" / "skills"
    names: set[str] = set()
    if not skill_root.exists():
        return names
    for skill_dir in sorted(skill_root.iterdir()):
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
            names.add(skill_dir.name)
    return names


def skill_names_from_agents(root: Path) -> set[str]:
    text = read_text(root / "AGENTS.md")
    try:
        catalog = text.split("### 3.2. Catálogo", 1)[1].split("### 3.3.", 1)[0]
    except IndexError:
        return set()
    return set(SKILL_NAME_PATTERN.findall(catalog))


def skill_names_from_readme(root: Path) -> set[str]:
    text = read_text(root / ".ia" / "README.md")
    try:
        section = text.split("### Skills disponíveis", 1)[1].split("### Scripts de automação", 1)[0]
    except IndexError:
        return set()
    return set(README_SKILL_ROW_PATTERN.findall(section))


def check_placeholders(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for file_path in gather_files(root, PLACEHOLDER_DOC_GLOBS):
        text = read_text(file_path)
        for pattern in PLACEHOLDER_PATTERNS:
            match = pattern.search(text)
            if match:
                findings.append(
                    Finding(
                        category="placeholder",
                        file_path=file_path,
                        message=f"placeholder encontrado: `{match.group(0)[:80]}`",
                    )
                )
                break
    return findings


def check_done_task_status(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for file_path in sorted((root / ".ia" / "docs" / "tasks" / "done").glob("done-task-*.md")):
        text = read_text(file_path)
        match = DONE_STATUS_PATTERN.search(text)
        if not match:
            if is_legacy_task_before_contract(file_path):
                continue
            findings.append(
                Finding(
                    category="task_status",
                    file_path=file_path,
                    message="task em done sem campo de status",
                )
            )
            continue
        status = match.group(1).strip()
        if status != ALLOWED_DONE_STATUS:
            if is_legacy_task_before_contract(file_path):
                continue
            findings.append(
                Finding(
                    category="task_status",
                    file_path=file_path,
                    message=f"status invalido em done: `{status}`",
                )
            )
    return findings


def normalize_task_lifecycle_key(file_path: Path) -> str:
    name = file_path.name
    if name.startswith("done-"):
        return name[len("done-"):]
    return name


def check_task_duplicate_lifecycle(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    task_root = root / ".ia" / "docs" / "tasks"
    todo_by_key = {
        normalize_task_lifecycle_key(path): path
        for path in sorted((task_root / "todo").glob("task-*.md"))
    }
    done_by_key = {
        normalize_task_lifecycle_key(path): path
        for path in sorted((task_root / "done").glob("done-task-*.md"))
    }
    for task_key in sorted(set(todo_by_key) & set(done_by_key)):
        if is_legacy_task_name_before_contract(task_key):
            continue
        findings.append(
            Finding(
                category="task_duplicate_lifecycle",
                file_path=todo_by_key[task_key],
                message=(
                    "mesma task aparece em todo e done; "
                    f"done=`{done_by_key[task_key].relative_to(root)}`"
                ),
            )
        )
    return findings


def check_task_status_consistency(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    task_files = sorted((root / ".ia" / "docs" / "tasks" / "todo").glob("task-*.md"))
    task_files.extend(sorted((root / ".ia" / "docs" / "tasks" / "done").glob("done-task-*.md")))
    for file_path in task_files:
        if is_legacy_task_before_contract(file_path):
            continue
        statuses = [match.strip() for match in DONE_STATUS_PATTERN.findall(read_text(file_path))]
        if len(statuses) <= 1:
            continue
        unique_statuses = sorted(set(statuses))
        if len(unique_statuses) > 1:
            findings.append(
                Finding(
                    category="task_multiple_status_fields",
                    file_path=file_path,
                    message=f"multiplos campos `Status da task`: {statuses}",
                )
            )
            findings.append(
                Finding(
                    category="task_conflicting_status_fields",
                    file_path=file_path,
                    message=f"valores conflitantes em `Status da task`: {unique_statuses}",
                )
            )
    return findings


def check_broken_references(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    current_docs = gather_files(root, CURRENT_DOC_GLOBS)
    for file_path in current_docs:
        if is_legacy_task_before_contract(file_path):
            continue
        text = read_text(file_path)
        seen_references: set[str] = set()
        for match in PATH_REFERENCE_PATTERN.finditer(text):
            raw_reference = normalize_reference(match.group("path"))
            if is_placeholder_reference(text, match, raw_reference):
                continue
            if raw_reference in seen_references:
                continue
            seen_references.add(raw_reference)
            if raw_reference in OPTIONAL_WORKSPACE_REFERENCES and not (root / raw_reference).exists():
                continue
            if raw_reference.startswith(".ia/") or raw_reference in {"AGENTS.md", "pyproject.toml", "base/settings.py"}:
                reference_path = root / raw_reference
                if not reference_path.exists():
                    findings.append(
                        Finding(
                            category="broken_reference",
                            file_path=file_path,
                            message=f"referencia local inexistente: `{raw_reference}`",
                        )
                    )
    return findings


def check_task_template_contract(root: Path) -> list[Finding]:
    task_template = root / TASK_TEMPLATE_PATH
    if not task_template.exists():
        return []

    text = read_text(task_template)
    findings: list[Finding] = []
    statuses = DONE_STATUS_PATTERN.findall(text)

    if len(statuses) != 1:
        findings.append(
            Finding(
                category="task_template_contract",
                file_path=task_template,
                message=(
                    "task-template deve conter exatamente um campo `Status da task`; "
                    f"encontrados={len(statuses)}"
                ),
            )
        )

    for snippet in TASK_TEMPLATE_REQUIRED_SNIPPETS:
        if snippet not in text:
            findings.append(
                Finding(
                    category="task_template_contract",
                    file_path=task_template,
                    message=f"task-template sem trecho obrigatorio para automacao: `{snippet}`",
                )
            )

    return findings


def is_valid_calendar_date(day: int, month: int, year: int) -> bool:
    try:
        date(year, month, day)
    except ValueError:
        return False
    return True


def is_valid_contract_date(value: str) -> bool:
    normalized = value.strip().strip("`")
    if normalized in TEMPLATE_DATE_VALUES:
        return True
    match = CONTRACT_DATE_PATTERN.fullmatch(normalized)
    if not match:
        return False
    return is_valid_calendar_date(
        int(match.group("day")),
        int(match.group("month")),
        int(match.group("year")),
    )


def pattern_date_is_valid(match: re.Match[str]) -> bool:
    return is_valid_calendar_date(
        int(match.group("day")),
        int(match.group("month")),
        int(match.group("year")),
    )


def date_from_filename_match(match: re.Match[str]) -> date | None:
    try:
        return date(
            int(match.group("year")),
            int(match.group("month")),
            int(match.group("day")),
        )
    except ValueError:
        return None


def legacy_task_date_from_name(file_name: str) -> date | None:
    for pattern in (LEGACY_TASK_FILENAME_PATTERN, LEGACY_DONE_TASK_FILENAME_PATTERN):
        match = pattern.fullmatch(file_name)
        if not match:
            continue
        return date_from_filename_match(match)
    return None


def is_legacy_task_name_before_contract(file_name: str) -> bool:
    legacy_date = legacy_task_date_from_name(file_name)
    return legacy_date is not None and legacy_date < CONTRACT_START_DATE


def is_legacy_task_before_contract(file_path: Path) -> bool:
    return is_legacy_task_name_before_contract(file_path.name)


def should_enforce_task_metadata_contract(file_path: Path) -> bool:
    if CURRENT_TASK_FILENAME_PATTERN.fullmatch(file_path.name):
        return True
    if CURRENT_DONE_TASK_FILENAME_PATTERN.fullmatch(file_path.name):
        return True
    return not is_legacy_task_before_contract(file_path)


def metadata_value(text: str, field_name: str) -> str | None:
    pattern = re.compile(
        rf"^-\s*{re.escape(field_name)}:\s*(.+?)\s*$",
        re.MULTILINE,
    )
    match = pattern.search(text)
    if not match:
        return None
    value = match.group(1).strip()
    if value.startswith("`") and value.endswith("`"):
        value = value[1:-1].strip()
    return value


def check_task_filename_date_contract(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    task_root = root / ".ia" / "docs" / "tasks"

    for file_path in sorted((task_root / "todo").glob("*.md")):
        match = CURRENT_TASK_FILENAME_PATTERN.fullmatch(file_path.name)
        if not match:
            if is_legacy_task_before_contract(file_path):
                continue
            findings.append(
                Finding(
                    category="task_filename_date_contract",
                    file_path=file_path,
                    message="task aberta deve seguir `task-DD-MM-YYYY-<hash_alfanumerico_10>.md`",
                )
            )
            continue
        if not pattern_date_is_valid(match):
            findings.append(
                Finding(
                    category="task_filename_date_contract",
                    file_path=file_path,
                    message="data invalida no nome da task aberta",
                )
            )

    for file_path in sorted((task_root / "done").glob("done-task-*.md")):
        current_match = CURRENT_DONE_TASK_FILENAME_PATTERN.fullmatch(file_path.name)
        if current_match and not pattern_date_is_valid(current_match):
            findings.append(
                Finding(
                    category="task_filename_date_contract",
                    file_path=file_path,
                    message="data invalida no nome da task concluida",
                )
            )
        elif current_match or is_legacy_task_before_contract(file_path):
            continue

    return findings


def check_todo_legacy_task_contract(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    todo_root = root / ".ia" / "docs" / "tasks" / "todo"

    for file_path in sorted(todo_root.glob("task-*.md")):
        if not LEGACY_TASK_FILENAME_PATTERN.fullmatch(file_path.name):
            continue
        findings.append(
            Finding(
                category="task_todo_legacy_contract",
                file_path=file_path,
                message=(
                    "task com `DD_MM_YYYY` nao pode permanecer no backlog operacional; "
                    "mover para `.ia/docs/tasks/legacy/` ou recriar no contrato atual"
                ),
            )
        )

    return findings


def check_metadata_date_contract(root: Path) -> list[Finding]:
    findings: list[Finding] = []

    task_files = [
        file_path
        for file_path in sorted((root / ".ia" / "docs" / "tasks" / "todo").glob("*.md"))
        if should_enforce_task_metadata_contract(file_path)
    ]
    task_files.extend(
        file_path
        for file_path in sorted((root / ".ia" / "docs" / "tasks" / "done").glob("done-task-*.md"))
        if CURRENT_DONE_TASK_FILENAME_PATTERN.fullmatch(file_path.name)
    )
    for file_path in task_files:
        text = read_text(file_path)
        for field_name in ("Data de criacao", "Ultima atualizacao"):
            value = metadata_value(text, field_name)
            if value is None or not is_valid_contract_date(value):
                findings.append(
                    Finding(
                        category="metadata_date_contract",
                        file_path=file_path,
                        message=f"campo `{field_name}` deve usar `DD-MM-YYYY`; atual=`{value or 'ausente'}`",
                    )
                )

    task_template = root / TASK_TEMPLATE_PATH
    if task_template.exists():
        text = read_text(task_template)
        for field_name in ("Data de criacao", "Ultima atualizacao"):
            value = metadata_value(text, field_name)
            if value is None or not is_valid_contract_date(value):
                findings.append(
                    Finding(
                        category="metadata_date_contract",
                        file_path=task_template,
                        message=f"template deve usar `{field_name}: <DD-MM-YYYY>`; atual=`{value or 'ausente'}`",
                    )
                )

    spec_files = gather_files(
        root,
        (
            ".ia/docs/specs/*.md",
            ".ia/docs/specs/done/*.md",
            ".ia/docs/specs/fastapi/*.md",
            ".ia/docs/templates/spec-template.md",
        ),
    )
    for file_path in spec_files:
        value = metadata_value(read_text(file_path), "Data")
        if value is None or not is_valid_contract_date(value):
            findings.append(
                Finding(
                    category="metadata_date_contract",
                    file_path=file_path,
                    message=f"campo `Data` deve usar `DD-MM-YYYY`; atual=`{value or 'ausente'}`",
                )
            )

    return findings


def check_spec_status_contract(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    spec_files = gather_files(
        root,
        (
            ".ia/docs/specs/*.md",
            ".ia/docs/specs/done/*.md",
            ".ia/docs/specs/fastapi/*.md",
        ),
    )
    for file_path in spec_files:
        status = metadata_value(read_text(file_path), "Status")
        if status not in SPEC_STATUS_VALUES:
            findings.append(
                Finding(
                    category="spec_status_contract",
                    file_path=file_path,
                    message=f"status de spec fora do enum em ingles: `{status or 'ausente'}`",
                )
            )
            continue
        if ".ia/docs/specs/done/" in file_path.as_posix() and status not in SPEC_DONE_STATUS_VALUES:
            findings.append(
                Finding(
                    category="spec_status_contract",
                    file_path=file_path,
                    message=f"spec em done deve usar `done` ou `superseded`; atual=`{status}`",
                )
            )
    return findings


def check_spec_filename_date_contract(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    specs_root = root / ".ia" / "docs" / "specs"

    for file_path in sorted(specs_root.glob("*.md")):
        if not ROOT_SPEC_FILENAME_PATTERN.fullmatch(file_path.name):
            findings.append(
                Finding(
                    category="spec_filename_date_contract",
                    file_path=file_path,
                    message="spec corrente deve seguir `<dominio>-<descricao-curta>-spec-DD-MM-YYYY.md`",
                )
            )

    fastapi_root = specs_root / "fastapi"
    for file_path in sorted(fastapi_root.glob("*.md")):
        if FASTAPI_SPEC_FILENAME_PATTERN.fullmatch(file_path.name):
            continue
        status = metadata_value(read_text(file_path), "Status")
        if FASTAPI_LEGACY_SPEC_FILENAME_PATTERN.fullmatch(file_path.name) and status in SPEC_DONE_STATUS_VALUES:
            continue
        findings.append(
            Finding(
                category="spec_filename_date_contract",
                file_path=file_path,
                message=(
                    "spec FastAPI corrente deve seguir "
                    "`<dominio>-<descricao-curta>-fastapi-spec-DD-MM-YYYY.md`; "
                    "nomes `YYYY-MM-DD-spec-*` so sao permitidos como legado concluido"
                ),
            )
        )
    return findings


def check_active_spec_subdir_contract(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    specs_root = root / ".ia" / "docs" / "specs"
    if not specs_root.exists():
        return findings

    for spec_dir in sorted(specs_root.iterdir()):
        if not spec_dir.is_dir() or spec_dir.name in ACTIVE_SPEC_SUBDIR_EXEMPTIONS:
            continue

        spec_files = sorted(spec_dir.glob("*.md"))
        if not spec_files:
            continue

        if spec_dir.name in LEGACY_ACTIVE_SPEC_SUBDIRS:
            findings.append(
                Finding(
                    category="spec_legacy_active_directory",
                    file_path=spec_dir,
                    message=(
                        "subpasta historica de specs nao pode voltar como planejamento ativo; "
                        f"mover para `.ia/docs/specs/legacy/{spec_dir.name}/` "
                        "ou recriar specs no contrato atual"
                    ),
                )
            )
            continue

        for file_path in spec_files:
            status = metadata_value(read_text(file_path), "Status")
            if status not in SPEC_STATUS_VALUES:
                findings.append(
                    Finding(
                        category="spec_active_subdir_status_contract",
                        file_path=file_path,
                        message=(
                            "spec em subpasta ativa deve declarar status canonico; "
                            f"atual=`{status or 'ausente'}`"
                        ),
                    )
                )
            if not (
                ROOT_SPEC_FILENAME_PATTERN.fullmatch(file_path.name)
                or FASTAPI_SPEC_FILENAME_PATTERN.fullmatch(file_path.name)
            ):
                findings.append(
                    Finding(
                        category="spec_active_subdir_filename_contract",
                        file_path=file_path,
                        message=(
                            "spec em subpasta ativa deve seguir "
                            "`<dominio>-<descricao-curta>-spec-DD-MM-YYYY.md` "
                            "ou `<dominio>-<descricao-curta>-fastapi-spec-DD-MM-YYYY.md`"
                        ),
                    )
                )

    return findings


def check_report_metadata_contract(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for file_path in sorted((root / ".ia" / "docs" / "reports").glob("*.md")):
        text = read_text(file_path)
        data_value = metadata_value(text, "Data")
        status_value = metadata_value(text, "Status do relatorio")
        escopo_value = metadata_value(text, "Escopo")
        validation_value = metadata_value(text, "Validacao executada")

        if data_value is None or not is_valid_contract_date(data_value):
            findings.append(
                Finding(
                    category="report_metadata_contract",
                    file_path=file_path,
                    message=f"report deve declarar `Data: DD-MM-YYYY`; atual=`{data_value or 'ausente'}`",
                )
            )
        if status_value not in REPORT_STATUS_VALUES:
            findings.append(
                Finding(
                    category="report_metadata_contract",
                    file_path=file_path,
                    message=f"report deve usar status em ingles; atual=`{status_value or 'ausente'}`",
                )
            )
        if not escopo_value:
            findings.append(
                Finding(
                    category="report_metadata_contract",
                    file_path=file_path,
                    message="report sem campo `Escopo`",
                )
            )
        if not validation_value:
            findings.append(
                Finding(
                    category="report_metadata_contract",
                    file_path=file_path,
                    message="report sem campo `Validacao executada`",
                )
            )
    return findings


def check_legacy_date_reference_contract(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for file_path in gather_files(root, LEGACY_DATE_REFERENCE_GLOBS):
        for line_no, line in enumerate(read_text(file_path).splitlines(), 1):
            match = LEGACY_DATE_TOKEN_PATTERN.search(line)
            if not match:
                continue
            normalized_line = line.casefold()
            if any(marker in normalized_line for marker in LEGACY_DATE_ALLOWED_CONTEXT_MARKERS):
                continue
            findings.append(
                Finding(
                    category="legacy_date_reference_contract",
                    file_path=file_path,
                    message=(
                        f"L{line_no}: referencia a padrao legado `{match.group(0)}` "
                        "sem contexto de legado/bloqueio"
                    ),
                )
            )
    return findings


def check_hardcoded_paths(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    files = gather_files(root, CURRENT_DOC_GLOBS) + gather_files(root, GOVERNANCE_SCRIPT_GLOBS)
    hardcoded_pattern = re.compile(r"(/Users/[^/\s]+/|[A-Za-z]:\\\\Users\\\\[^\\\s]+\\\\)")
    for file_path in files:
        if file_path.name == "check_ia_governance.py":
            continue
        text = read_text(file_path)
        match = hardcoded_pattern.search(text)
        if match:
            findings.append(
                Finding(
                    category="hardcoded_path",
                    file_path=file_path,
                    message=f"caminho pessoal hardcoded encontrado: `{match.group(1)}`",
                )
            )
    return findings


def check_agents_md_freshness(root: Path) -> list[Finding]:
    agents_path = root / "AGENTS.md"
    overview_path = root / ".ia" / "docs" / "architecture" / "overview.md"
    if not agents_path.exists() or not overview_path.exists():
        return []
    overview_lower = read_text(overview_path).lower()
    agents_lines = read_text(agents_path).splitlines()
    findings: list[Finding] = []
    skill_catalog_pattern = re.compile(r"`django-[a-z-]+`|`fastapi-[a-z-]+`")
    for term in STALE_TECH_TERMS:
        term_lower = term.lower()
        if term_lower not in overview_lower:
            continue
        if not any(marker in overview_lower for marker in DENIAL_MARKERS):
            continue
        for line_no, line in enumerate(agents_lines, 1):
            line_lower = line.lower()
            if term_lower not in line_lower:
                continue
            if any(marker in line_lower for marker in DENIAL_MARKERS):
                continue
            if skill_catalog_pattern.search(line):
                continue
            findings.append(
                Finding(
                    category="agents_md_freshness",
                    file_path=agents_path,
                    message=(
                        f"L{line_no}: termo `{term}` mencionado sem qualificacao em AGENTS.md, "
                        f"mas declarado ausente em overview.md. Adicionar denial marker ou reescrever."
                    ),
                )
            )
    return findings


def check_duplicate_docs(root: Path) -> list[Finding]:
    files = gather_files(root, DUPLICATE_DOC_GLOBS)
    by_hash: dict[str, list[Path]] = {}
    for file_path in files:
        data = file_path.read_bytes()
        if len(data) < DUPLICATE_DOC_MIN_BYTES:
            continue
        digest = hashlib.sha256(data).hexdigest()
        by_hash.setdefault(digest, []).append(file_path)
    findings: list[Finding] = []
    for group in by_hash.values():
        if len(group) < DUPLICATE_DOC_MIN_GROUP_SIZE:
            continue
        canonical = group[0]
        for duplicate in group[1:]:
            findings.append(
                Finding(
                    category="duplicate_doc",
                    file_path=duplicate,
                    message=f"conteudo identico a `{canonical.relative_to(root)}`",
                )
            )
    return findings


def check_skill_required_sections(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    skill_root = root / ".ia" / "skills"
    if not skill_root.exists():
        return findings
    for skill_dir in sorted(skill_root.iterdir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            continue
        text = read_text(skill_file)
        for required in SKILL_REQUIRED_SECTIONS:
            if required not in text:
                findings.append(
                    Finding(
                        category="skill_missing_section",
                        file_path=skill_file,
                        message=f"SKILL.md sem secao obrigatoria: `{required}`",
                    )
                )
    return findings


def check_skill_description_trigger(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    skill_root = root / ".ia" / "skills"
    if not skill_root.exists():
        return findings
    for skill_dir in sorted(skill_root.iterdir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            continue
        text = read_text(skill_file)
        if not text.startswith("---"):
            continue
        try:
            frontmatter = text.split("---", 2)[1]
        except IndexError:
            continue
        description_idx = frontmatter.find("description:")
        description_body = (
            frontmatter[description_idx + len("description:"):].strip()
            if description_idx != -1
            else ""
        )
        if not description_body or not SKILL_DESCRIPTION_TRIGGER_PATTERN.search(description_body):
            findings.append(
                Finding(
                    category="skill_description_trigger",
                    file_path=skill_file,
                    message=(
                        "frontmatter `description:` sem gatilho explicito "
                        "(padrao esperado: `Usar quando`, `Usar sempre que`, `Use quando`, `Use esta skill` ou `Ativa em`)"
                    ),
                )
            )
    return findings


def check_placeholder_terms(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    exempt_resolved = {
        (root / exempt_path).resolve() for exempt_path in PLACEHOLDER_TERM_EXEMPT_PATHS
    }
    for file_path in gather_files(root, PLACEHOLDER_TERM_DOC_GLOBS):
        if file_path.resolve() in exempt_resolved:
            continue
        text = read_text(file_path)
        match = PLACEHOLDER_TERM_PATTERN.search(text)
        if match:
            findings.append(
                Finding(
                    category="placeholder_term",
                    file_path=file_path,
                    message=f"termo placeholder generico encontrado: `{match.group(0)}`",
                )
            )
    return findings


def check_generator_placeholder_terms(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    exempt_resolved = {
        (root / exempt_path).resolve() for exempt_path in GENERATOR_PLACEHOLDER_EXEMPT_PATHS
    }
    for file_path in gather_files(root, GOVERNANCE_SCRIPT_GLOBS):
        if file_path.resolve() in exempt_resolved:
            continue
        text = read_text(file_path)
        match = PLACEHOLDER_TERM_PATTERN.search(text)
        if match:
            findings.append(
                Finding(
                    category="generator_placeholder_term",
                    file_path=file_path,
                    message=f"termo placeholder generico em script gerador: `{match.group(0)}`",
                )
            )
    return findings


def check_taskipy_broken_paths(root: Path) -> list[Finding]:
    pyproject_path = root / "pyproject.toml"
    if not pyproject_path.exists():
        return []
    text = read_text(pyproject_path)
    section_match = TASKIPY_SECTION_PATTERN.search(text)
    if not section_match:
        return []
    findings: list[Finding] = []
    for line in section_match.group("body").splitlines():
        command_match = TASKIPY_COMMAND_PATTERN.match(line.strip())
        if not command_match:
            continue
        task_name = command_match.group("name")
        command = command_match.group("command")
        for path_match in TASKIPY_LOCAL_PATH_PATTERN.finditer(command):
            raw_path = normalize_reference(path_match.group("path"))
            if not (root / raw_path).exists():
                findings.append(
                    Finding(
                        category="taskipy_broken_path",
                        file_path=pyproject_path,
                        message=f"task `{task_name}` aponta para caminho inexistente: `{raw_path}`",
                    )
                )
    return findings


def command_requires_rtk(command: str) -> bool:
    normalized = command.strip()
    if normalized.startswith("rtk "):
        return False
    if normalized.startswith("pytest "):
        return True
    return any(normalized.startswith(prefix) for prefix in COMMANDS_REQUIRING_RTK)


def check_agent_commands_missing_rtk(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for file_path in gather_files(root, AGENT_COMMAND_DOC_GLOBS):
        text = read_text(file_path)
        for line_no, line in enumerate(text.splitlines(), 1):
            line_match = AGENT_COMMAND_LINE_PATTERN.match(line)
            if line_match and command_requires_rtk(line_match.group("command")):
                findings.append(
                    Finding(
                        category="agent_command_missing_rtk",
                        file_path=file_path,
                        message=f"L{line_no}: comando sem prefixo `rtk`: `{line_match.group('command')}`",
                    )
                )
            for snippet in AGENT_COMMAND_SNIPPET_PATTERN.findall(line):
                if command_requires_rtk(snippet):
                    findings.append(
                        Finding(
                            category="agent_command_missing_rtk",
                            file_path=file_path,
                            message=f"L{line_no}: comando sem prefixo `rtk`: `{snippet}`",
                        )
                    )
    return findings


def check_legacy_template_reference(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    legacy_template = root / ".ia" / "docs" / "tasks" / "task-template.md"
    if legacy_template.exists():
        findings.append(
            Finding(
                category="legacy_template_reference",
                file_path=legacy_template,
                message="template legado compete com `.ia/docs/templates/task-template.md`",
            )
        )
    return findings


def check_skill_catalog_consistency(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    actual = actual_skill_names(root)
    agents = skill_names_from_agents(root)
    readme = skill_names_from_readme(root)

    missing_in_agents = sorted(actual - agents)
    missing_in_readme = sorted(actual - readme)
    extra_in_agents = sorted(agents - actual)
    extra_in_readme = sorted(readme - actual)

    if missing_in_agents or extra_in_agents:
        findings.append(
            Finding(
                category="catalog_consistency",
                file_path=root / "AGENTS.md",
                message=(
                    f"divergencia entre catalogo do AGENTS e skills reais; "
                    f"faltando={missing_in_agents or '[]'} extras={extra_in_agents or '[]'}"
                ),
            )
        )

    if missing_in_readme or extra_in_readme:
        findings.append(
            Finding(
                category="catalog_consistency",
                file_path=root / ".ia" / "README.md",
                message=(
                    f"divergencia entre tabela do README e skills reais; "
                    f"faltando={missing_in_readme or '[]'} extras={extra_in_readme or '[]'}"
                ),
            )
        )

    return findings


def run_checks(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    findings.extend(check_placeholders(root))
    findings.extend(check_done_task_status(root))
    findings.extend(check_task_duplicate_lifecycle(root))
    findings.extend(check_task_status_consistency(root))
    findings.extend(check_task_template_contract(root))
    findings.extend(check_task_filename_date_contract(root))
    findings.extend(check_todo_legacy_task_contract(root))
    findings.extend(check_metadata_date_contract(root))
    findings.extend(check_spec_status_contract(root))
    findings.extend(check_spec_filename_date_contract(root))
    findings.extend(check_active_spec_subdir_contract(root))
    findings.extend(check_report_metadata_contract(root))
    findings.extend(check_legacy_date_reference_contract(root))
    findings.extend(check_broken_references(root))
    findings.extend(check_hardcoded_paths(root))
    findings.extend(check_agents_md_freshness(root))
    findings.extend(check_duplicate_docs(root))
    findings.extend(check_skill_catalog_consistency(root))
    findings.extend(check_skill_required_sections(root))
    findings.extend(check_skill_description_trigger(root))
    findings.extend(check_placeholder_terms(root))
    findings.extend(check_generator_placeholder_terms(root))
    findings.extend(check_taskipy_broken_paths(root))
    findings.extend(check_agent_commands_missing_rtk(root))
    findings.extend(check_legacy_template_reference(root))
    return findings


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()

    findings = run_checks(root)
    if not findings:
        print("OK: nenhuma divergencia de governanca encontrada.")
        return 0

    print(f"FINDINGS={len(findings)}")
    for finding in findings:
        relative_path = finding.file_path.resolve().relative_to(root)
        print(f"[{finding.category}] {relative_path}: {finding.message}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
