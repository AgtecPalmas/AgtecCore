---
name: refatorar-modulo
description: Refatora um módulo existente do Argus para alinhar com os padrões arquiteturais vigentes (CoreBase, BaseUseCases, Pydantic v2, async). Use quando o usuário pedir para refatorar, modernizar, ou corrigir padrões em um módulo FastAPI existente. Também ativa automaticamente quando o contexto menciona "refatorar", "modernizar", "padronizar módulo" ou "alinha ao padrão".
---

# Refatorar Módulo — Argus

# Objetivo
Refatorar módulos FastAPI existentes para os padrões arquiteturais vigentes, reduzindo regressão e mantendo contratos públicos estáveis.

# Regras obrigatórias
- Regra global: nenhuma skill pode criar, editar, mover ou remover arquivos sob `argus_ia_agent/`; demandas nesse módulo devem ser tratadas como análise, especificação, backlog ou orientação operacional, sem implementação direta nesse diretório.
- Ler o módulo alvo por completo antes de propor mudanças.
- Aguardar aprovação antes de implementar refatorações.
- Não alterar nomes de tabelas, endpoints em produção ou lógica de negócio sem aprovação explícita.
- Implementar por camadas e testar cada etapa relevante.

## Pré-requisitos

Antes de começar:
1. Ler `.ia/docs/guides/rules-catalog.md` (rules canônicas e `rule_id`)
2. Ler `.ia/docs/guides/patterns.md` (padrões obrigatórios)
3. Ler `.ia/docs/architecture/relatorio-arquitetural.md` (fonte de verdade)
4. Ler `.ia/docs/guides/regra-endpoint-filiado-autenticado.md` se o modulo tiver endpoints com contexto de filiado logado
5. Ler o módulo alvo por completo antes de propor mudanças
6. Criar task em `.ia/docs/tasks/todo/task-DD-MM-YYYY-<hash_alfanumerico_10>.md`
7. **Aguardar aprovação antes de implementar** — refatorações têm risco de regressão

## Checklist de avaliação (antes de refatorar)

- [ ] Model herda de `CoreBase`? (se não: refatorar)
- [ ] Model redeclara `id`, `deleted`, `created_at`, `updated_at`, `enabled`? (se sim: remover)
- [ ] Use case herda de `BaseUseCases`? (se não: refatorar)
- [ ] Use case tem instância singleton ao final do arquivo? (se não: adicionar)
- [ ] Schemas seguem hierarquia `Base` → `Create` → `Update` → `InDBBase`? (se não: refatorar)
- [ ] Schemas usam `ConfigDict(from_attributes=True)` no `InDBBase`? (se não: adicionar)
- [ ] Router contém lógica de negócio? (se sim: mover para use case)
- [ ] Router usa `Depends(security.has_permission(...))` para proteger rotas? (se não: adicionar)
- [ ] Funções I/O são assíncronas (`async def`)? (se não: refatorar)
- [ ] Paths das rotas estão em kebab-case? (se não: corrigir)
- [ ] Política de barra final respeita novo vs legado? (se não: alinhar sem quebrar contrato)
- [ ] Endpoint self-service de filiado recebe `filiado_id`? (se sim: remover da assinatura HTTP)
- [ ] Resolução de filiado está no use case via `get_filiado_by_auth_user`? (se não: refatorar)

## O que não mudar sem aprovação explícita

- Nomes de tabelas do banco (requer migration)
- Nomes de endpoints já em produção (quebra clientes)
- Lógica de negócio durante refatoração estrutural
- Qualquer arquivo fora do módulo alvo

## Padrão de nomenclatura de rotas

| Operação | Path correto |
|---|---|
| Listar com paginação | `/fetch-paginated/` |
| Buscar por ID | `/fetch-by-id/` |
| Buscar por campo | `/fetch-by-<campo>/` |
| Busca full-text | `/search/` |
| Criar | `/create/` |
| Atualizar | `/update/` |
| Deletar (soft) | `/delete/` |
| Restaurar | `/restore/` |

## Migração Pydantic v1 → v2

| v1 | v2 |
|---|---|
| `class Config: orm_mode = True` | `model_config = ConfigDict(from_attributes=True)` |
| `NomeSchema.from_orm(obj)` | `NomeSchema.model_validate(obj)` |
| `schema.dict()` | `schema.model_dump()` |
| `validator` decorator | `field_validator` / `model_validator` |
| `Optional[str]` sem default | `Optional[str] = None` |

## Processo de refatoração seguro

1. **Ler** todo o módulo antes de qualquer mudança
2. **Listar** todas as diferenças em relação ao padrão
3. **Propor plano** de refatoração com escopo claro
4. **Aguardar aprovação** do plano
5. **Implementar** uma camada por vez (models → schemas → use_cases → routers)
6. **Testar** cada etapa antes de avançar
7. **Atualizar** a task com o que foi feito

## Referências de código

- Padrões: `.ia/docs/guides/patterns.md`
- CoreBase: `core/database.py`
- BaseUseCases: `core/use_cases.py`
- Segurança: `core/security.py`
- Módulo de referência bem estruturado: `usuario/`, `filiado/`
