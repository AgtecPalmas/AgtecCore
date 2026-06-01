# Ferramentas de Agente e Ambiente

Este guia concentra material operacional de ferramentas especificas usadas junto do projeto. Ele **nao** define regras canonicas do repositório; as regras do projeto continuam em `AGENTS.md` e nos arquivos de `.ia/docs/`.

Use este guia quando precisar configurar ou operar um ambiente de desenvolvimento assistido por IA. Se a ferramenta mudar, este arquivo pode ser atualizado sem alterar o nucleo da governanca.

## Escopo deste guia

Este documento cobre apenas:

- exemplos de setup de ambiente
- detalhes de ferramentas de terminal assistido
- configuracoes opcionais de produtividade
- referencias externas de instalacao

Este documento nao substitui:

- `AGENTS.md`
- `.ia/docs/architecture/`
- `.ia/docs/guides/`
- `.ia/skills/`

## Ferramentas atualmente documentadas

### OpenCode

Pode ser usado como terminal assistido por IA para ler `AGENTS.md`, carregar skills e operar o repositório. Quando utilizar OpenCode, siga a documentacao oficial da ferramenta e configure o ambiente para abrir na raiz do projeto.

Referencias:

- https://opencode.ai/docs
- https://opencode.ai/docs/config

### RTK

RTK pode ser usado para reduzir ruido de saida de comandos shell durante sessoes com agentes.

Referencias:

- https://github.com/rtk-ai/rtk

### Caveman

Caveman pode ser usado como camada opcional de compressao de comunicacao em ferramentas que suportem esse fluxo.

Referencias:

- https://github.com/JuliusBrussee/caveman

## Regra de manutencao

Se surgir conteudo detalhado de uma ferramenta especifica, ele deve entrar aqui ou em arquivo equivalente dedicado, e nao no README principal de `.ia/`.
