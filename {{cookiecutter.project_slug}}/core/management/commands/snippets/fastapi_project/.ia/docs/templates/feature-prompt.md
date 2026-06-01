# Contexto obrigatório

- Siga rigorosamente `AGENTS.md`.
- Respeite as restrições em `.ia/docs/guides/constraints.md`.
- Arquitetura definida em `.ia/docs/architecture/overview.md` e `.ia/docs/architecture/modules.md`.
- Estratégia de testes em `.ia/docs/testing/strategy.md`.

## Cenário

Estamos trabalhando no módulo FastAPI `<NOME_DO_MODULO>`, seguindo o padrão modular descrito em `.ia/docs/architecture/overview.md`.

## Tarefa

Implementar a seguinte funcionalidade (descreva o objetivo de negócio, contrato HTTP e fluxo esperado):

## Requisitos técnicos

- Endpoint FastAPI (`<GET|POST|PUT|PATCH|DELETE>`) sob o prefixo `/api/v1/`, registrado no `routers.py` do módulo.
- Router fino → schema Pydantic + use case/service contendo regras.
- Type hints obrigatórios em helpers, services, use cases e dependências.
- Validação via schemas Pydantic e validators; use consultas SQLAlchemy compatíveis com sessão sync/async existente.
- Evite N+1: use eager loading/joins adequados quando houver relacionamentos.
- Tratamento de exceções coerente com os padrões existentes em `core/exception_handlers.py` e `core/exceptions.py`.
- Autenticação/autorização via dependências existentes em `authentication/security.py` quando aplicável.

## Escopo

- Alterar apenas arquivos do módulo `<NOME_DO_MODULO>` e testes relacionados, salvo dependência explícita aprovada.
- Não introduzir novas dependências sem task/spec aprovada.
- Não alterar `core/` sem autorização explícita.

## Entrega esperada

- Endpoint/ação exposto no router FastAPI.
- Schema(s) Pydantic e use case/service correspondentes.
- Testes automatizados com pytest/pytest-asyncio cobrindo fluxos principais e erros.

## Observações

- Explique decisões técnicas.
- Aponte limitações ou melhorias futuras.
- Sempre responda utilizando o idioma português (pt-BR).