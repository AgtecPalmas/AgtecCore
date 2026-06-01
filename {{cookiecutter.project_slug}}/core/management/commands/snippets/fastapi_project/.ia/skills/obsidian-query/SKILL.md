---
name: obsidian-query
description: Usar quando o usuário perguntar sobre histórico, tarefas, specs, runbooks, decisões ou contexto de implementação do sistema. Resposta vem primeiro do vault Obsidian; fallback para o repositório somente se o vault não responder. Ativa em frases como "qual a última tarefa", "o que implementamos", "última spec", "buscar no cofre", "consultar obsidian".
---

# Objetivo

Responder perguntas sobre estado, histórico ou documentação do sistema consultando primeiro o vault Obsidian `DevBrain` e, somente em fallback, o repositório local. Informar claramente a fonte usada (`vault` ou `repositório`).

# Regra principal

1. Consultar primeiro o vault `DevBrain`.
2. Só consultar o repositório se o vault não trouxer resposta suficiente.
3. Informar claramente a fonte usada: `vault` ou `repositório`.
4. Usar o mesmo contrato de configuração do `obsidian-sync`: `OBSIDIAN_DEV_VAULT`/`DEVBRAIN_VAULT` e, opcionalmente, `OBSIDIAN_DEV_SYSTEM_NAME`/`DEVBRAIN_SYSTEM_NAME`.

# Como executar

```bash
rtk python .ia/skills/obsidian-query/query_devbrain.py \
  --query "Qual a ultima tarefa que implementamos?"
```

Com sistema explícito:

```bash
rtk python .ia/skills/obsidian-query/query_devbrain.py \
  --system-name "Argus FastAPI" \
  --query "Qual a ultima tarefa que implementamos?"
```

Com vault explícito:

```bash
rtk python .ia/skills/obsidian-query/query_devbrain.py \
  --vault /caminho/absoluto/do/vault \
  --query "Quais specs recentes existem?"
```

# Uso esperado

Perguntas comuns:

1. última tarefa implementada
2. última spec criada
3. tarefas em aberto
4. contexto de integração
5. notas de runbook
6. histórico operacional

# Saída esperada

O script deve indicar:

1. fonte da resposta
2. arquivo principal encontrado
3. título resumido
4. trecho relevante
5. alternativas, quando houver

# Regras obrigatórias
- Regra global: nenhuma skill pode criar, editar, mover ou remover arquivos sob `argus_ia_agent/`; demandas nesse módulo devem ser tratadas como análise, especificação, backlog ou orientação operacional, sem implementação direta nesse diretório.

- Sempre indicar a fonte (`vault` ou `repositório`).
- Não devolver conteúdo do repositório quando o vault tiver respondido com nível de confiança suficiente.
- Se `--system-name` não for informado, tentar `OBSIDIAN_DEV_SYSTEM_NAME`/`DEVBRAIN_SYSTEM_NAME` e, na ausência desses valores, buscar em todos os sistemas conhecidos do vault antes de cair para o repositório.
- Não inventar conteúdo: se nem vault nem repositório responderem, declarar lacuna explicitamente.
- Não expor credenciais ou caminhos pessoais nos resultados.
