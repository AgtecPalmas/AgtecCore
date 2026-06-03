#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

STATUS_PATTERN = re.compile(r"^- Status da task: `([^`]*)`$", re.MULTILINE)
BASE_BRANCH_PATTERN = re.compile(r"^- Branch base da implementacao: `([^`]*)`$", re.MULTILINE)
IMPL_BRANCH_PATTERN = re.compile(r"^- Branch de implementacao: `([^`]*)`$", re.MULTILINE)
TASK_FILENAME_PATTERN = re.compile(
    r"^task-(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d{4})-[A-Za-z0-9]{10}\.md$"
)
LEGACY_TASK_FILENAME_PATTERN = re.compile(
    r"^task-\d{2}_\d{2}_\d{4}-[A-Za-z0-9]{10}\.md$"
)

APPROVED_STATUS = "approved"
IN_PROGRESS_STATUS = "in_progress"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cria ou seleciona a branch de implementacao a partir de uma task aprovada."
    )
    parser.add_argument("task_file", help="Caminho para o arquivo da task aprovada.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Exibe a branch base, a branch de implementacao e as atualizacoes planejadas sem alterar git ou o arquivo da task.",
    )
    return parser.parse_args()


def fail(message: str) -> int:
    print(f"ERRO: {message}", file=sys.stderr)
    return 1


def run_git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or "falha ao executar comando git"
        raise RuntimeError(f"git {' '.join(args)}: {stderr}")
    return result.stdout.strip()


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
        raise ValueError("a abertura de branch so pode usar tasks em .ia/docs/tasks/todo/")

    match = TASK_FILENAME_PATTERN.fullmatch(task_path.name)
    if match:
        try:
            date(
                int(match.group("year")),
                int(match.group("month")),
                int(match.group("day")),
            )
        except ValueError as exc:
            raise ValueError(f"data invalida no nome da task: `{task_path.name}`") from exc
        return

    if LEGACY_TASK_FILENAME_PATTERN.fullmatch(task_path.name):
        raise ValueError(
            "tasks com data em `DD_MM_YYYY` sao legado de leitura; "
            "novas branches exigem `task-DD-MM-YYYY-<hash_alfanumerico_10>.md`"
        )

    raise ValueError(
        "o arquivo da task precisa seguir `task-DD-MM-YYYY-<hash_alfanumerico_10>.md`"
    )


def extract_status(task_text: str) -> str:
    statuses = [match.strip() for match in STATUS_PATTERN.findall(task_text)]
    if not statuses:
        raise ValueError(
            "a task precisa conter um unico campo '- Status da task: `...`' na secao de metadados"
        )
    if len(statuses) > 1:
        raise ValueError(
            "a task precisa conter um unico campo `Status da task`; remova duplicidades antes de abrir a branch"
        )
    return statuses[0]


def replace_single(pattern: re.Pattern[str], replacement: str, content: str) -> str:
    if not pattern.search(content):
        raise ValueError(
            "nao foi possivel localizar um dos campos obrigatorios de Controle de implementacao"
        )
    return pattern.sub(replacement, content, count=1)


def update_task_content(content: str, base_branch: str, implementation_branch: str) -> str:
    updated = replace_single(
        STATUS_PATTERN,
        f"- Status da task: `{IN_PROGRESS_STATUS}`",
        content,
    )
    updated = replace_single(
        BASE_BRANCH_PATTERN,
        f"- Branch base da implementacao: `{base_branch}`",
        updated,
    )
    updated = replace_single(
        IMPL_BRANCH_PATTERN,
        f"- Branch de implementacao: `{implementation_branch}`",
        updated,
    )
    return updated


def branch_exists(repo_root: Path, branch_name: str) -> bool:
    result = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch_name}"],
        cwd=repo_root,
        check=False,
    )
    return result.returncode == 0


def main() -> int:
    args = parse_args()
    task_path = resolve_task_file(args.task_file)

    try:
        validate_task_file(task_path)
        task_text = task_path.read_text(encoding="utf-8")
        status = extract_status(task_text)
        if status != APPROVED_STATUS:
            raise ValueError(
                "a task precisa estar com 'Status da task: `approved`' antes da criacao da branch"
            )

        repo_root = Path(run_git(["rev-parse", "--show-toplevel"], task_path.parent))
        base_branch = run_git(["branch", "--show-current"], repo_root)
        if not base_branch:
            raise RuntimeError(
                "nao foi possivel identificar a branch atual; verifique se o HEAD nao esta destacado"
            )

        implementation_branch = task_path.stem
        next_content = update_task_content(task_text, base_branch, implementation_branch)
        action = "switch" if branch_exists(repo_root, implementation_branch) else "create"

        if args.dry_run:
            print(f"TASK_FILE={task_path}")
            print(f"BASE_BRANCH={base_branch}")
            print(f"IMPLEMENTATION_BRANCH={implementation_branch}")
            print(f"BRANCH_ACTION={action}")
            print(f"NEXT_STATUS={IN_PROGRESS_STATUS}")
            return 0

        if action == "create":
            run_git(["switch", "-c", implementation_branch], repo_root)
        else:
            run_git(["switch", implementation_branch], repo_root)

        task_path.write_text(next_content, encoding="utf-8")
        print(f"Branch pronta: {implementation_branch}")
        print(f"Branch base: {base_branch}")
        print(f"Task atualizada: {task_path}")
        return 0
    except Exception as exc:
        return fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())