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
| Apps Django impactados | |
| Sistemas externos impactados | |

---

## 2. Resumo executivo

Descreva em até **5 linhas** o que está sendo proposto, para quem, e o ganho esperado. 
Esta seção deve permitir a um leitor não-técnico entender o PRD sem ler o restante.

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

- Stack: Django, PostgreSQL, templates Django (SSR).
- Autenticação: sessão Django (`django.contrib.auth`) + `LoginRequiredMixin` ou middleware.
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

| Grupo Django | Permissões necessárias | Acesso esperado |
|---|---|---|
| | | |

---

## 7. Histórias de usuário (user stories)

Use o padrão **Como [persona], quero [ação], para [ganho]**.

- **US-01**: Como `<persona>`, quero `<ação>`, para `<ganho>`.
  - **Critérios de aceite**:
    - [ ] Dado `<contexto>`, quando `<ação>`, então `<resultado esperado>`.
    - [ ] Mensagens de erro exibidas via `django.contrib.messages` com nível adequado.

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
- Queries por requisição ≤ `__` (validar com `assertNumQueries`).
- Uso de `select_related` / `prefetch_related` obrigatório em listagens.

### 9.2. Escalabilidade

- Volume esperado de registros após 12 meses.
- Picos previstos (campanhas, fechamento mensal, etc.).
- Estratégia de paginação para listagens (`Paginator` ou `django.views.generic.ListView`).

### 9.3. Segurança

- Autenticação por sessão Django; cookies `Secure`, `HttpOnly`, `SameSite=Lax`.
- CSRF habilitado em todos os formulários (`{% csrf_token %}` obrigatório).
- Proteção contra IDOR: filtrar `get_queryset()` pelo `request.user` quando aplicável.
- Sanitização: confiar nos templates Django (auto-escape); `mark_safe` apenas com justificativa.

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

- Idioma único pt-BR; usar `gettext` para strings de interface caso o sistema suporte mais idiomas no futuro.
- Formatação de data, número e moeda via `django.utils.formats` e `humanize`.

### 9.7. Observabilidade

- Eventos relevantes registrados via logger nomeado por app (`logging.getLogger("<app>")`).
- Métricas: contadores por evento de negócio (sucesso, falha, latência).
- Sentry (ou equivalente) deve capturar exceções não tratadas com `release` e `environment`.

### 9.8. Confiabilidade

- Operações de escrita múltipla envoltas em `transaction.atomic()`.
- Idempotência declarada para tarefas Celery (quando houver fila); ver `django-celery-tasks`.
- Comportamento esperado em falha de dependência externa.

---

## 10. Fluxos de usuário

Descreva os fluxos principais. Para cada fluxo, indicar URLs, views, templates e formulários envolvidos.

### 10.1. Fluxo `<nome>`

1. Usuário acessa `GET /<url>/`.
   - View: `app.views.MinhaView` (ou função).
   - Template: `app/templates/app/<arquivo>.html`.
2. Usuário envia formulário `POST /<url>/`.
   - Form: `app.forms.MeuForm`.
   - Validação server-side; redirect em sucesso (PRG pattern).
3. ...

**Diagrama** _(opcional, link para Excalidraw/Lucid)_:

```
[Login] -> [Lista] -> [Formulário] -> [Confirmação]
```

---

## 11. Telas e templates Django

### 11.1. Estrutura de templates

- Template base: `templates/base.html` (header, navbar, footer, blocos `{% block content %}`).
- Herança esperada por app: `app/templates/app/<entidade>_list.html`, `<entidade>_form.html`, `<entidade>_detail.html`.
- Componentes reutilizáveis: `templates/components/` ou `{% include %}`.

### 11.2. Telas previstas

| Tela | URL | View | Template | Form | Permissão |
|---|---|---|---|---|---|
| | | | | | |

### 11.3. Padrões de UI

- Tipografia, paleta e tokens em `static/css/` ou framework adotado (Bootstrap, Tailwind, etc.).
- Estado de carregamento, vazio e erro definidos por tela.
- Mensagens de feedback via `django.contrib.messages`.
- Componentes dinâmicos opcionais com **htmx** ou **Alpine.js** (declarar quando aplicável).

### 11.4. Wireframes / mockups

Inserir link para Figma, Excalidraw ou anexos versionados junto do artefato correspondente em `.ia/docs/specs/`, quando aplicável.

---

## 12. Modelo de dados

### 12.1. Entidades novas ou alteradas

#### `<NomeEntidade>` (`app.<nome_app>`)

| Campo | Tipo Django | Restrições | Índice | Sensível (LGPD) | Observação |
|---|---|---|---|---|---|
| `id` | `BigAutoField` | PK | sim | não | |
| `nome` | `CharField(max_length=120)` | `not null` | não | não | |
| `cpf` | `CharField(max_length=14)` | `unique` | sim | **sim** | Mascarar em listagens |
| | | | | | |

**Relacionamentos**:

- `ForeignKey` para `<OutraEntidade>` com `on_delete=PROTECT` quando aplicável.
- `ManyToMany` com `through=<Modelo>` quando o relacionamento carrega atributos.

**Constraints PostgreSQL**:

- `UniqueConstraint(fields=[...], name=...)`.
- `CheckConstraint(check=..., name=...)`.
- Índices compostos previstos para consultas reais (não especulativos).

**Migrations**:

- Migrations pequenas e reversíveis.
- Separar alteração de schema de backfill de dados (`RunPython` em migração distinta).
- Avaliar locks em tabelas grandes; documentar janela de manutenção quando necessária.

### 12.2. Diagrama (ER)

Inserir diagrama ou link.

### 12.3. Dados de seed / fixtures

Indicar se haverá `loaddata`, comando de management ou seed via migration de dados.

---

## 13. Permissões, autenticação e autorização

- Autenticação: sessão Django; integração com SSO (se aplicável).
- Autorização:
  - `LoginRequiredMixin` em todas as views autenticadas.
  - `PermissionRequiredMixin` ou `user.has_perm()` para ações sensíveis.
  - Filtro de `queryset` por `request.user` para garantir isolamento por tenant/usuário.
- Auditoria: registrar eventos críticos em modelo de log ou tabela de auditoria.

---

## 14. Integrações

### 14.1. Internas (entre apps Django)

| App consumidor | App fornecedor | Forma de acesso (service, signal, manager) |
|---|---|---|
| | | |

### 14.2. Externas

| Sistema | Protocolo | Operação | Autenticação | Timeout | Política de retry |
|---|---|---|---|---|---|
| | | | | | |

### 14.3. Filas / Celery (opcional)

- Tasks previstas, periodicidade (`celery beat`), idempotência, payload mínimo.

---

## 15. Performance, cache e otimização

- Consultas críticas listadas com QuerySet esperado e índices necessários.
- Estratégia de cache (Redis, `cache_page`, `cached_property`) por endpoint quando aplicável.
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

- **Estratégia**: big bang, gradual, feature flag (`django-waffle`, `django-flags`) ou canary.
- **Pré-requisitos de produção**: migrations aplicadas, variáveis de ambiente, índices criados, dados migrados.
- **Comunicação**: changelog interno, e-mail, banner no app.
- **Plano de rollback**: como reverter sem perda de dados (migrations reversíveis + flag desativável).

---

## 18. Plano de testes

### 18.1. Tipos de teste

- **Unitários**: services, managers, validators (pytest + pytest-django).
- **Integração**: views, forms, fluxos completos com `Django test Client`.
- **Migrations**: aplicar e reverter localmente; validar com `showmigrations`.
- **Performance**: `assertNumQueries` em listagens críticas.
- **Segurança**: testes que validam ausência de IDOR e respeito a permissões.
- **Acessibilidade**: checagem manual + ferramenta automatizada (axe, Lighthouse) em telas críticas.

### 18.2. Critérios mínimos

- Cobertura mínima por app impactado: `__%`.
- Todos os requisitos `obrigatorio` da seção 8 possuem teste correspondente.

### 18.3. Dados de teste

- Uso de `model_bakery` ou factories próprias.
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
- `.ia/docs/guides/testing.md`
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
