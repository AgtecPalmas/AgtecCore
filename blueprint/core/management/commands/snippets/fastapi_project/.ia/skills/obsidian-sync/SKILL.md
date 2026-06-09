---
name: obsidian-sync
description: Sincronizar o repositório atual com o vault Obsidian DevBrain. Usar quando o usuário pedir "obsidian-sync", "sincronizar obsidian" ou quiser exportar o contexto do repositório para o DevBrain.
---

# Objetivo

Sincronizar o repositório atual com o vault `DevBrain` do Obsidian, publicando o contexto operacional do projeto em `01-Sistemas/<Sistema>/` via exportador local oficial.

# O que faz

1. Executa o exportador local em `.ia/skills/obsidian-sync/export_devbrain.py`.
2. Sincroniza o projeto em `01-Sistemas/<Sistema>/` dentro do vault.
3. Atualiza as notas operacionais principais do sistema.
4. Usa `OBSIDIAN_DEV_VAULT`/`DEVBRAIN_VAULT` como fonte padrão do vault e aceita `OBSIDIAN_DEV_SYSTEM_NAME`/`DEVBRAIN_SYSTEM_NAME` para o nome do sistema.

# Como executar

Da raiz do repositório:

```bash
rtk python .ia/skills/obsidian-sync/export_devbrain.py
```

Nesse modo, o script usa:

1. `OBSIDIAN_DEV_VAULT` ou `DEVBRAIN_VAULT` para localizar o vault.
2. `OBSIDIAN_DEV_SYSTEM_NAME` ou `DEVBRAIN_SYSTEM_NAME` para o sistema, quando configurados.
3. O nome do diretório do repositório como fallback para derivar o sistema.

Com parâmetros explícitos:

```bash
rtk python .ia/skills/obsidian-sync/export_devbrain.py \
  --project-path /caminho/absoluto/do/repo \
  --vault /caminho/absoluto/do/vault \
  --system-name NomeDoSistema
```

# Pré-condições

O repositório deve conter:

1. `.ia/skills/obsidian-sync/export_devbrain.py`
2. Raiz do repositório legível
3. Arquivos-fonte necessários pelo exportador

Se o exportador não existir, interromper e informar que o repositório não está preparado para sincronização com o DevBrain.

# Saída esperada

Após execução, verificar as notas principais:

1. `01-Sistemas/<Sistema>/00-Visao-Geral.md`
2. `01-Sistemas/<Sistema>/03-Runbooks.md`
3. `01-Sistemas/<Sistema>/08-Agentes.md`
4. `01-Sistemas/<Sistema>/09-Integracoes.md`

# Regras obrigatórias
- Regra global: nenhuma skill pode criar, editar, mover ou remover arquivos sob o módulo de IA/agentes do projeto (se existir); demandas sobre esse módulo devem ser tratadas como análise, especificação, backlog ou orientação operacional, sem implementação direta nesse diretório.

- Preferir o exportador local. Não duplicar lógica de sincronização dentro da skill — apenas orquestrar a execução do script.
- Não sobrescrever o vault sem antes confirmar o caminho resolvido (variáveis de ambiente ou parâmetros explícitos).
- Interromper imediatamente se o exportador estiver ausente ou se os arquivos-fonte esperados não existirem na raiz do repositório.
- Não expor credenciais ou caminhos pessoais nos artefatos publicados no vault.
