# PRD - <Nome da Funcionalidade ou Produto>

---

## 1. Metadados

| Campo | Valor |
|---|---|
| Título | |
| Identificador (slug) | |
| Versão do documento | `0.1` |
| Status do PRD | `draft` \| `in_review` \| `approved` \| `in_progress` \| `delivered` \| `archived` |
| Data de criação | `DD-MM-YYYY` |
| Última atualização | `DD-MM-YYYY` |
| Autor(a) | |
| Product Owner | |
| Tech Lead | |
| Designer responsável | |
| Stakeholders | |
| Aprovadores | |
| Tasks relacionadas | `<path_da_task_no_repo_ou_nao_se_aplica>` |
| Módulos FastAPI impactados | |
| Sistemas externos impactados | |

---

## 2. Resumo executivo

Descreva em até **5 linhas** o que está sendo proposto, para quem, e o ganho esperado. Esta seção deve permitir a um leitor não-técnico entender o PRD sem ler o restante.

---

## 3. Contexto e problema

### 3.1. Situação atual

Descreva o estado atual do sistema ou processo. Use evidências (métricas, prints, tickets, feedback).

### 3.2. Problema a resolver

Defina o problema em uma frase. Evite descrever a solução nesta seção.

### 3.3. Por que agora

Justifique a priorização: mudança regulatória, custo operacional, risco, oportunidade de receita, dívida técnica bloqueante, etc.

### 3.4. Custo de não fazer

Quantifique se possível (horas/mês, R$/mês, número de tickets, churn, exposição LGPD).

---

## 4. Objetivos e métricas de sucesso

### 4.1. Objetivos de negócio

- Objetivo 1 — declaração curta.
- Objetivo 2 — declaração curta.

### 4.2. Métricas (KPIs)

| Métrica | Como medir | Baseline atual | Meta | Prazo de avaliação |
|---|---|---|---|---|
| Ex.: tempo médio de cadastro | Evento `cadastro_concluido` | 4 min | ≤ 90 s | 30 dias após GA |

### 4.3. Critérios de sucesso (binários)

Liste afirmações que serão `verdadeiras` quando a entrega for considerada bem sucedida.

- [ ] Usuário consegue concluir o fluxo X em ≤ N cliques.
- [ ] Endpoint/Página Y responde em ≤ Z ms no P95.
- [ ] Cobertura de testes do app `<nome_app>` ≥ N%.

### 4.4. Hipóteses

Liste premissas que, se falsas, invalidam o PRD.

- Hipótese 1
- Hipótese 2

---

## 5. Escopo

### 5.1. Dentro do escopo

Liste itens explicitamente cobertos.

### 5.2. Fora do escopo

Liste o que **não** será entregue. Quanto mais explícito, menor o risco de scope creep.

### 5.3. Premissas operacionais

- Stack: FastAPI, PostgreSQL, SQLAlchemy e Pydantic.
- Autenticação: OAuth2 Bearer/JWT via dependências FastAPI existentes.
- Idioma da interface: pt-BR; formato de data `dd/mm/aaaa`; moeda BRL; timezone `America/Sao_Paulo`.
- Acessibilidade: WCAG 2.1 AA.
- Navegadores suportados: lista mínima (ex.: 2 versões mais recentes de Chrome, Firefox, Edge, Safari).

---

## 6. Usuários e personas

### 6.1. Personas envolvidas

| Persona | Papel no sistema | Objetivo principal | Frequência de uso |
|---|---|---|---|
| | | | |

### 6.2. Permissões e grupos

| Perfil/role | Permissões necessárias | Acesso esperado |
|---|---|---|
| | | |

---

## 7. Histórias de usuário (user stories)

Use o padrão **Como [persona], quero [ação], para [ganho]**.

- **US-01**: Como `<persona>`, quero `<ação>`, para `<ganho>`.
  - **Critérios de aceite**:
    - [ ] Dado `<contexto>`, quando `<ação>`, então `<resultado esperado>`.
    - [ ] Mensagens de erro retornadas no contrato HTTP com status code e payload coerentes.

- **US-02**: ...

---

## 8. Requisitos funcionais

Numere de forma estável. Não renumere quando remover; marque como `DEPRECATED`.

| ID | Requisito | Prioridade | Origem |
|---|---|---|---|
| RF-001 | O sistema deve permitir que `<persona>` realize `<ação>`. | `obrigatorio` \| `desejavel` \| `opcional` | US-01 |
| RF-002 | | | |

---

## 9. Requisitos não funcionais

### 9.1. Performance

- Tempo de resposta server-side P95 ≤ `__ ms` para páginas críticas.
- Consultas por requisição ≤ `__` quando mensurável por logs/instrumentação.
- Uso de joins/eager loading SQLAlchemy obrigatório em listagens com relacionamentos.

### 9.2. Escalabilidade

- Volume esperado de registros após 12 meses.
- Picos previstos (campanhas, fechamento mensal, etc.).
- Estratégia de paginação para listagens (`offset/limit`, cursor ou padrão já adotado pelo módulo).

### 9.3. Segurança

- Autenticação por Bearer/JWT ou dependência FastAPI aprovada para o fluxo.
- Proteção contra IDOR: filtrar consultas pelo usuário/tenant/contexto autorizado quando aplicável.
- Validação e sanitização: schemas Pydantic, validações de domínio e proteção contra exposição indevida de campos.

### 9.4. LGPD e privacidade

- Dados pessoais coletados: listar e classificar (`identificador`, `sensível`, `financeiro`, etc.).
- Base legal de tratamento por categoria de dado.
- Retenção: prazo e mecanismo de expurgo.
- Anonimização em logs: nenhum PII em log; ver `.ia/docs/architecture/security.md`.
- Direitos do titular: como atender exportação, correção, exclusão.

### 9.5. Acessibilidade (WCAG 2.1 AA)

- Contraste mínimo, navegação por teclado, `aria-*` em componentes interativos.
- Formulários: `label` associado a todo `input`; mensagens de erro descritivas em pt-BR.
- Testar com leitor de tela (NVDA ou VoiceOver) nos fluxos críticos.

### 9.6. Internacionalização e localização

- Idioma único pt-BR para mensagens de negócio expostas pela API.
- Formatação de data, número e moeda deve seguir o contrato definido para o cliente consumidor.

### 9.7. Observabilidade

- Eventos relevantes registrados via logger nomeado por app (`logging.getLogger("<app>")`).
- Métricas: contadores por evento de negócio (sucesso, falha, latência).
- Sentry (ou equivalente) deve capturar exceções não tratadas com `release` e `environment`.

### 9.8. Confiabilidade

- Operações de escrita múltipla envoltas em transação SQLAlchemy apropriada.
- Idempotência declarada para background tasks, workers ou integrações externas quando houver.
- Comportamento esperado em falha de dependência externa.

---

## 10. Fluxos de usuário

Descreva os fluxos principais. Para cada fluxo, indicar endpoints, routers, schemas, use cases e clientes envolvidos.

### 10.1. Fluxo `<nome>`

1. Cliente chama `GET /<url>/`.
  - Router: `modulo.routers`.
  - Response schema: `modulo.schemas.<Schema>`.
2. Cliente envia `POST /<url>/`.
  - Request schema: `modulo.schemas.<InputSchema>`.
  - Use case: `modulo.use_cases.<UseCase>`.
  - Validação server-side e resposta HTTP de sucesso/erro.
3. ...

**Diagrama** _(opcional, link para Excalidraw/Lucid)_:

```
[Autenticacao] -> [Listagem] -> [Acao HTTP] -> [Resposta]
```

---

## 11. Clientes e contratos de API

### 11.1. Estrutura de contratos

- Prefixo base da API: `/api/v1/` ou valor configurado em `settings.api_str`.
- Routers esperados por módulo: `routers.py`.
- Schemas esperados por módulo: `schemas.py`.
- Contratos devem ser verificáveis via OpenAPI/Swagger quando aplicável.

### 11.2. Endpoints previstos

| Endpoint | Método | Router | Request schema | Response schema | Permissão |
|---|---|---|---|---|---|
| | | | | | |

### 11.3. Padrões de cliente

- Estados de carregamento, vazio e erro definidos pelo cliente consumidor.
- Mensagens de erro devem ser estáveis e coerentes com o contrato HTTP.
- Mudanças que afetem Flutter ou outro cliente devem ter spec de integração quando necessário.

### 11.4. Wireframes / mockups

Inserir link para Figma, Excalidraw ou anexos versionados junto do artefato correspondente em `.ia/docs/specs/`, quando aplicável.

---

## 12. Modelo de dados

### 12.1. Entidades novas ou alteradas

#### `<NomeEntidade>` (`app.<nome_app>`)

| Campo | Tipo SQLAlchemy/Pydantic | Restrições | Índice | Sensível (LGPD) | Observação |
|---|---|---|---|---|---|
| `id` | `UUID` ou tipo existente no módulo | PK | sim | não | |
| `nome` | `String(120)` / `str` | `not null` | não | não | |
| `cpf` | `String(14)` / `str` | `unique` | sim | **sim** | Mascarar em responses/logs |
| | | | | | |

**Relacionamentos**:

- Relacionamento SQLAlchemy para `<OutraEntidade>` quando aplicável.
- Tabelas associativas/modelos intermediários quando o relacionamento carrega atributos.

**Constraints PostgreSQL**:

- `UniqueConstraint(...)`.
- `CheckConstraint(...)`.
- Índices compostos previstos para consultas reais (não especulativos).

**Migrations**:

- Migrations pequenas e reversíveis quando o fluxo de migration estiver definido.
- Separar alteração de schema de backfill de dados.
- Avaliar locks em tabelas grandes; documentar janela de manutenção quando necessária.

### 12.2. Diagrama (ER)

Inserir diagrama ou link.

### 12.3. Dados de seed / fixtures

Indicar se haverá seed, script operacional ou migration/backfill de dados.

---

## 13. Permissões, autenticação e autorização

- Autenticação: OAuth2 Bearer/JWT ou integração de identidade aprovada.
- Autorização:
  - Dependências FastAPI em todas as rotas autenticadas.
  - Verificação explícita de role/permissão para ações sensíveis.
  - Filtro de consultas por usuário/tenant/contexto autorizado.
- Auditoria: registrar eventos críticos em modelo de log ou tabela de auditoria.

---

## 14. Integrações

### 14.1. Internas (entre módulos FastAPI)

| Módulo consumidor | Módulo fornecedor | Forma de acesso (use case, service, query, integração) |
|---|---|---|
| | | |

### 14.2. Externas

| Sistema | Protocolo | Operação | Autenticação | Timeout | Política de retry |
|---|---|---|---|---|---|
| | | | | | |

### 14.3. Background tasks / filas (opcional)

- Tasks previstas, tecnologia, periodicidade, idempotência e payload mínimo.

---

## 15. Performance, cache e otimização

- Consultas críticas listadas com query SQLAlchemy esperada e índices necessários.
- Estratégia de cache por endpoint quando aplicável.
- Estratégia de invalidação de cache.
- Compressão e cache de assets estáticos (`collectstatic`, `whitenoise` ou CDN).

---

## 16. Observabilidade e operação

- **Logs**: níveis (`INFO`, `WARNING`, `ERROR`), formato, ausência de PII.
- **Métricas**: contadores e histogramas relevantes para o negócio.
- **Alertas**: condições e canal (e-mail, Slack, PagerDuty).
- **Runbook**: link ou seção curta com passos para incidentes comuns.

---

## 17. Plano de rollout

- **Estratégia**: big bang, gradual, feature flag por configuração ou canary.
- **Pré-requisitos de produção**: migrations aplicadas, variáveis de ambiente, índices criados, dados migrados.
- **Comunicação**: changelog interno, e-mail, banner no app.
- **Plano de rollback**: como reverter sem perda de dados (migrations reversíveis + flag desativável).

---

## 18. Plano de testes

### 18.1. Tipos de teste

- **Unitários**: use cases, services, schemas e validators (pytest).
- **Integração**: routers/endpoints com cliente HTTP de teste.
- **Migrations/backfill**: aplicar e reverter localmente quando houver fluxo versionado.
- **Performance**: contagem de queries/logs em listagens críticas.
- **Segurança**: testes que validam ausência de IDOR e respeito a permissões.
- **Acessibilidade**: checagem manual + ferramenta automatizada (axe, Lighthouse) em telas críticas.

### 18.2. Critérios mínimos

- Cobertura mínima por app impactado: `__%`.
- Todos os requisitos `obrigatorio` da seção 8 possuem teste correspondente.

### 18.3. Dados de teste

- Uso de factories próprias, Faker ou fixtures controladas.
- Dados sensíveis fictícios; nunca usar PII real.

---

## 19. Riscos e mitigações

| ID | Risco | Probabilidade | Impacto | Mitigação | Plano de contingência |
|---|---|---|---|---|---|
| R-01 | | `baixa` \| `media` \| `alta` | `baixo` \| `medio` \| `alto` | | |

---

## 20. Dependências e bloqueios

- Equipes externas envolvidas e o que se espera de cada uma.
- Dependências técnicas (libs, infraestrutura, contratos com terceiros).
- Bloqueios conhecidos no momento da redação.

---

## 21. Cronograma estimado

Tabela de marcos. Datas absolutas no formato `DD-MM-YYYY`.

| Marco | Descrição | Data prevista | Responsável |
|---|---|---|---|
| Kickoff | | | |
| Especificação técnica | | | |
| MVP funcional | | | |
| Testes integrados | | | |
| Homologação | | | |
| Go-live | | | |

---

## 22. Decisões técnicas registradas

Pequenas ADRs embutidas. Para cada decisão relevante:

- **Contexto**:
- **Decisão**:
- **Alternativas consideradas**:
- **Consequências**:

---

## 23. Glossário

Termos de domínio e siglas usados no PRD.

| Termo | Definição |
|---|---|
| | |

---

## 24. Referências

- `AGENTS.md`
- `.ia/docs/architecture/overview.md`
- `.ia/docs/architecture/modules.md`
- `.ia/docs/architecture/security.md`
- `.ia/docs/guides/patterns.md`
- `.ia/docs/testing/strategy.md`
- `.ia/docs/guides/constraints.md`
- Links externos (Figma, planilhas, tickets, documentação de terceiros).

---

## 25. Histórico de revisões

| Versão | Data | Autor(a) | Mudanças |
|---|---|---|---|
| 0.1 | `DD-MM-YYYY` | | Versão inicial |

---

## 26. Aprovações

| Papel | Nome | Data | Status |
|---|---|---|---|
| Product Owner | | | `pending` \| `approved` \| `rejected` |
| Tech Lead | | | |
| Segurança / LGPD | | | |
| Design | | | |
