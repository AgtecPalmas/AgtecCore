# Template — Integração Flutter (padrão do projeto)

> Template canônico consumido pela skill `spec-integracao-flutter`.

## Contexto obrigatório (não pular)

- Siga rigorosamente `AGENTS.md`.
- Respeite restrições e protocolo anti-alucinação em `.ia/docs/guides/constraints.md`.
- Siga padrões em `.ia/docs/guides/patterns.md` (inclui regra "não inventar outro jeito", especialmente para Dio).
- Aplique a governança/catálogo de rules em `.ia/docs/guides/rules-governance.md` e `.ia/docs/guides/rules-catalog.md`.
- Contexto do projeto: `.ia/docs/guides/project-context.md`.
- Se existir spec Flutter relacionada, referenciar explicitamente em `.ia/docs/specs/`.

Regras:

- Não inventar nova forma de chamar API com Dio; seguir o padrão existente no app.
- Não alterar camada de DTO/models do app Flutter sem requisito explícito.
- Se faltar referência do design system (Figma/tokens/lib), pedir o link e não improvisar UI/estilos.

## Cenário

- Módulo/feature no Flutter: `<NOME_DO_MODULO_FLUTTER>`
- Módulo/rota no backend: `<NOME_DO_MODULO_BACKEND>`
- Objetivo: `<OBJETIVO_DA_INTEGRACAO>`
- Referências no app (obrigatório): `<CAMINHOS_DE_SERVICE/CONTROLLER_EXISTENTES>`

## Endpoints (fonte de verdade)

Liste os endpoints do backend e seus contratos, copiando da spec ou do OpenAPI do projeto:

- Base URL: `<BASE>` (ex.: `/api/v1/<modulo>/`)
- Endpoints:
  - `<METODO> <PATH>` → response `<DTO/CONTRATO>`

## Regras de integração (não negociar)

- Dio:
  - Usar o mesmo wrapper/instância e padrão de chamadas existente.
  - Manter padrão de retorno (ex.: `Either<Exception, T>`) e mensagens de erro coerentes.
  - Paginação: seguir o padrão do projeto (offset/limit e next/previous quando aplicável).
- Controller:
  - Manter padrão de estados (loading/error/success) já existente no módulo.
  - Logging: seguir padrão do projeto (ex.: AppLogger) quando já adotado.
- DTOs:
  - Consumir contratos existentes; não criar DTO paralelo.
  - Só criar/alterar DTO se o backend mudou o contrato (com evidência).
- Design system:
  - Usar componentes/tokens existentes; sem criar "mini design system".

## Checklist de implementação (service/controller)

### Service

- [ ] Criar métodos por endpoint:
  - Nome: `<nome>` (ex.: `fetchPaginated`, `search`, `updateStatusX`)
  - Método HTTP: `<GET|POST|PATCH|PUT|DELETE>`
  - Path: `<path>`
- [ ] Montar URL seguindo o padrão do projeto (base + path; paginação respeitando `urlPage` quando existir).
- [ ] Tratar erros seguindo o padrão do módulo (mensagens e exceptions).
- [ ] Converter response para o model existente (`fromMap`/mapeamento padrão do projeto).

### Controller

- [ ] Orquestrar chamada do service mantendo padrão de states.
- [ ] Atualizar lista/state/UI após sucesso.
- [ ] Tratar vazio/erro com as mensagens e estados adotados.

## Perguntas de esclarecimento (se faltar contexto)

- Qual é o código de referência no app que define o padrão Dio/`Either`?
- Quais módulos do app são a referência obrigatória (ex.: `<modulo_principal>/<submodulo>`)?
- Qual design system devemos seguir (link/arquivo)?

## Fontes consultadas

- `<LISTAR_PATHS_DO_REPO_E_DO_APP_FLUTTER_SE_DISPONIVEL>`

## Rules aplicadas

- `<LISTAR_RULE_IDS_EX.: RULE-ROUTE-001, RULE-ANTIHAL-001>`

## Assunções (se houver)

- `<LISTAR_ASSUNCOES>`

## Saída esperada da IA

- Lista objetiva de métodos a criar/alterar (service/controller) com assinatura e endpoint correspondente.
- Notas de tratamento de erro e paginação seguindo padrão existente.
- Lista de arquivos a tocar (paths).
