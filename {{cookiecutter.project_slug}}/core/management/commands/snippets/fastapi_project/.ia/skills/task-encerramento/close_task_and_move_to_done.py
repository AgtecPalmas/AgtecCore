#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import shutil
import sys
import unicodedata
from datetime import date
from pathlib import Path

STATUS_PATTERN = re.compile(r"^- Status da task: `([^`]*)`$", re.MULTILINE)
BASE_BRANCH_PATTERN = re.compile(r"^- Branch base da implementacao: `([^`]*)`$", re.MULTILINE)
IMPL_BRANCH_PATTERN = re.compile(r"^- Branch de implementacao: `([^`]*)`$", re.MULTILINE)
SECTION_PATTERN = re.compile(r"^##+ (.+?)\n(.*?)(?=^##+ |\Z)", re.MULTILINE | re.DOTALL)
TASK_FILENAME_PATTERN = re.compile(
    r"^task-(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d{4})-[A-Za-z0-9]{10}\.md$"
)
LEGACY_TASK_FILENAME_PATTERN = re.compile(
    r"^task-(?P<day>\d{2})_(?P<month>\d{2})_(?P<year>\d{4})-[A-Za-z0-9]{10}\.md$"
)

IN_PROGRESS_STATUS = "in_progress"
DONE_STATUS = "done"
CONTRACT_START_DATE = date(2026, 5, 30)
REQUIRED_SECTIONS = {
    "Descricao da solucao implementada": (
        "Descricao da solucao implementada",
        "Descrição da solução implementada",
        "Descrição da Solução Implementada",
    ),
    "Trade-offs": ("Trade-offs",),
    "Arquivos alterados": (
        "Arquivos alterados",
        "Arquivos Alterados",
        "Arquivos alterados/criados/removidos",
        "Arquivos Alterados/Criados",
        "Arquivos alterados (execucao parcial)",
    ),
}
PLACEHOLDER_TEXTS = {
    "Descricao da solucao implementada": {"Preencher ao concluir a demanda."},
    "Trade-offs": {"Preencher ao concluir a demanda."},
    "Arquivos alterados": {"- Preencher ao concluir a demanda."},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Valida o fechamento de uma task e move o arquivo para .ia/docs/tasks/done/."
    )
    parser.add_argument("task_file", help="Caminho para o arquivo da task em implementacao.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Valida o fechamento e exibe o caminho final sem mover o arquivo.",
    )
    return parser.parse_args()


def fail(message: str) -> int:
    print(f"ERRO: {message}", file=sys.stderr)
    return 1


def resolve_task_file(raw_path: str) -> Path:
    task_path = Path(raw_path).expanduser()
    if not task_path.is_absolute():
        task_path = Path.cwd() / task_path
    return task_path.resolve()


def validate_task_file(task_path: Path) -> None:
    if not task_path.exists():
        raise FileNotFoundError(f"task nao encontrada: {task_path}")
    if task_path.suffix != ".md":
        raise ValueError("o arquivo da task precisa terminar com .md")
    if task_path.parent.name != "todo":
        raise ValueError("o encerramento so pode ser executado para tasks em .ia/docs/tasks/todo/")

    current_match = TASK_FILENAME_PATTERN.fullmatch(task_path.name)
    if current_match:
        try:
            date(
                int(current_match.group("year")),
                int(current_match.group("month")),
                int(current_match.group("day")),
            )
        except ValueError as exc:
            raise ValueError(f"data invalida no nome da task: `{task_path.name}`") from exc
        return

    legacy_match = LEGACY_TASK_FILENAME_PATTERN.fullmatch(task_path.name)
    if legacy_match:
        try:
            legacy_date = date(
                int(legacy_match.group("year")),
                int(legacy_match.group("month")),
                int(legacy_match.group("day")),
            )
        except ValueError as exc:
            raise ValueError(f"data invalida no nome legado da task: `{task_path.name}`") from exc
        if legacy_date < CONTRACT_START_DATE:
            return
        raise ValueError(
            "tasks em `DD_MM_YYYY` com data igual ou posterior a 30-05-2026 "
            "nao podem ser encerradas como novo artefato; use `DD-MM-YYYY`"
        )

    raise ValueError(
        "o arquivo da task precisa seguir `task-DD-MM-YYYY-<hash_alfanumerico_10>.md` "
        "ou ser legado anterior a 30-05-2026 em `DD_MM_YYYY`"
    )


def extract_status(task_text: str) -> str:
    statuses = [match.strip() for match in STATUS_PATTERN.findall(task_text)]
    if not statuses:
        raise ValueError(
            "a task precisa conter um unico campo '- Status da task: `...`' na secao de metadados"
        )
    if len(statuses) > 1:
        raise ValueError(
            "a task precisa conter um unico campo `Status da task`; remova duplicidades antes do encerramento"
        )
    return statuses[0]


def extract_field(pattern: re.Pattern[str], task_text: str, field_name: str) -> str:
    match = pattern.search(task_text)
    if not match:
        raise ValueError(f"nao foi possivel localizar o campo obrigatorio `{field_name}`")
    return match.group(1).strip()


def extract_sections(task_text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    for heading, content in SECTION_PATTERN.findall(task_text):
        sections[heading.strip()] = content.strip()
    return sections


def normalize_heading(heading: str) -> str:
    normalized = unicodedata.normalize("NFKD", heading)
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    return normalized.casefold()


def resolve_section_content(sections: dict[str, str], canonical_name: str) -> str:
    aliases = REQUIRED_SECTIONS[canonical_name]
    normalized_sections = {
        normalize_heading(heading): content for heading, content in sections.items()
    }
    for alias in aliases:
        content = normalized_sections.get(normalize_heading(alias), "").strip()
        if content:
            return content
    return ""


def validate_required_sections(sections: dict[str, str]) -> None:
    for section_name, placeholders in PLACEHOLDER_TEXTS.items():
        content = resolve_section_content(sections, section_name)
        if not content:
            raise ValueError(f"a secao `{section_name}` precisa estar preenchida antes do encerramento")
        if content in placeholders:
            raise ValueError(f"a secao `{section_name}` ainda contem placeholder")

    arquivos_alterados = resolve_section_content(sections, "Arquivos alterados")
    if not re.search(r"^- .+", arquivos_alterados, re.MULTILINE):
        raise ValueError("a secao `Arquivos alterados` precisa listar ao menos um item com bullet")


def replace_single(pattern: re.Pattern[str], replacement: str, content: str) -> str:
    if not pattern.search(content):
        raise ValueError("nao foi possivel localizar o status da task para atualizacao")
    return pattern.sub(replacement, content, count=1)


def build_done_path(task_path: Path) -> Path:
    done_dir = task_path.parent.parent / "done"
    return done_dir / f"done-{task_path.name}"


def main() -> int:
    args = parse_args()
    task_path = resolve_task_file(args.task_file)

    try:
        validate_task_file(task_path)
        task_text = task_path.read_text(encoding="utf-8")
        status = extract_status(task_text)
        if status != IN_PROGRESS_STATUS:
            raise ValueError(
                "a task precisa estar com 'Status da task: `in_progress`' antes do encerramento"
            )

        extract_field(BASE_BRANCH_PATTERN, task_text, "Branch base da implementacao")
        extract_field(IMPL_BRANCH_PATTERN, task_text, "Branch de implementacao")
        sections = extract_sections(task_text)
        validate_required_sections(sections)

        done_path = build_done_path(task_path)
        if done_path.exists():
            raise FileExistsError(f"o arquivo final ja existe: {done_path}")

        updated_text = replace_single(
            STATUS_PATTERN,
            f"- Status da task: `{DONE_STATUS}`",
            task_text,
        )

        if args.dry_run:
            print(f"TASK_FILE={task_path}")
            print(f"DONE_FILE={done_path}")
            print(f"NEXT_STATUS={DONE_STATUS}")
            return 0

        done_path.parent.mkdir(parents=True, exist_ok=True)
        task_path.write_text(updated_text, encoding="utf-8")
        shutil.move(str(task_path), str(done_path))
        print(f"Task encerrada: {done_path}")
        print(f"STATUS_FINAL={DONE_STATUS}")
        return 0
    except Exception as exc:
        return fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
