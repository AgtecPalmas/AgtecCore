#!/usr/bin/env python3
"""Migrate task enum field values from Portuguese to English (field-scoped)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SUBSTITUTIONS = [
    ("- Status da task: `concluida`", "- Status da task: `done`"),
    ("- Prioridade: `alta`", "- Prioridade: `high`"),
    ("- Prioridade: `media`", "- Prioridade: `medium`"),
    ("- Prioridade: `baixa`", "- Prioridade: `low`"),
    ("- Tipo: `testes`", "- Tipo: `tests`"),
    ("- Tipo: `governanca`", "- Tipo: `governance`"),
]


def migrate_file(path: Path, dry_run: bool) -> list[str]:
    original = path.read_text(encoding="utf-8")
    updated = original
    changes: list[str] = []
    for old, new in SUBSTITUTIONS:
        if old in updated:
            changes.append(f"  {path}: {old!r} -> {new!r}")
            updated = updated.replace(old, new)
    if changes and not dry_run:
        path.write_text(updated, encoding="utf-8")
    return changes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Migra campos enumerados de tasks PT -> EN (field-scoped)."
    )
    parser.add_argument("--path", required=True, help="Diretorio com arquivos .md a migrar.")
    parser.add_argument("--dry-run", action="store_true", help="Exibe substituicoes sem aplicar.")
    args = parser.parse_args()

    root = Path(args.path)
    if not root.is_dir():
        print(f"ERRO: {root} nao e um diretorio valido", file=sys.stderr)
        return 1

    files = sorted(root.glob("*.md"))
    all_changes: list[str] = []
    for f in files:
        all_changes.extend(migrate_file(f, dry_run=args.dry_run))

    if args.dry_run:
        if all_changes:
            print(f"DRY-RUN: {len(all_changes)} substituicao(oes) encontrada(s):")
            for c in all_changes:
                print(c)
        else:
            print("DRY-RUN: nenhuma substituicao necessaria.")
    else:
        print(f"Migracao concluida: {len(all_changes)} substituicao(oes) aplicada(s) em {root}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
