# SPEC Tecnica - <Titulo curto da mudanca>

> **Como usar**: este template e orientativo. Mantenha o cabecalho de metadados; adapte/remova secoes conforme o escopo. 
Para refatorações use AS-IS + TO-BE; para features novas substitua AS-IS por "Contexto". 
Especificações geradas pela skill `fastapi-especificacao-tecnica` para a camada 
FastAPI seguem template proprio em `.ia/skills/fastapi-especificacao-tecnica/`.

- Data: `DD-MM-YYYY`
- Status: `draft` | `approved` | `in_progress` | `in_review` | `done` | `cancelled` | `superseded`
- Apps principais: `app_a`, `app_b`
- App transversal relacionado: `core` (quando aplicavel)
- Publico-alvo: `Equipe Django/DRF` | `Equipe FastAPI` | `Equipe Frontend`
- Task(s) de rastreabilidade: `.ia/docs/tasks/todo/task-DD-MM-YYYY-<hash_alfanumerico_10>.md`

---

## 1. Objetivo

Descrever em 1-2 paragrafos o problema, o estado alvo e o porque da mudanca.

Estado alvo (lista curta de invariantes que devem ser verdadeiros ao final):

1. ...
2. ...
3. ...

## 2. Escopo

### 2.1 Entra no escopo

- ...

### 2.2 Fica fora do escopo

- ...

## 3. Premissas e decisoes

Liste premissas tecnicas/operacionais e decisoes ja tomadas que orientam a spec.

- Premissa: ...
- Decisao: ...

## 4. AS-IS (estado atual)

> Use para refatoracoes / migracoes. Para features novas, substitua por "Contexto".

### 4.1 Diagnostico

- Onde a logica/dado vive hoje.
- Quais limitacoes/problemas existem.

### 4.2 Hotspots prioritarios

| Prioridade | App | Local | Diagnostico | Direcao proposta |
| --- | --- | --- | --- | --- |
| P0 | ... | `app/file.py:linha` | ... | ... |

## 5. TO-BE (proposta)

### 5.1 Visao geral

Descreva a arquitetura alvo. Diagrama em texto/Mermaid quando ajudar.

### 5.2 Contratos / Interfaces

- Managers/services novos.
- Assinaturas de metodos publicos.

## 6. Requisitos funcionais

- RF1: ...
- RF2: ...

## 7. Requisitos nao funcionais

- Desempenho: ...
- Seguranca/LGPD: ...
- Observabilidade: ...

## 8. Contratos de API (quando aplicavel)

| Verbo | Path | Auth | Request | Response | Observacoes |
| --- | --- | --- | --- | --- | --- |
| GET | `/app/api/v1/recurso/` | JWT | ... | ... | ... |

## 9. Alteracoes em camadas Django (quando aplicavel)

### 9.1 Models / Migrations

- Mudancas de schema.
- Migrations previstas (numero, tipo, reversibilidade).

### 9.2 Managers / QuerySets

- Metodos novos por model.

### 9.3 Serializers / Views / Permissions

- Diff esperado em `api/serializers/`, `api/views/`, `api/routers.py`.

### 9.4 Services / Use cases

- Fluxos de orquestracao.

### 9.5 Tasks (Celery)

> Hoje Celery nao esta instalado (`overview.md` §2). Se a spec depender de Celery, registrar a decisao em §3.

## 10. Permissoes e autenticacao

Liste permissoes/roles necessarios e quais backends DRF cobrem o caso.

## 11. Observabilidade

- Logs estruturados a emitir (`logger.getLogger("django_debug")`).
- Eventos Sentry / Elastic APM.

## 12. Testes previstos

- Unit: ...
- API: ...
- Migration / data backfill: ...

## 13. Ordem de implementacao recomendada

Sequencia obrigatoria/preferencial das tasks executaveis (mapear cada item a uma task em `.ia/docs/tasks/todo/`).

1. Task 1 — ...
2. Task 2 — ...

## 14. Riscos e mitigacoes

| Risco | Probabilidade | Impacto | Mitigacao |
| --- | --- | --- | --- |
| ... | media | alto | ... |

## 15. Criterios de aceite

- Criterio 1: ...
- Criterio 2: ...
- Spec movida para `.ia/docs/specs/done/` apos todas as tasks derivadas serem concluidas.

---

## Convencao de nome

- Padrao canonico: `<dominio>-<descricao-curta>-spec-DD-MM-YYYY.md`
- Exemplos: `assinatura-documento-fluxo-solicitacao-spec-30-05-2026.md`, `refatoracao-consultas-managers-spec-30-05-2026.md`.
- Specs FastAPI (subpasta `fastapi/`) seguem `<dominio>-<descricao-curta>-fastapi-spec-DD-MM-YYYY.md` por convencao da skill `fastapi-especificacao-tecnica`.

## Ciclo de vida

1. Criar a spec em `.ia/docs/specs/` (raiz).
2. Aprovar com o desenvolvedor.
3. Criar as tasks derivadas em `.ia/docs/tasks/todo/`, referenciando esta spec na secao "Referencias consultadas".
4. Ao concluir todas as tasks derivadas, mover a spec para `.ia/docs/specs/done/`.
