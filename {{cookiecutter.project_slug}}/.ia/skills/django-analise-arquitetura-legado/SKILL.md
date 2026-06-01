---
name: django-analise-arquitetura-legado
description: Realizar levantamento arquitetural completo de um projeto Django + PostgreSQL legado quando os documentos de `.ia/docs/architecture/` ainda não estão preenchidos. Skill intencionalmente específica de Django + PostgreSQL — heurísticas, parsing de `settings.py`/`INSTALLED_APPS`, migrations e detectores de PII são acoplados ao framework por design e não são reutilizáveis em outros stacks. Usar quando o projeto for integrado ao pacote de IA pela primeira vez, quando a equipe pedir análise inicial de arquitetura ou quando os documentos de arquitetura estiverem ausentes ou desatualizados. A coleta factual é feita pelo script `analyze_legacy_project.py`; o agente fica responsável pela síntese arquitetural a partir do relatório gerado.
---

# Objetivo
Produzir os quatro documentos de arquitetura em `.ia/docs/architecture/` com base em evidências estáticas confirmadas, separando o que é fato extraído por script do que é julgamento humano ou de IA.

# Fluxo

## 1. Coleta factual automatizada

Executar o script de análise estática:

```bash
rtk python .ia/skills/django-analise-arquitetura-legado/analyze_legacy_project.py \
  --project-path <caminho_do_projeto_django>
```

Opções úteis:

- `--dry-run`: apenas confirma que o projeto Django foi detectado, sem gerar relatório.
- `--print`: imprime o relatório em stdout em vez de gravar arquivo.
- `--output <caminho>`: grava o relatório no caminho informado.

O script gera `.ia/docs/reports/<data>-relatorio-analise-arquitetura.md` contendo:

1. dependências detectadas com versão e tópico
2. configurações de settings (`INSTALLED_APPS`, `AUTH_USER_MODEL`, `DEBUG`, `REST_FRAMEWORK`, `CELERY`, `CACHES`, `MIDDLEWARE`)
3. catálogo de apps com inventário de arquivos esperados por app
4. contagem de migrations e migrations com operações de risco
5. campos candidatos a LGPD por heurística de nome
6. candidatos a N+1 em views e serializers
7. avisos e limitações do script
8. lista de próximos passos para o agente

## 2. Revisão do relatório gerado

O agente deve:

1. Ler o relatório inteiro antes de tocar nos documentos de arquitetura.
2. Identificar lacunas — quando o script registrar `<referencia: NOME>` em `INSTALLED_APPS`, abrir o settings manualmente para resolver a referência.
3. Reabrir manualmente os arquivos quando uma heurística deixar dúvida (campo PII com nome genérico, view com `select_related` parcial, etc.).
4. Declarar como **premissa** qualquer afirmação que não puder ser confirmada por leitura de arquivo.

## 3. Complementação com leitura dirigida

Para itens fora do alcance do script, usar o checklist em `analise-arquitetura-legado.md` como referência. São itens que dependem de julgamento:

- inferência de domínio de negócio por app
- identificação de acoplamento indevido entre apps
- avaliação de qualidade dos testes existentes
- análise de fluxos principais de negócio
- mapeamento de integrações externas reais (apenas a presença de libs é detectada pelo script)

## 4. Preenchimento dos documentos canônicos

A partir do relatório + leitura complementar, preencher:

- `.ia/docs/architecture/overview.md`
- `.ia/docs/architecture/system-architecture.md`
- `.ia/docs/architecture/modules.md`
- `.ia/docs/architecture/security.md`

## 5. Abertura de task de análise

Criar e mover para `.ia/docs/tasks/done/` uma task de análise documentando:

- comando do script executado e timestamp
- caminho do relatório gerado
- premissas declaradas
- pontos de atenção consolidados
- arquivos atualizados em `.ia/docs/architecture/`
- itens que não foi possível confirmar sem execução do projeto

# Regras obrigatórias

- Não criar, alterar ou deletar nenhum arquivo de código-fonte do projeto analisado (`.py`, migrations, templates, static).
- Não executar `manage.py` nem nenhum comando que altere estado do banco ou do ambiente.
- Não instalar dependências no projeto analisado.
- Toda inferência que não puder ser confirmada por leitura direta de arquivo deve ser declarada explicitamente como premissa, nunca como fato.
- Se um arquivo esperado não existir, registrar a ausência — não inferir comportamento padrão silenciosamente.
- Se houver conflito entre dois arquivos ou padrões contraditórios, declarar o conflito — não resolver silenciosamente.
- O script `analyze_legacy_project.py` é a fonte de verdade para as evidências factuais; quando uma evidência for divergente do relatório, atualizar o relatório ou registrar a divergência na task.
- Seguir o checklist em `analise-arquitetura-legado.md` para itens não automatizados.

# Checklist de qualidade

- O script foi executado com sucesso e o relatório existe em `.ia/docs/reports/`.
- Todos os apps de `INSTALLED_APPS` reportados pelo script estão catalogados em `system-architecture.md`.
- Todos os campos sensíveis reportados pelo script foram revisados manualmente e estão em `security.md` com status de proteção atual.
- Todos os candidatos a N+1 e migrations de risco foram triados e classificados como atenção, falso positivo ou pendência.
- Nenhuma premissa ficou implícita — toda inferência está declarada como tal.
- Nenhum arquivo de código-fonte foi criado ou alterado.
- Os quatro arquivos de `.ia/docs/architecture/` foram criados ou atualizados.
- Existe task de análise em `.ia/docs/tasks/done/` com seção de premissas e pendências.

# Referências locais

- `.ia/skills/django-analise-arquitetura-legado/analyze_legacy_project.py` (coleta factual automatizada)
- `.ia/skills/django-analise-arquitetura-legado/analise-arquitetura-legado.md` (checklist detalhado de referência)
- `.ia/docs/architecture/overview.md`
- `.ia/docs/architecture/system-architecture.md`
- `.ia/docs/architecture/modules.md`
- `.ia/docs/architecture/security.md`
- `.ia/docs/guides/constraints.md`
- `.ia/docs/guides/patterns.md`
