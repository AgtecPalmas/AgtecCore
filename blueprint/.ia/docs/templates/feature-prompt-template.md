# Contexto obrigatório

- Siga rigorosamente AGENTS.md
- Respeite as restrições em .ia/docs/guides/constraints.md
- Arquitetura definida em .ia/docs/architecture/overview.md e .ia/docs/architecture/modules.md
- Estratégia de testes em .ia/docs/guides/testing.md

## Cenário

Estamos trabalhando no app Django <NOME_DO_APP>, seguindo o padrão modular descrito em .ia/docs/architecture/modules.md.

## Tarefa

Implementar a seguinte funcionalidade (descreva o objetivo de negócio e o fluxo esperado):

## Requisitos técnicos

- Endpoint DRF (<GET|POST|PUT|DELETE>) sob o prefixo /api/v1/, registrado no router do app.
- ViewSet/CBV com Fat Models.
- Validação via serializers/validators; use managers/querysets para regras de leitura.
- Evite N+1: use select_related/prefetch_related em queries.
- Tratamento de exceções padronizado via core.excecoes; respostas DRF coerentes.
- Autenticação/permite via dj-rest-auth + SimpleJWT; defina permissions explícitas.

## Escopo

- Alterar apenas arquivos do app <NOME_DO_APP> (migrations se necessário, pequenas e reversíveis).
- Não introduzir novas dependências.

## Entrega esperada

- Endpoint/ação no ViewSet/CBV exposto em /api/v1/.
- Serializer(s) e service/use_case correspondentes.
- Testes automatizados (pytest-django): domínio + API cobrindo fluxos e erros.

## Observações

- Explique decisões técnicas
- Aponte limitações ou melhorias futuras
- Sempre responda utilizando o idioma português (pt-BR)
