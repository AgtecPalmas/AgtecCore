# Pacote `.ia/`

Diretório central de governança de IA do projeto. Contém skills, documentação arquitetural, tasks assistidas e scripts de automação. Regras operacionais estão em `AGENTS.md` (raiz do projeto) — este `.ia/` é copiado para cada projeto gerado pelo template.

## Estrutura

```
.ia/
├── docs/
│   ├── architecture/        # overview, system-architecture, modules, security
│   ├── guides/              # constraints, patterns, testing, commits, feature, agent-tooling
│   ├── reports/             # relatórios gerados por skills (ex.: análise de governança)
│   ├── specs/               # specs técnicas (raiz = em andamento; done/ = concluídas; fastapi/ = camada FastAPI)
│   ├── tasks/               # todo/ e done/
│   └── templates/           # task-template.md, spec-template.md, prd-template.md, feature-prompt-template.md
└── skills/                  # skills internas (ver tabela abaixo)
```

> **Nota**: stack/contexto canônico do projeto gerado em `.ia/docs/architecture/overview.md`.

---

## Configuração do ambiente de desenvolvimento assistido por IA

Esta seção descreve como preparar o ambiente em um projeto gerado pelo template. Execute os passos na ordem apresentada.

### 1. Instalar o OpenCode

OpenCode é o ambiente de terminal com IA que orquestra os agentes neste projeto.

```bash
# macOS / Linux (recomendado)
curl -fsSL https://opencode.ai/install | bash

# Homebrew
brew install anomalyco/tap/opencode

# npm
npm install -g opencode-ai
```

Após a instalação, inicialize na raiz do repositório:

```bash
cd /caminho/do/projeto
opencode
```

Dentro da sessão OpenCode, execute `/init` para que o agente analise o repositório e registre o `AGENTS.md` existente como contexto ativo.

> Documentação completa: https://opencode.ai/docs

---

### 2. Instalar o RTK

RTK (Rust Token Killer) intercepta comandos shell e os reescreve para versões filtradas, reduzindo 60–90% do consumo de tokens em operações de dev.

```bash
# Homebrew (recomendado)
brew install rtk

# Linux / macOS via script
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
```

Verificar instalação:

```bash
rtk --version
rtk gain
```

Integrar ao OpenCode (cria hook de interceptação):

```bash
rtk init -g --opencode
```

> Repositório: https://github.com/rtk-ai/rtk

---

### 3. Instalar o Caveman

Caveman ativa o modo de comunicação comprimido nos agentes de IA, reduzindo ~75% dos tokens de saída sem perda de precisão técnica.

```bash
# macOS / Linux / WSL
curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash
```

O instalador detecta automaticamente os agentes presentes (Claude Code, OpenCode, Codex) e implanta os hooks necessários em cada um.

Modos disponíveis após instalação: `/caveman lite`, `/caveman full` (padrão), `/caveman ultra`.

> Repositório: https://github.com/JuliusBrussee/caveman

---

### 4. Configurar o Obsidian Brain (memória persistente)

O Obsidian Brain integra o agente com um vault Obsidian, permitindo armazenar e consultar contexto de forma persistente entre sessões.

1. Instale o Obsidian: https://obsidian.md/download
2. Crie um vault chamado `DevBrain` (ou nome de sua preferência).
3. Configure a variável de ambiente no projeto:

```bash
OBSIDIAN_DEV_VAULT="CAMINHO_PARA_SEU_VAULT/DevBrain"
```

Após configurar, use as skills `obsidian-sync` para exportar contexto do repositório para o vault e `obsidian-query` para consultar histórico e specs.

---

### 5. Executar o onboarding inicial do projeto

Após a configuração do ambiente, o primeiro procedimento recomendado é o checklist de validação do projeto gerado:

```
Execute a skill django-onboarding-checklist para validar o projeto gerado.
```

O agente verificará `INSTALLED_APPS`, `AUTH_USER_MODEL`, migrations, variáveis de ambiente e conexão com banco antes de qualquer demanda de desenvolvimento.

---

## Como escrever prompts para desenvolvimento assistido por IA

A qualidade do resultado entregue pelo agente é diretamente proporcional à qualidade do prompt. Um prompt ruim gera código genérico, ignora a arquitetura do projeto e exige retrabalho. Um prompt bem escrito ativa o contexto correto, respeita o fluxo de tasks e produz código alinhado ao padrão real do repositório.

---

### Prompt ruim — o que evitar

```
Faça um módulo de login com o govBR
```

**Por que é ruim:**

| Problema | Consequência |
|---|---|
| Sem contexto de origem | Agente não sabe se é feature nova, bugfix ou refactor — não cria task |
| Sem referência à arquitetura | Agente pode criar views com lógica de negócio, ignorar dj-rest-auth, não usar SimpleJWT |
| Sem escopo definido | Agente decide sozinho quais apps, camadas e arquivos tocar |
| Sem pedido de planejamento | Agente vai direto para código sem plano de ação ou critérios de aceite |
| Sem referência à documentação externa | Agente infere o protocolo govBR do próprio treinamento, que pode estar desatualizado |
| Verbo imperativo direto | Induz o agente a implementar antes de entender — viola o fluxo de task deste projeto |

---

### Prompt correto — o que fazer

```
Recebemos da equipe de produto uma demanda de implementarmos o login do usuário
integrado com a plataforma de SSO govBR. Leia a documentação oficial do govBR em
https://login.gov.br/documentacao para entender o fluxo OAuth2/OIDC utilizado
e siga as regras de AGENTS.md.

Crie o planejamento da demanda com as camadas impactadas (models, serializers,
views, testes), os critérios de aceite e as skills a usar. Não implemente até a aprovação.
```

**Por que é correto:**

| Elemento | Função |
|---|---|
| Origem da demanda declarada | Agente entende o contexto de negócio sem precisar inferir |
| Leitura de documentação externa antes do código | Garante que o protocolo real (OAuth2/OIDC do govBR) seja respeitado |
| Referência explícita a `AGENTS.md` | Agente ancora a implementação na arquitetura de autenticação existente |
| Pedido de planejamento com task | Ativa o fluxo de `workflow-demandas` e cria rastreabilidade |
| Camadas listadas explicitamente | Agente carrega as skills corretas antes de implementar |
| "Não implemente até a aprovação" | Preserva o ciclo de revisão humana — agente não avança sozinho |

---

### Anatomia de um prompt bem escrito

```
[ORIGEM]
De onde veio a demanda (produto, cliente, bug reportado, débito técnico).

[OBJETIVO]
O que precisa ser verdade ao final — em termos de comportamento, não de código.

[REFERÊNCIAS]
- Documentação externa relevante (URLs)
- Arquivos internos a consultar primeiro (.ia/docs/*, AGENTS.md)

[RESTRIÇÕES]
Camadas que não devem ser tocadas, compatibilidade necessária, prazo, LGPD.

[INSTRUÇÃO DE FLUXO]
"Crie o planejamento e aguarde aprovação antes de implementar."
ou
"Task já aprovada em .ia/docs/tasks/todo/<hash>.md — execute a implementação."
```

---

### Exemplos adicionais

**Ruim:**
```
Adiciona paginação nas listagens
```

**Correto:**
```
O time de produto identificou que endpoints de listagem estão retornando todos os
registros sem paginação, causando timeout em produção no app `atendimento`.

Consulte AGENTS.md para entender o padrão adotado. Crie o planejamento da demanda
com as camadas impactadas (views, serializers, testes) e os critérios de aceite
antes de implementar.
```

---

**Ruim:**
```
Refatora o app financeiro
```

**Correto:**
```
O app `financeiro` acumula N+1 identificados em code review na semana passada.
As queries problemáticas estão em `financeiro/api/views/conta.py` e
`financeiro/managers.py`. Siga as regras de AGENTS.md — crie uma task com
escopo, plano de ação e critérios de aceite antes de qualquer alteração.
```

---

> **Regra geral:** o agente executa melhor quando recebe _contexto_, _restrições_ e _ordem de operações_ — não apenas _o que fazer_. Quanto mais o prompt se parece com um briefing técnico, menos retrabalho haverá.

---

## Workflows documentais

- **Datas de governança**: metadados documentais e nomes de novos artefatos usam `DD-MM-YYYY`.
- **Tasks** (`docs/tasks/`): unidade de execução. Ciclo `planned → approved → in_progress → in_review → blocked → done/cancelled`. Regras em `AGENTS.md` §5.
- O campo canônico de lifecycle da task é `Status da task` em `## 1. Metadados`; `Controle de implementacao` registra aprovação, branch e validações operacionais. Novas tasks usam `task-DD-MM-YYYY-<hash_alfanumerico_10>.md`; concluídas usam `done-task-DD-MM-YYYY-<hash_alfanumerico_10>.md`; a branch usa o nome do arquivo sem `.md`.
- **Specs técnicas** (`docs/specs/`): design upfront para mudanças amplas, integrações e refatorações multi-app. Uma spec gera N tasks derivadas. Specs Django usam `<dominio>-<descricao-curta>-spec-DD-MM-YYYY.md`; specs FastAPI usam `<dominio>-<descricao-curta>-fastapi-spec-DD-MM-YYYY.md`; status válidos são `draft`, `approved`, `in_progress`, `in_review`, `done`, `cancelled`, `superseded`. Regras em `AGENTS.md` §6.
- **Relatórios** (`docs/reports/`): saída de scripts de skills (análise de governança, conformidade etc). Novos reports usam `DD-MM-YYYY-<descricao-curta>.md` e `Status do relatorio` em `draft`, `in_review`, `done` ou `superseded`.
- **Templates** (`docs/templates/`): `task-template.md`, `spec-template.md`, `prd-template.md`, `feature-prompt-template.md`.

### Quando usar cada artefato de planejamento

| Artefato | Localização | Para quê | Quando usar |
| --- | --- | --- | --- |
| `task-template.md` | `docs/templates/` | Unidade de execução (uma demanda concreta, escopo delimitado) | Toda demanda assistida por IA (§5 do `AGENTS.md`) |
| `spec-template.md` | `docs/templates/` | Design técnico upfront com AS-IS/TO-BE, contratos, ordem de implementação | Mudança ampla, integração externa, refatoração multi-app (§6) |
| `prd-template.md` | `docs/templates/` | PRD completo de produto (problema, escopo, métricas, release plan) | Funcionalidade nova com discussão de produto antes da spec técnica |
| `feature-prompt-template.md` | `docs/templates/` | Prompt-template curto para pedir feature Django ao agente | Quando o desenvolvedor quer um prompt pronto para uma feature concreta |

---

## Como os agentes usam este contexto

O ponto de entrada para qualquer agente é o arquivo `AGENTS.md` na raiz do repositório. Ele define:

1. **Idioma e stack** — resposta em português, Django + DRF, PostgreSQL.
2. **Fontes de verdade** — lista explícita de quais arquivos de `.ia/docs/` prevalecem sobre qualquer outra instrução.
3. **Catálogo de skills** — quais skills existem e onde encontrá-las.
4. **Fluxo de tasks** — como criar, executar, aprovar e encerrar uma demanda rastreável.
5. **Comandos de build** — uv sync, migrate, runserver, lint, pytest — todos com prefixo `rtk`.
6. **Proibições de segurança** — `git commit/push/rebase/pull` nunca são executados pela IA.

**Regra de precedência:** `AGENTS.md` é o ponto de entrada; em caso de conflito, os arquivos de `.ia/docs/` prevalecem.

---

## Skills

### Skills disponíveis

| Skill | Caminho | Resumo |
| --- | --- | --- |
| `branch-task-aprovada` | `.ia/skills/branch-task-aprovada/SKILL.md` | Cria branch de implementação a partir de task aprovada. |
| `django-onboarding-checklist` | `.ia/skills/django-onboarding-checklist/SKILL.md` | Checklist de validação inicial de projeto gerado pelo template. |
| `django-api-serializers` | `.ia/skills/django-api-serializers/SKILL.md` | Serializers DRF. |
| `django-api-views` | `.ia/skills/django-api-views/SKILL.md` | ViewSets/CBVs DRF e roteamento. |
| `django-celery-tasks` | `.ia/skills/django-celery-tasks/SKILL.md` | Tarefas assíncronas Celery — aplicar quando Celery estiver instalado na stack. |
| `django-managers` | `.ia/skills/django-managers/SKILL.md` | QuerySets e managers customizados. |
| `django-migrations` | `.ia/skills/django-migrations/SKILL.md` | Planejamento e revisão de migrations. |
| `django-models` | `.ia/skills/django-models/SKILL.md` | Modelos ORM. |
| `django-services-use-cases` | `.ia/skills/django-services-use-cases/SKILL.md` | Regras de negócio em `services.py`/`use_cases.py`. |
| `django-tests-pytest` | `.ia/skills/django-tests-pytest/SKILL.md` | Testes pytest/pytest-django. |
| `fastapi-especificacao-tecnica` | `.ia/skills/fastapi-especificacao-tecnica/SKILL.md` | Spec técnica para a camada FastAPI. |
| `governanca-compliance` | `.ia/skills/governanca-compliance/SKILL.md` | Auditoria de governança documental de `AGENTS.md` + `.ia/`. |
| `merge-com-dev` | `.ia/skills/merge-com-dev/SKILL.md` | Merge de branch de task para `dev`. |
| `obsidian-query` | `.ia/skills/obsidian-query/SKILL.md` | Consulta ao vault DevBrain (vault → repo fallback). |
| `obsidian-sync` | `.ia/skills/obsidian-sync/SKILL.md` | Sincronização do repositório com o vault DevBrain. |
| `task-encerramento` | `.ia/skills/task-encerramento/SKILL.md` | Encerra task e move `todo/` → `done/`. |
| `workflow-demandas` | `.ia/skills/workflow-demandas/SKILL.md` | Orquestra ciclo de task assistida por IA. |

**Total: 16 skills**

### Scripts de automação

| Script | Skill | Propósito |
| --- | --- | --- |
| `.ia/skills/branch-task-aprovada/create_task_implementation_branch.py` | `branch-task-aprovada` | Cria branch a partir do nome do arquivo da task. |
| `.ia/skills/task-encerramento/close_task_and_move_to_done.py` | `task-encerramento` | Valida status final e move task para `done/`. |
| `.ia/skills/merge-com-dev/merge_task_branch_with_dev.py` | `merge-com-dev` | Merge da branch atual para `dev` com `--dry-run` opcional; unica excecao permitida para efetivar merge via automacao da IA. |
| `.ia/skills/governanca-compliance/check_ia_governance.py` | `governanca-compliance` | Auditoria automatizada de `AGENTS.md` + `.ia/`. |
| `.ia/skills/obsidian-query/query_devbrain.py` | `obsidian-query` | Consulta o vault DevBrain e faz fallback para o repositório quando necessário. |
| `.ia/skills/obsidian-sync/export_devbrain.py` | `obsidian-sync` | Exporta contexto do repositório para o vault DevBrain. |

---

## Documentação arquitetural

| Arquivo | Conteúdo canônico |
|---|---|
| `overview.md` | Stack resumida, objetivos arquiteturais e regras gerais de qualidade |
| `system-architecture.md` | Mapa amplo do sistema: catálogo de apps, camadas, fluxos principais, integrações |
| `modules.md` | Estrutura interna esperada de cada app Django (models, managers, api/, services, tasks) e regras de acoplamento |
| `security.md` | Autenticação, autorização por endpoint, proteção de dados, LGPD, logs sem PII |

---

## Gestão de tarefas

- Backlog em `.ia/docs/tasks/todo/`.
- Concluídas em `.ia/docs/tasks/done/` com prefixo `done-`.
- Template em `.ia/docs/templates/task-template.md`.
- Regras completas em `AGENTS.md` §5.

---

## Regras de manutenção deste diretório

1. **Não duplicar conteúdo entre arquivos.** Cada regra tem uma fonte canônica. Se uma informação já existe em outro arquivo, aponte para ele.
2. **Não fixar versão de dependências em texto corrido.** Fonte de verdade para versões: `pyproject.toml` e `settings.py`.
3. **Manter `AGENTS.md` focado em regras operacionais.** Detalhes de arquitetura ficam em `.ia/docs/`; `AGENTS.md` é apenas o ponto de entrada.
4. **Toda mudança em `.ia/` que envolva múltiplos arquivos deve ter task rastreável** em `tasks/todo/` antes de ser executada.
5. **Scripts Python em `.ia/skills/` não devem ser alterados pela IA sem instrução explícita** do desenvolvedor.
