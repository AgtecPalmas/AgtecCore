---
name: novo-agente-ia
description: Cria um novo agente especialista no módulo de IA do projeto. Use quando o usuário pedir para adicionar um novo agente de domínio, especialista IA para um módulo, ou integrar um novo módulo ao orquestrador. Também ativa automaticamente quando o contexto menciona "novo agente", "agente especialista", "adicionar agente IA" ou arquivos no diretório de agentes do módulo de IA.
---

# Novo Agente Especialista — Módulo de IA

# Objetivo
Criar agentes especialistas para o módulo de IA do projeto, integrando tools, skills de domínio e registro no orquestrador sem alterar contratos públicos existentes.

# Regras obrigatórias
- Nunca modificar rotas de contrato público sem task/spec explícita.
- Nunca criar schemas no módulo de IA para outros módulos.
- Nunca modificar models, routers ou schemas de outros módulos.
- Registrar o agente no orquestrador e criar teste de validação manual.
- Não alterar arquivos do módulo de IA sem autorização explícita em task aprovada.

## Pré-requisitos

Antes de começar:
1. Ler `.ia/docs/architecture/ia_modules.md` (arquitetura completa do módulo de IA)
2. Ler `.ia/docs/architecture/relatorio-arquitetural.md` (fonte de verdade)
3. Confirmar: qual módulo de domínio será coberto?
4. Criar arquivo de task em `.ia/docs/tasks/todo/task-DD-MM-YYYY-<hash_alfanumerico_10>.md`

## Estrutura obrigatória produzida

```
<modulo_ia>/agent_agno/agents/<nome_modulo>.py       # definição do agente especialista
<modulo_ia>/agent_agno/skills/<nome_modulo>/         # diretório de skill do agente
<modulo_ia>/agent_agno/skills/<nome_modulo>/SKILL.md # conhecimento operacional do domínio
<modulo_ia>/agent_agno/tools/<nome_modulo>.py        # tools de leitura do domínio
tests/tests_<modulo_ia>/test_<nome_modulo>_agent.py  # testes automatizados
```

## Checklist de implementação

- [ ] Criar o agente especialista
- [ ] Criar skills de domínio para o agente
- [ ] Criar tools de leitura do domínio
- [ ] Registrar o novo agente no orquestrador (Team)
- [ ] Criar testes automatizados
- [ ] Confirmar que rotas de contrato público **não foram modificadas**
- [ ] Confirmar que nenhum arquivo fora do módulo de IA foi alterado

## Regras mandatórias (não violar)

1. Nunca modificar rotas de contrato público
2. Nunca criar schemas no módulo de IA para outros módulos
3. Nunca modificar models, routers ou schemas de outros módulos
4. O agente deve ser registrado no orquestrador como membro

## Padrão de agente especialista

```python
<nome_modulo>_agent = Agent(
    name="<NomeModulo>Agent",
    description="Agente especialista em <descricao do dominio>.",
    tools=[nome_da_tool],
)
```

## Referências de código

- Arquitetura do módulo de IA: `.ia/docs/architecture/ia_modules.md`
- Relatório arquitetural: `.ia/docs/architecture/relatorio-arquitetural.md`
