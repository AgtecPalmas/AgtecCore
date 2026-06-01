# Plano de Ajuste do Pacote `.ia/` — Template CookieCutter

## 1. Contexto

O `.ia/` é parte de um template CookieCutter que gera projetos Django. Precisa ser:
- **Genérico** o suficiente para qualquer projeto Django gerado
- **Atrelado a Django** (não a uma stack específica)
- **Pronto para uso** no projeto gerado (sem dependência de arquivos externos)

---

## 2. Jobs

### Job 1: Revisar `AGENTS.md` — Remover hard-coding e referenciar `.ia/docs/`

**Problema**: O arquivo contém valores específicos (`Django 4.2`, `pgvector`, `SimpleJWT`, etc.) que não deveriam estar em um template genérico. Skills referenciam `AGENTS.md` como se estivesse dentro de `.ia/`, mas ele fica na raiz.

**Ação**:
1. Remover valores hard-codados da seção §1 (manter apenas "projeto Django com DRF")
2. Na seção §2, explicitrar que `.ia/docs/architecture/overview.md` é a fonte de verdade canônica
3. Remover menções a `base/settings.py`, `rtk`, `task lint`, `task test` —，这些都是 valores específicos de instância
4. Manter as regras operacionais (RTK, skills, status, convenções) pois são reutilizáveis
5. Atualizar referências: skills referenciam `AGENTS.md` na raiz → mudar para `.ia/docs/architecture/overview.md`

**Arquivos afetados**: `AGENTS.md`

---

### Job 2: Criar `overview.md` com variáveis CookieCutter

**Problema**: `overview.md` contém valores específicos do AgtecCore que devem ser variáveis de template.

**Ação**: Substituir valores hard-codados por variáveis CookieCutter:

```
## 1. Stack Inicial

| Camada | Tecnologia | Versão |
| Linguagem | Python | `{{ cookiecutter.python_version }}` |
| Framework web | Django | `{{ cookiecutter.django_version }}` |
| API | Django REST Framework | `{{ cookiecutter.drf_version }}` |
| Banco de dados | PostgreSQL | `{{ cookiecutter.postgresql_version }}` |

## 2. Stack NÃO presente

- Celery (assíncrono) — remover se não necessário
- Redis (filas/cache) — remover se não necessário
- Elasticsearch — remover se não necessário

## 3. Integrações externas

`{{ cookiecutter.integracoes_externas | default("A definir no projeto gerado") }}`

## 6. Pontos de atenção imediatos

Manter como exemplo de checklist, mas comentar que são pontos de atenção do AgtecCore e não necessariamente de qualquer projeto gerado.
```

**Arquivos afetados**: `.ia/docs/architecture/overview.md`

---

### Job 3: Renomear `django-analise-arquitetura-legado` → `django-onboarding-checklist`

**Problema**: A skill atual serve para analisar projetos Django existentes (código legacy). Em um template, não há código para analisar.

**Ação**:
1. Renomear diretório de `django-analise-arquitetura-legado` para `django-onboarding-checklist`
2. Reescrever o `SKILL.md` para ser um checklist de validação inicial de um novo projeto gerado:
   - Verificar `INSTALLED_APPS`
   - Verificar `AUTH_USER_MODEL`
   - Verificar migrations
   - Verificar variáveis de ambiente
   - Verificar conexão com banco
3. Atualizar referências na tabela do README e AGENTS.md

**Arquivos afetados**:
- `skills/django-analise-arquitetura-legado/` → `skills/django-onboarding-checklist/`
- `README.md` (tabela de skills)
- `AGENTS.md` (catálogo de skills)

---

### Job 4: Limpar `todo/` e `done/` — manter apenas exemplos

**Problema**: Tasks em andamento não fazem sentido em um template.

**Ação**:
1. Remover qualquer arquivo real em `todo/` e `done/`
2. Criar exemplos mínimos em cada diretório:
   - `todo/task-EXEMPLO-01-01-2025-abcdefghij.md` (com conteúdo de exemplo)
   - `done/done-task-EXEMPLO-01-01-2025-abcdefghij.md` (com conteúdo preenchido como exemplo)
3. Adicionar README em cada diretório explicando o propósito

**Arquivos afetados**:
- `.ia/docs/tasks/todo/` e `.ia/docs/tasks/done/`
- Adicionar `.ia/docs/tasks/README.md` explicando o fluxo

---

### Job 5: Remover referências circulares em skills

**Problema**: `workflow-demandas/SKILL.md` referencia a si mesma e a documentos que podem não existir.

**Ação**:
1. `workflow-demandas/SKILL.md` — remover referências a si mesma e a `overview.md` (já que será variável)
2. Manter referências apenas a:
   - `.ia/docs/templates/task-template.md`
   - `.ia/docs/architecture/overview.md` (pós-Job 2, será genérico)
3. Outras skills Django (`django-models`, `django-api-views`, etc.) — revisar e remover referências a `AGENTS.md` ou torná-las opcionais

**Arquivos afetados**: Todas as skills em `.ia/skills/*/SKILL.md`

---

### Job 6: Preencher `system-architecture.md` e `modules.md` com placeholders claros

**Problema**: Estes arquivos têm seções vazias ("-") que não fazem sentido.

**Ação**:
1. `system-architecture.md` —rewriting com estrutura de placeholders:
   - Apps do projeto (`{{ cookiecutter.project_slug }}`)
   - Integrações (FastAPI externo, Flutter, etc.)
   - Fluxos de autenticação
   - Diagrama de camadas (placeholder)
2. `modules.md` — preenchimento com estrutura padrão Django e placeholders:
   - Cada app com `models.py`, `managers.py`, `api/serializers/`, `api/views/`, `api/routers.py`
   - Regras de SoftDelete, Audit, QuerySet

**Arquivos afetados**: `.ia/docs/architecture/system-architecture.md`, `.ia/docs/architecture/modules.md`

---

### Job 7: Atualizar `django-celery-tasks` SKILL.md

**Problema**: Skill está "dormente" mas isso é específico do AgtecCore.

**Ação**: Na skill, manter o aviso de que Celery não está na stack padrão, mas documentar como ativar quando necessário.

**Arquivos afetados**: `.ia/skills/django-celery-tasks/SKILL.md`

---

### Job 8: Ajustar README do `.ia/`

**Problema**: README referencia `AGENTS.md` na raiz e faz contagem incorreta de skills.

**Ação**:
1. Atualizar contagem: 17 → 16 skills (remover contagem duplicada)
2. Na tabela de skills, atualizar caminho e descrição para refletir o novo propósito genérico
3. Adicionar nota de que o `.ia/` é copiado para o projeto gerado

**Arquivos afetados**: `.ia/README.md`

---

## 3. Resumo dos Jobs

| # | Job | Prioridade | Complexidade | Arquivos afetados |
|---|-----|------------|--------------|-------------------|
| 1 | Revisar AGENTS.md | Alta | Média | 1 | ✅ concluído |
| 2 | overview.md com CookieCutter | Alta | Alta | 1 | ✅ concluído |
| 3 | Renomear skill legacy → onboarding | Alta | Média | 4+ | ✅ concluído |
| 4 | Limpar todo/done com exemplos | Média | Baixa | 4+ | ✅ concluído |
| 5 | Remover referências circulares | Alta | Média | 16 | pendente |
| 6 | Preencher system-architecture e modules | Média | Alta | 2 | pendente |
| 7 | Ajustar django-celery-tasks | Baixa | Baixa | 1 | pendente |
| 8 | Ajustar README .ia | Média | Baixa | 1 | ✅ concluído |

---

## 4. Pré-requisitos

- Definir as variáveis CookieCutter que serão usadas (sugestões):
  - `python_version`
  - `django_version`
  - `drf_version`
  - `postgresql_version`
  - `project_slug`
  - `project_name`
  - `database_name`
  - `database_user`
  - `integracoes_externas`

---

## 5. Status

- **Status**: `in_progress`
- **Jobs pendentes**: 3 (Jobs 5, 6, 7)
- **Jobs concluídos**: 5 (Jobs 1, 2, 3, 4, 8)