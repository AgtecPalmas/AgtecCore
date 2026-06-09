---
name: nova-tool-ia
description: Cria uma nova tool assíncrona no módulo de IA do projeto. Use quando o usuário pedir para adicionar uma tool de domínio, consulta ao banco ou transformação de dados para um agente. Também ativa automaticamente quando o contexto menciona "nova tool", "tool para o agente", "adicionar ferramenta IA" ou arquivos no módulo de agentes do projeto.
---

# Nova Tool — Módulo de IA

# Objetivo
Criar tools assíncronas de leitura para agentes do módulo de IA do projeto, preservando contratos de rota existentes e isolamento do módulo.

# Regras obrigatórias
- Nunca modificar rotas de contrato público sem task/spec explícita.
- Nunca criar schemas para módulos internos do módulo de IA.
- Nunca modificar models, routers ou schemas fora do módulo de IA.
- Tool deve ser assíncrona e somente leitura.
- Não alterar arquivos do módulo de IA sem autorização explícita em task aprovada.

## Pré-requisitos

Antes de começar:
1. Ler `.ia/docs/architecture/ia_modules.md` (regras mandatórias e padrão de extensão)
2. Ler `.ia/docs/architecture/relatorio-arquitetural.md` (fonte de verdade)
3. Identificar o módulo de domínio que a tool irá cobrir
4. Criar arquivo de task em `.ia/docs/tasks/todo/task-DD-MM-YYYY-<hash_alfanumerico_10>.md` antes de implementar

## Estrutura obrigatória produzida

```
<modulo_ia>/agent_agno/tools/<nome_modulo>.py        # implementação da tool
<modulo_ia>/agent_agno/skills/<nome_modulo>/         # skill do agente (se ainda não existir)
tests/tests_<modulo_ia>/test_<nome_modulo>_tool.py   # testes automatizados
```

## Checklist de implementação

- [ ] Criar `<modulo_ia>/agent_agno/tools/<nome_modulo>.py` com a tool assíncrona
- [ ] Tool deve ser somente leitura (nunca escrever no banco)
- [ ] Registrar a tool no agente especializado correspondente
- [ ] Verificar se o Team/orquestrador precisa ser atualizado
- [ ] Criar diretório de skills do agente se não existir
- [ ] Criar testes automatizados
- [ ] Confirmar que rotas de contrato público **não foram modificadas**
- [ ] Confirmar que nenhum arquivo fora do módulo de IA foi alterado

## Regras mandatórias (não violar)

1. Nunca modificar rotas de contrato público
2. Nunca criar schemas para módulos internos do módulo de IA
3. Nunca modificar models, routers ou schemas fora do módulo de IA
4. Tool sempre assíncrona (`async def`)

## Padrão de tool assíncrona

```python
@tool
async def nome_da_tool(run_context: RunContext, parametro: str) -> str:
    """Descrição do que a tool faz."""
    db = run_context.db_session
    # consulta de leitura apenas
    resultado = await db.execute(...)
    return str(resultado)
```

## Referências de código

- Arquitetura do módulo de IA: `.ia/docs/architecture/ia_modules.md`
- Relatório arquitetural: `.ia/docs/architecture/relatorio-arquitetural.md`
