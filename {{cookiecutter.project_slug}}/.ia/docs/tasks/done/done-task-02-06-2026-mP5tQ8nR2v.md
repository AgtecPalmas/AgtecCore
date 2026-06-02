# Tarefa: Adicionar prompts interativos para install, git init e build apps no generate_project.py

## 1. Metadados

- ID da task: `task-02-06-2026-mP5tQ8nR2v`
- Status da task: `done`
- Prioridade: `high`
- Tipo: `bugfix`
- Modulo/area: `tooling / generate_project.py`
- Responsavel: `equipe de produto`
- Solicitante: `equipe de produto`
- Data de criacao: `02-06-2026`
- Ultima atualizacao: `02-06-2026`

## 2. Referencias

- Spec/PRD: `não se aplica`
- TechSpec: `não se aplica`
- Task relacionada: `done-task-02-06-2026-hK9wZ3rX1n` (criação do generate_project.py)
- Board/issue externa: `não se aplica`
- Fontes consultadas:
  - `generate_project.py`
  - `hooks/post_gen_project.py`
  - `cookiecutter.json`
  - `tests/test_generate_project.py`

## 3. Contexto

O CookieCutter perguntava ao usuário, de forma interativa, três perguntas antes de iniciar o processo de geração:

| Pergunta CookieCutter | Campo `cookiecutter.json` | Default |
|---|---|---|
| "Instalar requirements?" | `install_requirements` | `Sim` |
| "Iniciar o git?" | `git_init` | `Sim` |
| "Construir apps padrões?" | `build_apps` | `Sim` |

O `generate_project.py` substituiu esse fluxo mas não replicou as perguntas interativas. As três etapas são controladas apenas via flags CLI (`--no-install`, `--no-git`, `--no-build-apps`). Usuários que executam o script sem flags têm as três etapas executadas automaticamente, sem oportunidade de recusar — comportamento diferente do CookieCutter.

O problema foi identificado em teste real de geração de projeto pela equipe de produto.

### Comportamento atual

```
── AgtecCore — Novo Projeto ─────────────────────────────────
  Nome do projeto [Projeto Base]: Meu Sistema
  ...
  Confirmar geração? [S/n]: S
── Copiando template ...
── Pós-geração ...
  ✅ .env criado com SECRET_KEY gerada
  ⏳ Instalando dependências via uv sync...   ← executa sem perguntar
  ✅ Dependências instaladas
  ⏳ Construindo app: usuario               ← executa sem perguntar
  ⏳ Construindo app: configuracao_core     ← executa sem perguntar
  ✅ Inicializando git...                   ← executa sem perguntar
```

### Comportamento esperado (replicando CookieCutter)

```
── AgtecCore — Novo Projeto ─────────────────────────────────
  Nome do projeto [Projeto Base]: Meu Sistema
  ...
  Instalar dependências? [S/n]: S
  Construir apps padrões? [S/n]: S
  Inicializar git? [S/n]: S
  Confirmar geração? [S/n]: S
```

## 4. Objetivo

Adicionar três prompts interativos na fase de coleta de inputs (`_build_context`) para replicar o comportamento original do CookieCutter, mantendo as flags CLI como forma de pular os prompts em uso automatizado/não-interativo.

## 5. Escopo

- Inclui:
  - Adicionar prompts interativos `ask_bool()` em `_build_context` para `install_requirements`, `git_init` e `build_apps`
  - As flags `--no-install`, `--no-git`, `--no-build-apps` devem continuar funcionando (ignoram o prompt)
  - Propagar os valores coletados até as chamadas em `main()`
  - Atualizar testes para cobrir os novos prompts
- Nao inclui:
  - Alterar a lógica de instalação, git ou build em si
  - Alterar o template `{{cookiecutter.project_slug}}/`

## 6. Criterios de aceite

1. Executar `python generate_project.py` sem flags exibe os três prompts na ordem: instalar deps → construir apps → inicializar git
2. Responder `n` em qualquer prompt pula a etapa correspondente
3. Flags `--no-install`, `--no-git`, `--no-build-apps` continuam pulando a etapa sem exibir o prompt
4. Default de cada prompt é `S` (equivalente ao CookieCutter)
5. Testes unitários cobrem os novos prompts (mock de `input`)

## 7. Restricoes e premissas

- Restricoes:
  - Não quebrar uso automatizado via flags CLI
  - Manter assinatura de `_build_context(args)` — o retorno pode ser ampliado, mas não renomeado
- Premissas:
  - A ordem dos prompts deve seguir a lógica de dependência: instalar deps → construir apps (depende de deps) → git

## 8. Impacto esperado

- Backend/API: `não`
- Banco de dados: `não`
- Integracoes: `não`
- Seguranca/LGPD: `não`
- Testes: `sim — atualizar testes de _build_context e main()`
- Documentacao: `sim — atualizar README.md (seção flags opcionais)`

## 9. Plano de execucao

1. Criar função auxiliar `ask_bool(prompt, default=True) -> bool` em `generate_project.py`
2. Em `_build_context`, adicionar os três prompts após a coleta de dados do projeto (somente se a flag correspondente não foi passada)
3. Retornar `install_requirements`, `git_init` e `build_apps` como booleanos no dict de contexto
4. Em `main()`, substituir `args.no_install`, `args.no_git`, `args.no_build_apps` pelos valores do contexto
5. Atualizar testes: mock de `input` para cobrir respostas `S` e `N` nos novos prompts
6. Atualizar README.md: ajustar descrição das flags

## 10. Controle de implementacao

- Branch base da implementacao: `dev`
- Branch de implementacao: `task-02-06-2026-mP5tQ8nR2v`
- Skills usadas: `workflow-demandas`
- Arquivos previstos:
  - `generate_project.py`
  - `tests/test_generate_project.py`
  - `README.md`
- Status de aprovacao: `approved`
- Execucao de testes: `executada`
- Comandos executados:
  - `rtk python3 -m pytest tests/test_generate_project.py -q`

## 11. Evidencias

- Resultado de testes:
  - `53 passed, 0 failed` — suite completa executada com sucesso
- Logs, screenshots ou observacoes:
  - 9 testes novos adicionados cobrindo ask_bool, flags, interação TTY e combinações

## 12. Definition of Done

- [ ] Implementacao concluida
- [ ] Criterios de aceite atendidos
- [ ] Testes executados ou justificativa registrada
- [ ] Documentacao atualizada
- [ ] Riscos e trade-offs registrados

## 13. Fechamento

- Riscos residuais:
  - Em uso CI/CD (sem TTY), `input()` pode travar — mitigar detectando ambiente não-interativo e caindo no default automaticamente
- Proximos passos:
  - Aprovação desta task pelo desenvolvedor responsável
  - Abertura de branch via `branch-task-aprovada`

## Descricao da solucao implementada

Adicionada função `ask_bool(prompt, default=True)` dentro de `_build_context`. A função detecta ambiente não-interativo via `sys.stdin.isatty()` e retorna o default sem chamar `input()` — garantindo compatibilidade com CI/CD. Em ambiente interativo, exibe o prompt e aceita variações de "s/sim/y/yes". Os três prompts são exibidos na ordem correta (instalar deps → construir apps → git), com a regra de dependência: `build_apps` só é perguntado se `install_requirements` for True. As flags `--no-install`, `--no-git`, `--no-build-apps` continuam funcionando e ignoram os prompts. O `main()` foi atualizado para consumir os valores do contexto em vez das flags diretamente.

## Trade-offs

- **ask_bool dentro de _build_context vs. função de módulo**: mantida como função aninhada para evitar poluir o namespace do módulo com uma helper de uso único.
- **isatty() para detectar CI**: abordagem padrão e sem dependências; alternativa seria variável de ambiente `CI=true`, mas isatty() cobre mais casos automaticamente.
- **build_apps depende de install_requirements**: decisão explícita — construir apps sem dependências instaladas geraria erro silencioso; a dependência é modelada no código, não apenas documentada.

## Arquivos alterados

- `generate_project.py` — `_build_context` com `ask_bool` e três prompts; `main()` consome ctx em vez de args
- `tests/test_generate_project.py` — 9 novos testes em `TestBoolPrompts`; `_make_args` atualizado com `no_install`, `no_git`, `no_build_apps`
