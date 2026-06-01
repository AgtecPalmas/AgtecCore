#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import unicodedata
from pathlib import Path

DEFAULT_REPO_PATH = Path(__file__).resolve().parents[4]
DEFAULT_REPO_DOC_ROOTS = (
    Path('.ia/docs'),
    Path('.ia'),
)
VAULT_SYSTEM_ROOTS = (
    "01-Sistemas",
    "01 Projects",
)
STOPWORDS = {
    'a', 'o', 'as', 'os', 'de', 'da', 'do', 'das', 'dos', 'e', 'em', 'no', 'na',
    'para', 'por', 'que', 'qual', 'quais', 'ultima', 'ultimo', 'ultimas', 'ultimos',
    'implementamos', 'projeto', 'sistema', 'cofre', 'obsidian', 'vault',
}
def read_setting(setting_name: str, repo_path: Path) -> str:
    value = os.getenv(setting_name, "").strip()
    if value:
        return value

    env_file = repo_path / ".env"
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


def get_default_devbrain_vault(repo_path: Path) -> str:
    vault = read_setting("OBSIDIAN_DEV_VAULT", repo_path)
    if vault:
        return vault

    legacy_vault = read_setting("DEVBRAIN_VAULT", repo_path)
    if legacy_vault:
        return legacy_vault

    raise ValueError(
        "Configure OBSIDIAN_DEV_VAULT no arquivo .env ou informe --vault explicitamente."
    )


def get_default_system_name(repo_path: Path) -> str | None:
    system_name = read_setting("OBSIDIAN_DEV_SYSTEM_NAME", repo_path)
    if system_name:
        return system_name

    legacy_system_name = read_setting("DEVBRAIN_SYSTEM_NAME", repo_path)
    if legacy_system_name:
        return legacy_system_name

    return None


def normalize_system_name(raw_name: str) -> str:
    normalized = " ".join(raw_name.replace("-", " ").replace("_", " ").split())
    if not normalized:
        return "Projeto"

    words = [word.capitalize() for word in normalized.split()]
    if not words or words[-1].lower() != "django":
        words.append("Django")

    return " ".join(words)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Consulta o DevBrain primeiro e faz fallback para o repositório.'
    )
    parser.add_argument('--query', required=True, help='Pergunta a ser pesquisada.')
    parser.add_argument('--vault', default=None, help='Raiz do vault DevBrain.')
    parser.add_argument(
        '--system-name',
        default=None,
        help='Nome do sistema no vault. Se omitido, usa OBSIDIAN_DEV_SYSTEM_NAME ou busca em todos os sistemas.',
    )
    parser.add_argument('--repo-path', default=str(DEFAULT_REPO_PATH), help='Raiz do repositório.')
    args = parser.parse_args()
    repo_path = Path(args.repo_path).resolve()
    if args.vault is None:
        args.vault = get_default_devbrain_vault(repo_path)
    if args.system_name is None:
        args.system_name = get_default_system_name(repo_path)
    return args


def normalize(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'\s+', ' ', text.lower()).strip()


def query_tokens(query: str) -> list[str]:
    tokens = re.findall(r'[a-zA-Z0-9_/-]+', normalize(query))
    return [token for token in tokens if token not in STOPWORDS and len(token) > 1]


def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith('#'):
            return line.lstrip('#').strip()
    return fallback


def extract_snippet(text: str, tokens: list[str]) -> str:
    normalized = normalize(text)
    for token in tokens:
        idx = normalized.find(token)
        if idx >= 0:
            start = max(0, idx - 80)
            end = min(len(text), idx + 220)
            snippet = text[start:end].replace('\n', ' ')
            return re.sub(r'\s+', ' ', snippet).strip()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines[0][:220] if lines else ''


DATE_PATTERNS = (
    re.compile(r'(?:^|[-_])(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d{4})(?:\.|[-_])'),
    re.compile(r'(?:^|[-_])(?P<day>\d{2})_(?P<month>\d{2})_(?P<year>\d{4})(?:\.|[-_])'),
    re.compile(r'(?:^|[-_])(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})(?:\.|[-_])'),
)


def dated_sort_key(path: Path) -> tuple[int, int, int, str]:
    for pattern in DATE_PATTERNS:
        match = pattern.search(path.name)
        if match:
            return (
                int(match.group('year')),
                int(match.group('month')),
                int(match.group('day')),
                path.name,
            )
    return (0, 0, 0, path.name)


def task_sort_key(path: Path) -> tuple[int, int, int, str]:
    return dated_sort_key(path)


def spec_sort_key(path: Path) -> tuple[int, int, int, str]:
    return dated_sort_key(path)


def repo_doc_roots(repo_path: Path) -> list[Path]:
    roots: list[Path] = []
    for relative in DEFAULT_REPO_DOC_ROOTS:
        candidate = repo_path / relative
        if candidate.exists():
            roots.append(candidate)
    return roots or [repo_path]


def unique_paths(paths: list[Path]) -> list[Path]:
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        unique.append(path)
    return unique


def build_vault_system_dirs(
    vault_path: Path,
    repo_path: Path,
    system_name: str | None,
) -> list[Path]:
    names: list[str] = []
    if system_name:
        names.extend([system_name, normalize_system_name(system_name)])
    else:
        inferred_names = [repo_path.name, normalize_system_name(repo_path.name)]
        names.extend(name for name in inferred_names if name)

    candidates: list[Path] = []
    for root_name in VAULT_SYSTEM_ROOTS:
        root_dir = vault_path / root_name
        for name in names:
            candidates.append(root_dir / name)

    for root_name in VAULT_SYSTEM_ROOTS:
        root_dir = vault_path / root_name
        if not root_dir.exists():
            continue
        for child in sorted(root_dir.iterdir()):
            if child.is_dir():
                candidates.append(child)

    return unique_paths(candidates)


def search_latest_markdown(
    base_dir: Path,
    kind: str,
    tokens: list[str],
    system_name: str | None = None,
) -> dict | None:
    if not base_dir.exists():
        return None
    sorter = task_sort_key if kind == 'task' else spec_sort_key
    candidates = sorted(base_dir.rglob('*.md'), key=sorter, reverse=True)
    meaningful = [token for token in tokens if token not in {'tarefa', 'task', 'spec', 'especificacao'}]
    for path in candidates:
        text = path.read_text(encoding='utf-8')
        normalized_text = normalize(text)
        normalized_path = normalize(str(path))
        if meaningful and not any(token in normalized_text or token in normalized_path for token in meaningful):
            continue
        return {
            'source_file': path,
            'system_name': system_name or base_dir.name,
            'title': first_heading(text, path.stem),
            'snippet': extract_snippet(text, meaningful or tokens),
        }
    if candidates:
        path = candidates[0]
        text = path.read_text(encoding='utf-8')
        return {
            'source_file': path,
            'system_name': system_name or base_dir.name,
            'title': first_heading(text, path.stem),
            'snippet': extract_snippet(text, tokens),
        }
    return None


def search_latest_vault_markdown(
    system_dirs: list[Path],
    relative_dirs: tuple[str, ...],
    kind: str,
    tokens: list[str],
) -> dict | None:
    for system_dir in system_dirs:
        for relative_dir in relative_dirs:
            match = search_latest_markdown(
                system_dir / relative_dir,
                kind,
                tokens,
                system_name=system_dir.name,
            )
            if match:
                return match
    return None


def search_latest_repo_markdown(repo_path: Path, relative_dirs: tuple[str, ...], kind: str, tokens: list[str]) -> dict | None:
    for root in repo_doc_roots(repo_path):
        for relative_dir in relative_dirs:
            match = search_latest_markdown(root / relative_dir, kind, tokens)
            if match:
                return match
    return None


def score_file(path: Path, text: str, tokens: list[str]) -> int:
    normalized_text = normalize(text)
    normalized_path = normalize(str(path))
    score = 0
    for token in tokens:
        if token in normalized_path:
            score += 5
        if token in normalized_text:
            score += min(3, normalized_text.count(token))
    if tokens and all(token in normalized_text or token in normalized_path for token in tokens):
        score += 10
    if 'tasks' in normalized_path:
        score += 2
    if 'specs' in normalized_path:
        score += 2
    return score


def general_search(base_dir: Path, tokens: list[str], max_results: int = 5) -> list[dict]:
    if not base_dir.exists():
        return []
    results: list[dict] = []
    for path in sorted(base_dir.rglob('*')):
        if path.is_dir() or path.suffix.lower() not in {'.md', '.py', '.toml', '.yml', '.yaml', '.json', '.http', '.txt'}:
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        score = score_file(path, text, tokens)
        if score <= 0:
            continue
        results.append({
            'source_file': path,
            'system_name': base_dir.name,
            'title': first_heading(text, path.stem),
            'snippet': extract_snippet(text, tokens),
            'score': score,
        })
    return sorted(results, key=lambda item: item['score'], reverse=True)[:max_results]


def general_vault_search(system_dirs: list[Path], tokens: list[str], max_results: int = 5) -> list[dict]:
    for system_dir in system_dirs:
        results = general_search(system_dir, tokens, max_results=max_results)
        if results:
            return results
    return []


def general_repo_search(repo_path: Path, tokens: list[str], max_results: int = 5) -> list[dict]:
    for root in repo_doc_roots(repo_path):
        results = general_search(root, tokens, max_results=max_results)
        if results:
            return results
    return general_search(repo_path, tokens, max_results=max_results)


def format_result(source: str, system_name: str, primary: dict, alternatives: list[dict]) -> str:
    lines = [
        f'Fonte: {source}',
        f'Sistema: {primary.get("system_name", system_name) or system_name}',
        f'Arquivo principal: {primary["source_file"]}',
        f'Título: {primary["title"]}',
        f'Trecho: {primary["snippet"] or "Sem trecho relevante."}',
    ]
    if alternatives:
        lines.append('Alternativas:')
        for item in alternatives:
            lines.append(f'- {item["source_file"]}')
    return '\n'.join(lines)


def main() -> int:
    args = parse_args()
    tokens = query_tokens(args.query)
    vault_path = Path(args.vault).resolve()
    repo_path = Path(args.repo_path).resolve()
    vault_system_dirs = build_vault_system_dirs(vault_path, repo_path, args.system_name)
    normalized_query = normalize(args.query)

    if 'ultima tarefa' in normalized_query or 'ultima task' in normalized_query:
        primary = search_latest_vault_markdown(
            vault_system_dirs,
            ('tasks/done',),
            'task',
            tokens,
        )
        if primary:
            print(format_result('vault', args.system_name or 'auto', primary, []))
            return 0
        primary = search_latest_repo_markdown(repo_path, ('tasks/done', 'docs/tasks/done'), 'task', tokens)
        if primary:
            print(format_result('repositório', args.system_name or 'auto', primary, []))
            return 0

    if 'ultima spec' in normalized_query or 'ultima especificacao' in normalized_query:
        primary = search_latest_vault_markdown(
            vault_system_dirs,
            ('specs/done', 'specs'),
            'spec',
            tokens,
        )
        if primary:
            print(format_result('vault', args.system_name or 'auto', primary, []))
            return 0
        primary = search_latest_repo_markdown(repo_path, ('specs', 'docs/specs'), 'spec', tokens)
        if primary:
            print(format_result('repositório', args.system_name or 'auto', primary, []))
            return 0

    vault_results = general_vault_search(vault_system_dirs, tokens)
    if vault_results:
        print(format_result('vault', args.system_name or 'auto', vault_results[0], vault_results[1:]))
        return 0

    repo_results = general_repo_search(repo_path, tokens)
    if repo_results:
        print(format_result('repositório', args.system_name or 'auto', repo_results[0], repo_results[1:]))
        return 0

    print(
        f'Fonte: nenhuma\nSistema: {args.system_name or "auto"}\n'
        'Mensagem: nenhuma evidência encontrada no vault ou no repositório.'
    )
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
