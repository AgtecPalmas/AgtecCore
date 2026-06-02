# Tarefa: Substituir CookieCutter por script Python 3.12 puro para geração de projetos AgtecCore

## 1. Metadados

- ID da task: `task-02-06-2026-hK9wZ3rX1n`
- Status da task: `done`
- Prioridade: `medium`
- Tipo: `refactor`
- Modulo/area: `tooling / geração de projetos`
- Responsavel: `equipe de produto`
- Solicitante: `equipe de produto`
- Data de criacao: `02-06-2026`
- Ultima atualizacao: `02-06-2026`

## 2. Referencias

- Spec/PRD: `não se aplica`
- TechSpec: `não se aplica`
- Task relacionada: `não se aplica`
- Board/issue externa: `não se aplica`
- Fontes consultadas:
  - `cookiecutter.json`
  - `hooks/pre_gen_project.py`
  - `hooks/post_gen_project.py`
  - `{{cookiecutter.project_slug}}/base/settings.py`
  - `{{cookiecutter.project_slug}}/.env.example`
  - `{{cookiecutter.project_slug}}/pyproject.toml`
  - `{{cookiecutter.project_slug}}/docker-compose.yml`

## 3. Contexto

O AgtecCore usa o CookieCutter para gerar projetos Django a partir do template em `{{cookiecutter.project_slug}}/`. O fluxo atual depende do CookieCutter CLI, do `cookiecutter.json` como manifesto de variáveis e dos hooks `pre_gen_project.py` / `post_gen_project.py` para pós-processamento (instalação de deps, git init, cópia de arquivos, geração de SECRET_KEY).

A equipe de produto identificou que a arquitetura base já é estável o suficiente para que o processo de geração seja controlado por um script Python 3.12 puro, eliminando a dependência do CookieCutter e permitindo maior customização, manutenção e extensibilidade do processo de scaffolding.

### Levantamento técnico realizado

**Variáveis do `cookiecutter.json` (14 campos de entrada + 3 opções booleanas):**

| Variável | Derivada? | Observação |
|---|---|---|
| `project_name` | Não | Input principal |
| `project_slug` | Sim | `slugify(project_name).replace('-','_')` |
| `main_app` | Sim | igual a `project_slug` |
| `client_name` | Não | Input |
| `docker_port` | Não | Default `8000` |
| `postgre_port` | Não | Default `5432` |
| `created_date_project` | Sim | `datetime.now()` |
| `description` | Não | Input |
| `author_name` | Não | Input |
| `domain_name` | Não | Input |
| `email` | Não | Input |
| `flutter_organization_name` | Não | Input |
| `flutter_organization_domain` | Sim | `'.'.join(reversed(domain_name.split('.')))` |
| `django_version` | Não | Default `5.2.12` |
| `python_version` | Não | Default `3.12.*` |
| `postgresql_version` | Não | Default `14.2` |
| `drf_version` | Não | Default `3.16.1` |
| `install_requirements` | Não | Bool, default `True` |
| `git_init` | Não | Bool, default `True` |
| `build_apps` | Não | Bool, default `True` |

**Arquivos com `{{ cookiecutter.* }}` no template:**
- `base/settings.py`, `base/asgi.py`, `base/wsgi.py`, `base/urls.py`, `base/elastic.py`
- `.env.example`, `pyproject.toml`, `docker-compose.yml`, `dev.docker-compose.yml`
- `manage.py` (via `base/__init__.py`)

**Lógica dos hooks atual:**
- `pre_gen_project.py`: atualiza portas aleatórias no `cookiecutter.json` (workaround para conflitos)
- `post_gen_project.py`: copia arquivos para raiz do destino, cria `.env` a partir de `.env.example`, gera `SECRET_KEY`, instala deps via `uv sync`, executa `python manage.py build <app>` para apps padrão, inicializa git

**Diretórios com `_copy_without_render` (copiados sem renderização):**
- `core/`, `usuario/`, `atendimento/`, `configuracao_core/`, `contrib/`, `docs/`

## 4. Objetivo

Criar um script `generate_project.py` (Python 3.12, stdlib + dependências mínimas) que replique integralmente o processo de geração de projetos hoje feito pelo CookieCutter, eliminando a dependência do CookieCutter CLI.

## 5. Escopo

- Inclui:
  - Script `generate_project.py` na raiz do AgtecCore
  - Coleta interativa de inputs (CLI via `argparse` ou prompt simples)
  - Renderização de templates com `string.Template` ou `jinja2` (manter Jinja2 pois já é dep do Django)
  - Cópia da árvore do template com controle de `copy_without_render`
  - Geração de `SECRET_KEY` via `contrib/secret_gen.py`
  - Cópia de `.env.example` → `.env` com SECRET_KEY substituída
  - Instalação de dependências via `uv sync` (opcional)
  - `git init` + commits iniciais (opcional)
  - Build de apps padrão via `manage.py build` (opcional)
  - Testes do script via `pytest` (unitários para renderização + integração para fluxo completo)
  - Atualização do `README.md` do AgtecCore com novo fluxo de uso
- Nao inclui:
  - Remoção imediata do CookieCutter (manter em paralelo até validação)
  - Suporte a múltiplos templates (escopo é exclusivamente o AgtecCore)
  - Interface gráfica ou TUI
  - Migração de projetos já gerados

## 6. Criterios de aceite

1. `python generate_project.py` gera um projeto Django funcional idêntico ao gerado pelo CookieCutter, com todas as variáveis substituídas corretamente
2. Arquivos nos diretórios `_copy_without_render` são copiados sem nenhuma substituição de variável
3. `.env` é criado a partir de `.env.example` com `SECRET_KEY` única gerada
4. Flag `--no-install`, `--no-git`, `--no-build-apps` desativam as etapas opcionais
5. Suite de testes passa com `rtk pytest` sem erros
6. `README.md` atualizado documenta o novo fluxo de uso

## 7. Restricoes e premissas

- Restricoes:
  - Python 3.12 obrigatório (sem backports)
  - Não adicionar dependências novas além das já presentes no `pyproject.toml` do AgtecCore
  - Jinja2 pode ser usado (já é dependência transitiva do Django) — preferir `string.Template` se a complexidade das vars permitir
  - CookieCutter deve permanecer funcional durante a transição (não remover até validação pelo time)
  - O script NÃO deve modificar arquivos dentro de `core/` (restrição do AGENTS.md §8.1)
- Premissas:
  - O template em `{{cookiecutter.project_slug}}/` é a fonte canônica e não será alterado nesta task
  - `uv` está disponível no PATH do ambiente onde o script será executado
  - O time validará o projeto gerado pelo script antes de deprecar o CookieCutter

## 8. Impacto esperado

- Backend/API: `não — script de tooling externo ao projeto Django gerado`
- Banco de dados: `não`
- Integracoes: `não`
- Seguranca/LGPD: `sim — geração de SECRET_KEY deve usar entropia adequada (secrets module)`
- Testes: `sim — testes unitários e de integração para o script`
- Documentacao: `sim — README.md do AgtecCore e potencialmente AGENTS.md`

## 9. Plano de execucao

1. Definir estrutura do script: módulos `context.py` (coleta de inputs), `renderer.py` (renderização), `scaffold.py` (cópia de arquivos), `post_gen.py` (secret, git, deps, build)
2. Implementar coleta interativa de contexto com validações e defaults
3. Implementar renderização Jinja2 respeitando `copy_without_render`
4. Implementar pós-geração: SECRET_KEY, .env, uv sync, git init, build apps
5. Adicionar CLI com `argparse` (flags opcionais para etapas)
6. Escrever testes: unitários para renderização + integração (gera projeto em tmpdir e valida)
7. Atualizar README.md do AgtecCore
8. Validação manual: gerar projeto real e comparar com saída do CookieCutter

## 10. Controle de implementacao

- Branch base da implementacao: `dev`
- Branch de implementacao: `task-02-06-2026-hK9wZ3rX1n`
- Skills usadas: `workflow-demandas`
- Arquivos previstos:
  - `generate_project.py` (raiz do AgtecCore)
  - `tests/test_generate_project.py`
  - `README.md` (atualização)
- Status de aprovacao: `approved`
- Execucao de testes: `executada`
- Comandos executados:
  - `rtk python3 -m pytest tests/test_generate_project.py -v`

## 11. Evidencias

- Resultado de testes:
  - `40 passed, 0 failed` — suite completa executada com sucesso
- Logs, screenshots ou observacoes:
  - Governança: 4 findings pré-existentes (task de exemplo + spec sem metadados), nenhum criado por esta task

## 12. Definition of Done

- [ ] Implementacao concluida
- [ ] Criterios de aceite atendidos
- [ ] Testes executados ou justificativa registrada
- [ ] Documentacao atualizada
- [ ] Riscos e trade-offs registrados

## 13. Fechamento

- Riscos residuais:
  - Divergência entre projeto gerado pelo script vs CookieCutter se algum template usar sintaxe CookieCutter não mapeada
  - Lógica de portas aleatórias do `pre_gen_project.py` (workaround legado) precisa ser avaliada — pode ser simplificada ou removida
- Proximos passos:
  - Aprovação desta task pelo desenvolvedor responsável
  - Abertura de branch via `branch-task-aprovada`
  - Implementação do script conforme plano de execução (§9)

## Descricao da solucao implementada

Script `generate_project.py` (Python 3.12, ~220 linhas) criado na raiz do AgtecCore para substituir o CookieCutter. O script usa Jinja2 (já disponível como dep transitiva do Django) para renderizar os arquivos do template `{{cookiecutter.project_slug}}/`, respeitando a lista `COPY_WITHOUT_RENDER` (core/, usuario/, contrib/, docs/, etc.). Coleta inputs via prompts interativos ou flags `--project-name`, `--client-name`, etc. Realiza pós-geração: cria `.env` a partir de `.env.example` com `SECRET_KEY` única, instala dependências via `uv sync` (desativável com `--no-install`), inicializa git (desativável com `--no-git`) e constrói apps padrão via `manage.py build` (desativável com `--no-build-apps`). Suite de 40 testes unitários e de integração cobrindo todas as funções principais.

## Trade-offs

- **Jinja2 vs string.Template**: optado por Jinja2 porque os templates já usam sintaxe Jinja2 com filtros (`| default()`), chamadas de método (`.lower()`, `.title()`) e variáveis aninhadas — string.Template não suportaria essa complexidade sem reescrever todos os templates.
- **Script único vs módulos**: mantido como arquivo único para reduzir fricção de manutenção; a lógica tem complexidade baixa o suficiente para não justificar pacote separado.
- **CookieCutter mantido em paralelo**: decisão consciente — o script coexiste com o fluxo CookieCutter para permitir validação comparativa antes da deprecação definitiva.
- **Governance findings pré-existentes**: o check de governança retornou 4 findings, todos pré-existentes (task de exemplo e spec sem metadados), não gerados por esta task.

## Arquivos alterados

- `generate_project.py` — criado (script principal)
- `tests/__init__.py` — criado (init do pacote de testes)
- `tests/test_generate_project.py` — criado (40 testes)
- `README.md` — atualizado (nova seção "Gerando um novo projeto" com Opção 1 e Opção 2)
