---
name: spec-integracao-flutter
description: Cria uma especificação técnica de integração entre um módulo FastAPI do Argus e o cliente Flutter Web. Usar quando o usuário pedir explicitamente para criar uma spec de integração Flutter web/mobile, spec flutter, integração flutter, flutter mobile, flutter web.
---

# Objetivo
Gerar specs de integração Flutter focadas no contrato HTTP consumido pelo cliente, sem expor detalhes internos desnecessários da implementação backend.

# Regras obrigatórias
- Regra global: nenhuma skill pode criar, editar, mover ou remover arquivos sob `argus_ia_agent/`; demandas nesse módulo devem ser tratadas como análise, especificação, backlog ou orientação operacional, sem implementação direta nesse diretório.
- A spec deve refletir apenas contratos confirmados em routers, schemas ou OpenAPI.
- Não incluir detalhes internos de implementação backend no artefato final de integração.
- Usar o template canônico `.ia/docs/templates/integracao-flutter.md`.
- Nomear novas specs com data `DD-MM-YYYY`.

## Pré-requisitos

Antes de gerar a spec:
1. Ler os arquivos do módulo alvo: `<modulo>/routers.py`, `<modulo>/schemas.py`
2. Verificar prefixo de rota real do módulo em `core/routers.py` ou no agregador do módulo
3. Confirmar autenticação: `core/security.py` e os `Depends` nos routers
4. Para endpoints com contexto de filiado autenticado, aplicar `.ia/docs/guides/regra-endpoint-filiado-autenticado.md`
5. Criar o arquivo de spec em `.ia/docs/specs/flutter/<dominio>-<descricao-curta>-flutter-spec-DD-MM-YYYY.md`

## Guard rails

1. **NUNCA** incluir no arquivo de especificação referências aos arquivos do backend (ex: `routers.py`, `schemas.py`) ou detalhes de implementação. A spec é um contrato de integração, não um guia de implementação.
2. **NUNCA** mencionar o nome do framework (FastAPI) ou tecnologias específicas do backend. A spec deve ser agnóstica à implementação, focada apenas no contrato de API.
3. **NUNCA** incluir detalhes de autenticação que não sejam relevantes para o cliente Flutter (ex: tipos de tokens, fluxos de refresh). Basta indicar se o endpoint requer autenticação ou não.
4. **NUNCA** incluir campos ou comportamentos que não estejam explicitamente definidos nos endpoints do módulo. A spec deve refletir fielmente o contrato da API, sem suposições ou extrapolações.
5. **NUNCA** incluir detalhes de erros que não sejam explicitamente definidos nos endpoints (ex: mensagens de erro específicas, códigos de status além dos comuns 4xx). A spec deve se limitar a indicar os status de erro possíveis, sem entrar em detalhes de implementação.

## Estrutura da spec a ser gerada

Unifique o conteúdo do markdown abaixo com o template canônico `.ia/docs/templates/integracao-flutter.md`

```markdown

## Autenticação

Descrever o mecanismo de autenticação:
- Header obrigatório: `Authorization: Bearer <token>`
- Token obtido via: `POST /api/v1/auth/login/`
- Endpoints que NÃO requerem autenticação (se houver): listar explicitamente

## Endpoints

### [VERBO] /api/v1/<modulo>/<path>/

**Descrição:** O que o endpoint faz.  
**Autenticação:** ✅ Obrigatória / ❌ Não requerida  
**Permissão:** `<modulo>.<acao>_<modelo>` (se aplicável)  

#### Request

**Headers:**
\`\`\`
Authorization: Bearer <token>
Content-Type: application/json
\`\`\`

**Query params** (se aplicável):
| Parâmetro | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `page` | int | Não | Página (default: 1) |

**Payload (Body):**
\`\`\`json
{
  "campo": "valor_exemplo"
}
\`\`\`

**Campos do payload:**
| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `campo` | string | Sim | Descrição do campo |

#### Response

**Status:** `200 OK`

\`\`\`json
{
  "id": "uuid-exemplo",
  "campo": "valor",
  "created_at": "2026-01-01T00:00:00Z"
}
\`\`\`

**Campos da resposta:**
| Campo | Tipo | Descrição |
|---|---|---|
| `id` | UUID | Identificador único |

**Erros possíveis:**
| Status | Descrição |
|---|---|
| `401` | Token ausente ou inválido |
| `403` | Sem permissão para a operação |
| `404` | Recurso não encontrado |
| `422` | Payload inválido (validação Pydantic) |

---

[repetir seção para cada endpoint, caso aplicável]

```

## Convensões do projeto a aplicar na spec

- Prefixo global de rotas: `/api/v1/`
- Paths em kebab-case com barra final: `/fetch-paginated/`, `/create/`, `/update/`
- Datas em ISO 8601: `"2026-01-01T00:00:00Z"`
- IDs em UUID v4: `"3fa85f64-5717-4562-b3fc-2c963f66afa6"`
- Paginação via query params: `limit`, `offset` (verificar `FilterPagination` em `core/schemas.py`)
- Soft delete: campo `deleted: bool` — endpoints de listagem retornam apenas `deleted=false` por padrão
- Autenticação: JWT Bearer via `Authorization` header

## Exemplo de spec de resposta paginada

```json
{
    "count": 15,
    "next": "https://11.11.0.112:8001/api/v1/agenda/evento/fetch-paginated/?offset=5&limit=5",
    "previous": null,
    "results": [
        {
            "id": "c3b484ce-738a-4c39-83ac-dbe9227b25fe",
            ...
        },
        {
            "id": "4820b17b-f0d2-4e80-81f7-817029699241",
            ...
        },
        {
            "id": "196dfda9-feda-45fa-b95f-d2b5aa4521e9",
            ...
        },
        {
            "id": "79d46443-2add-409a-ab5a-9922949d99b6",
            ...
        }
    ]
}
```
