#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

TASK_BRANCH_PATTERN = re.compile(
    r"^task-(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d{4})-[A-Za-z0-9]{10}$"
)
LEGACY_TASK_BRANCH_PATTERN = re.compile(
    r"^task-\d{2}_\d{2}_\d{4}-[A-Za-z0-9]{10}$"
)
TARGET_BRANCH = "dev"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Faz o merge da branch de task atual com a branch local 'dev' "
            "seguindo a convencao de nomenclatura do projeto."
        )
    )
    parser.add_argument(
        "--delete-merged-branch",
        metavar="BRANCH_NAME",
        help=(
            "Exclui uma branch local de task ja mergeada em dev. "
            "Use apenas apos confirmacao explicita do desenvolvedor."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Exibe a branch atual, a branch alvo e a acao planejada sem alterar o repositório.",
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


def validate_task_branch(branch_name: str) -> None:
    match = TASK_BRANCH_PATTERN.fullmatch(branch_name)
    if match:
        try:
            date(
                int(match.group("year")),
                int(match.group("month")),
                int(match.group("day")),
            )
        except ValueError as exc:
            raise ValueError(f"data invalida na branch de task: `{branch_name}`") from exc
        return

    if LEGACY_TASK_BRANCH_PATTERN.fullmatch(branch_name):
        raise ValueError(
            "branches de task com data em `DD_MM_YYYY` sao legado de leitura; "
            "para merge local use `task-DD-MM-YYYY-<hash_alfanumerico_10>`"
        )

    raise ValueError(
        "a branch atual precisa seguir o padrao "
        "`task-DD-MM-YYYY-<hash_alfanumerico_10>`"
    )


def ensure_clean_worktree(repo_root: Path) -> None:
    status = run_git(["status", "--short"], repo_root)
    if status:
        raise RuntimeError(
            "o worktree precisa estar limpo antes do merge com dev"
        )


def ensure_local_branch_exists(repo_root: Path, branch_name: str) -> None:
    result = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch_name}"],
        cwd=repo_root,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"a branch local `{branch_name}` nao existe")


def ensure_branch_merged_into_dev(repo_root: Path, branch_name: str) -> None:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", branch_name, TARGET_BRANCH],
        cwd=repo_root,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"a branch `{branch_name}` ainda nao esta mergeada em `{TARGET_BRANCH}`"
        )


def delete_merged_branch(
    repo_root: Path,
    current_branch: str,
    branch_name: str,
    dry_run: bool,
) -> int:
    validate_task_branch(branch_name)
    ensure_local_branch_exists(repo_root, TARGET_BRANCH)
    ensure_local_branch_exists(repo_root, branch_name)

    if current_branch != TARGET_BRANCH:
        raise RuntimeError(
            f"para excluir a branch mergeada, o HEAD atual precisa estar em `{TARGET_BRANCH}`"
        )

    if branch_name == current_branch:
        raise RuntimeError("nao e permitido excluir a branch atualmente selecionada")

    ensure_branch_merged_into_dev(repo_root, branch_name)

    if dry_run:
        print(f"DELETE_BRANCH={branch_name}")
        print(f"TARGET_BRANCH={TARGET_BRANCH}")
        print("DELETE_STRATEGY=git branch -d <task_branch>")
        return 0

    ensure_clean_worktree(repo_root)
    run_git(["branch", "-d", branch_name], repo_root)
    print(f"Branch excluida: {branch_name}")
    print(f"HEAD atual: {TARGET_BRANCH}")
    return 0


def main() -> int:
    args = parse_args()

    try:
        repo_root = Path(run_git(["rev-parse", "--show-toplevel"], Path.cwd()))
        current_branch = run_git(["branch", "--show-current"], repo_root)
        if not current_branch:
            raise RuntimeError(
                "nao foi possivel identificar a branch atual; verifique se o HEAD nao esta destacado"
            )

        if args.delete_merged_branch:
            return delete_merged_branch(
                repo_root=repo_root,
                current_branch=current_branch,
                branch_name=args.delete_merged_branch,
                dry_run=args.dry_run,
            )

        validate_task_branch(current_branch)
        ensure_local_branch_exists(repo_root, TARGET_BRANCH)

        if args.dry_run:
            print(f"TASK_BRANCH={current_branch}")
            print(f"TARGET_BRANCH={TARGET_BRANCH}")
            print("MERGE_STRATEGY=git switch dev && git merge --no-ff <task_branch>")
            return 0

        ensure_clean_worktree(repo_root)
        run_git(["switch", TARGET_BRANCH], repo_root)
        merge_message = f"Merge branch '{current_branch}' into {TARGET_BRANCH}"
        run_git(["merge", "--no-ff", current_branch, "-m", merge_message], repo_root)

        print(f"Merge concluido: {current_branch} -> {TARGET_BRANCH}")
        print(f"HEAD atual: {TARGET_BRANCH}")
        print(
            "Pergunte ao desenvolvedor se deseja excluir a branch mergeada e, "
            f"se confirmado, execute: --delete-merged-branch {current_branch}"
        )
        return 0
    except Exception as exc:
        return fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
