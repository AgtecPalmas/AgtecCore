# Checklist de Referência — Análise de Arquitetura de Projeto Legado (Django + PostgreSQL)

> **Uso:** este documento é o **checklist de referência** que respalda a skill `django-analise-arquitetura-legado`. Ele **não substitui** o script `analyze_legacy_project.py` — complementa.
>
> - Etapas **1, 2, 4, 5 (parcial), 6 (parcial), 7 (parcial) e 8 (parcial)** já são executadas pelo script. O agente revisa o relatório gerado em `.ia/docs/reports/`.
> - Etapas **3 (domínio de negócio), partes qualitativas de 5–8** dependem de julgamento e não foram automatizadas. Continuam manuais e usam este checklist como guia.
> - Etapa **9** continua manual — o agente sintetiza o relatório nos quatro arquivos canônicos.
>
> **Princípio:** Explícito é melhor que implícito. O agente deve declarar tudo que encontrou, tudo que não encontrou e tudo que assumiu — nunca inferir silenciosamente.

---

## Contexto obrigatório

- Siga rigorosamente `AGENTS.md`
- Respeite as restrições em `.ia/docs/guides/constraints.md`
- Esta é uma tarefa de **leitura e documentação** — nenhum arquivo de código deve ser criado ou alterado
- Toda premissa que não puder ser confirmada com leitura direta de arquivo deve ser declarada explicitamente como premissa, não como fato

---

## Objetivo

Realizar a leitura completa do projeto Django legado e produzir os documentos de arquitetura em `.ia/docs/architecture/`, de forma que o time e os agentes de IA tenham contexto suficiente para atuar no repositório com segurança.

---

## Restrições

- **Não criar, alterar ou deletar nenhum arquivo de código-fonte do projeto** (`.py`, migrations, templates, static)
- Não executar `manage.py` nem nenhum comando que altere estado do banco ou do ambiente
- Não instalar dependências
- Se um arquivo não existir, declarar ausência — não inventar conteúdo
- Se houver ambiguidade entre dois arquivos ou padrões conflitantes, declarar o conflito — não escolher silenciosamente

---

## Etapa 1 — Leitura do ambiente e dependências

Leia os seguintes arquivos na ordem indicada e registre o que encontrou:

1. `pyproject.toml` ou `requirements.txt` ou `requirements/*.txt` (todos que existirem)
   - Versão do Python
   - Versão do Django
   - Versão do DRF (se presente)
   - Dependências de autenticação (`dj-rest-auth`, `djangorestframework-simplejwt`, `django-allauth`, etc.)
   - Dependências de fila/cache (`celery`, `redis`, `django-celery-results`, etc.)
   - Dependências de busca (`elasticsearch-dsl`, `whoosh`, etc.)
   - Dependências de observabilidade (`sentry-sdk`, `loguru`, `structlog`, etc.)
   - Dependências externas relevantes não listadas acima
   - Declarar explicitamente qualquer dependência cuja função seja desconhecida

2. `Dockerfile` e `docker-compose*.yml` (se existirem)
   - Serviços declarados (banco, cache, worker, beat, etc.)
   - Versão do PostgreSQL
   - Variáveis de ambiente expostas

3. `.env.example` ou `.env.sample` (se existir)
   - Variáveis obrigatórias declaradas
   - Indicação de integrações externas por nome de variável

---

## Etapa 2 — Leitura das configurações Django

Leia `settings.py` ou todos os arquivos em `settings/` (base, local, production, etc.):

1. `INSTALLED_APPS` — listar todos os apps, separando:
   - Apps de terceiros
   - Apps próprios do projeto (prefixo do projeto ou sem prefixo conhecido)
   - Apps Django built-in relevantes (`django.contrib.auth`, `rest_framework`, etc.)

2. `DATABASES` — confirmar engine PostgreSQL, nome do banco, host

3. `AUTH_USER_MODEL` — modelo de usuário customizado ou padrão Django

4. `REST_FRAMEWORK` — configurações globais de autenticação, permissão e paginação

5. `CELERY_*` ou `CELERY_BROKER_URL` — confirmar broker e backend

6. `CACHES` — confirmar backend de cache (Redis, Memcached, dummy, etc.)

7. `MIDDLEWARE` — listar middlewares customizados que fujam do padrão Django

8. `LOGGING` — estratégia de log declarada (handlers, formatters, nível)

9. Qualquer configuração que referencia serviço externo (APIs, storage, email, etc.)

---

## Etapa 3 — Mapeamento de apps e domínios

Para cada app listado em `INSTALLED_APPS` que seja próprio do projeto:

1. Confirmar existência dos seguintes arquivos (declarar ausência quando não encontrar):
   - `models.py` ou `models/`
   - `managers.py`
   - `views.py` ou `api/views/`
   - `serializers.py` ou `api/serializers/`
   - `services.py` ou `use_cases.py`
   - `tasks.py`
   - `urls.py` ou `api/routers.py`
   - `admin.py`
   - `tests/` ou `test_*.py`
   - `migrations/`

2. Identificar o **domínio de negócio** de cada app com base nos nomes dos models encontrados — declarar como premissa se não for óbvio pelo nome do app

3. Identificar dependências entre apps: qual app importa models, services ou funções de outro app (grep por `from <outro_app>`)

4. Identificar apps que possuem lógica de negócio em views (grep por `save()`, `create()`, `update()`, `delete()` diretamente em views) — declarar como ponto de atenção

---

## Etapa 4 — Análise de models e banco de dados

Para cada app com `models.py` ou `models/`:

1. Listar todas as entidades (classes que herdam de `models.Model` ou base customizada)
2. Para cada entidade identificar:
   - Campos e tipos principais
   - Relacionamentos (`ForeignKey`, `OneToOneField`, `ManyToManyField`) e os apps relacionados
   - Uso de `Meta.indexes`, `Meta.constraints`, `Meta.ordering`
   - Campos com `unique=True` ou `unique_together`
   - Campos que sugerem dados sensíveis (CPF, email, telefone, senha, token) — marcar para revisão LGPD

3. Verificar se existe modelo de usuário customizado (`AbstractUser`, `AbstractBaseUser`) e documentar seus campos adicionais

4. Contar o número de migrations por app e identificar:
   - Se há migrations não aplicadas (comparar com estado atual dos models — apenas visualmente, sem rodar `migrate`)
   - Se há migrations de dados (`RunPython`, `RunSQL`) — listar
   - Se há migrations com operações de alto risco (`RemoveField`, `AlterField` em tabelas grandes, `SeparateDatabaseAndState`)

---

## Etapa 5 — Análise da camada de API

1. Identificar o padrão de roteamento:
   - URLs definidas em `urls.py` por app ou centralizadas em `base/urls.py` / `config/urls.py`
   - Prefixo global de API (ex.: `/api/v1/`, `/api/`)
   - Uso de `DefaultRouter`, `SimpleRouter` ou rotas manuais

2. Para cada ViewSet ou APIView encontrada:
   - Identificar autenticação e permissões aplicadas (`authentication_classes`, `permission_classes`)
   - Identificar se há lógica de negócio embutida (ponto de atenção)
   - Identificar uso de `get_queryset` com `select_related`/`prefetch_related` ou sem otimização

3. Identificar serializers customizados com `validate_*` ou `validate` sobrescritos

4. Identificar endpoints que expõem campos sensíveis sem filtro (`SerializerMethodField`, `source=`)

---

## Etapa 6 — Análise de segurança

1. Autenticação:
   - Mecanismo principal (SessionAuthentication, TokenAuthentication, JWTAuthentication, outro)
   - Existe endpoint de login/logout/refresh? Em qual app?
   - Existe autenticação social ou SSO configurado?

2. Autorização:
   - Permissões globais definidas em `REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES']`
   - Apps ou views que sobrescrevem permissões globalmente
   - Existência de permissões customizadas (`BasePermission`)

3. Proteção de dados:
   - Campos sensíveis em models (identificados na Etapa 4) — verificar se são serializados sem filtro
   - Logs que possam conter PII (grep por `logger.` próximo a campos de usuário)
   - Uso de `write_only=True` em serializers para senhas/tokens

4. Configurações de segurança Django:
   - `DEBUG` — confirmar que não está `True` via variável de ambiente em produção
   - `ALLOWED_HOSTS`, `CORS_*`, `CSRF_*`
   - `SECRET_KEY` — confirmar que vem de variável de ambiente

---

## Etapa 7 — Análise de tasks assíncronas

Se Celery estiver presente:

1. Listar todos os arquivos `tasks.py` encontrados
2. Para cada task identificar:
   - Nome da task e app de origem
   - Se possui `bind=True`, `max_retries`, `autoretry_for`
   - Se há garantia de idempotência (comentário ou lógica explícita)
   - Se há log de início e fim
   - Se a task acessa banco diretamente ou via service

3. Verificar se há `beat_schedule` configurado e listar as tasks agendadas

---

## Etapa 8 — Pontos de atenção e débitos técnicos

Ao final da leitura, consolidar uma lista explícita de pontos de atenção encontrados, separados por categoria:

**Acoplamento indevido:**
- Apps que importam models de outros apps diretamente (sem service ou contrato)

**Performance:**
- Views ou serializers sem `select_related`/`prefetch_related` em relacionamentos
- QuerySets em loops identificados (`for ... in queryset: obj.related_set.all()`)

**Segurança:**
- Campos sensíveis sem `write_only` ou sem filtro na serialização
- Endpoints sem permissão explícita declarada
- `DEBUG` ou `SECRET_KEY` hardcoded

**Qualidade:**
- Lógica de negócio em views
- Models com regras de negócio embutidas (`save()` sobrescrito com lógica complexa)
- Ausência de testes em apps de domínio crítico

**Migrations:**
- Migrations de dados sem reversão implementada
- Operações destrutivas sem comentário de impacto

**Outros:**
- Qualquer padrão que contradiga `.ia/docs/guides/constraints.md` ou `.ia/docs/guides/patterns.md`

---

## Etapa 9 — Entregáveis obrigatórios

Ao concluir todas as etapas acima, preencher ou criar os seguintes arquivos. Se o arquivo já existir, atualizar apenas o que mudou — não sobrescrever conteúdo que já estava correto.

### 9.1. `.ia/docs/architecture/overview.md`

Preencher com:
- Stack confirmada (versões reais encontradas em `pyproject.toml`)
- Serviços de infraestrutura confirmados (banco, cache, fila, busca)
- Objetivos arquiteturais inferidos do projeto (declarar como premissa)
- Regras gerais de qualidade que já são seguidas vs. as que não são

### 9.2. `.ia/docs/architecture/system-architecture.md`

Preencher com:
- Catálogo real de apps e domínios de negócio (com base na Etapa 3)
- Camadas arquiteturais identificadas
- Fluxos principais inferidos (declarar como premissa os que não puderem ser confirmados por código)
- Integrações externas identificadas (Etapa 1 + Etapa 6)

### 9.3. `.ia/docs/architecture/modules.md`

Preencher com:
- Estrutura real encontrada por app (quais arquivos existem de fato vs. o padrão esperado)
- Desvios do padrão modular (declarar explicitamente)
- Regras de acoplamento vigentes vs. violações identificadas

### 9.4. `.ia/docs/architecture/security.md`

Preencher com:
- Mecanismo de autenticação real (Etapa 6)
- Configuração de permissões vigente
- Dados sensíveis identificados e status de proteção atual
- Riscos de segurança encontrados (Etapa 8)

### 9.5. Task de análise em `.ia/docs/tasks/done/`

Criar e mover para `done/` uma task documentando:
- O que foi analisado
- Premissas declaradas
- Pontos de atenção encontrados (resumo da Etapa 8)
- Arquivos criados/atualizados
- O que **não** foi possível confirmar sem execução do projeto

---

## Critérios de aceite

- [ ] Todos os apps de `INSTALLED_APPS` estão catalogados em `system-architecture.md`
- [ ] Todos os models com dados sensíveis estão identificados em `security.md`
- [ ] Todos os pontos de atenção da Etapa 8 estão listados na task de análise
- [ ] Nenhuma premissa ficou implícita — toda inferência está declarada como tal
- [ ] Nenhum arquivo de código-fonte foi alterado
- [ ] Os quatro arquivos de `.ia/docs/architecture/` foram criados ou atualizados
