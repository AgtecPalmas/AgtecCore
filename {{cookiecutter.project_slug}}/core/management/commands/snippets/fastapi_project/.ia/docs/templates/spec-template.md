# SPEC Tecnica - <Titulo curto da mudanca>

> **Como usar**: este template e orientativo. Mantenha o cabecalho de metadados; adapte/remova secoes conforme o escopo. Para refatorações use AS-IS + TO-BE; para features novas substitua AS-IS por "Contexto". Specs deste repositorio devem refletir a camada FastAPI real descrita em `.ia/docs/architecture/overview.md`.

- Data: `DD-MM-YYYY`
- Status: `draft` | `approved` | `in_progress` | `in_review` | `done` | `cancelled` | `superseded`
- Modulos principais: `modulo_a`, `modulo_b`
- Modulo transversal relacionado: `core` (quando aplicavel e explicitamente autorizado)
- Publico-alvo: `Equipe FastAPI` | `Equipe Frontend` | `Equipe IA`
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

- Routers/endpoints novos ou alterados.
- Schemas Pydantic de entrada/saida.
- Use cases/services e dependencias FastAPI.
- Assinaturas de metodos publicos e contratos de integracao.

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

## 9. Alteracoes em camadas FastAPI (quando aplicavel)

### 9.1 Models SQLAlchemy / schema de banco

- Mudancas de schema.
- Estrategia de migration/backfill quando aplicavel.
- Reversibilidade e riscos de lock em tabelas relevantes.

### 9.2 Schemas Pydantic

- Schemas de entrada, resposta e filtros.
- Validacoes de contrato e compatibilidade com clientes.

### 9.3 Routers / Dependencies / Permissions

- Diff esperado em `routers.py`, dependencias FastAPI, response models e autorizacao.

### 9.4 Services / Use cases

- Fluxos de orquestracao.
- Regras de negocio e transacoes.

### 9.5 Integracoes / background tasks

> Se a spec depender de worker, fila, scheduler ou background task, registrar a decisao em §3 e apontar a tecnologia real usada pelo projeto.

## 10. Permissoes e autenticacao

Liste permissoes/roles necessarios e quais dependencias FastAPI cobrem o caso.

## 11. Observabilidade

- Logs estruturados a emitir.
- Eventos Sentry, Elastic APM, Logfire ou mecanismo equivalente ja configurado.

## 12. Testes previstos

- Unit: use cases, services, schemas e helpers.
- API: routers/endpoints com cliente HTTP de teste.
- Banco: models, consultas e backfill/migration quando aplicavel.

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
- Spec movida ou marcada como concluida conforme o fluxo aprovado apos todas as tasks derivadas serem concluidas.

---

## Convencao de nome

- Padrao canonico: `<dominio>-<descricao-curta>-spec-DD-MM-YYYY.md`
- Exemplos: `assinatura-documento-fluxo-solicitacao-spec-30-05-2026.md`, `refatoracao-consultas-managers-spec-30-05-2026.md`.
- Specs de integracao podem usar sufixo explicito de camada quando aprovado pela skill correspondente.

## Ciclo de vida

1. Criar a spec em `.ia/docs/specs/` (raiz).
2. Aprovar com o desenvolvedor.
3. Criar as tasks derivadas em `.ia/docs/tasks/todo/`, referenciando esta spec na secao "Referencias consultadas".
4. Ao concluir todas as tasks derivadas, mover a spec para o destino de concluídas aprovado pelo fluxo do projeto.
