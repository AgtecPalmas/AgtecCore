# Decisao de Skills para Agentes IA (Multi-LLM)

## Objetivo

Definir o protocolo de desempate entre skills e o checklist de validacao de selecao.

> A **matriz canonica de intencao → skill** esta em `AGENTS.md` (R0).
> Consulte-a como fonte primaria. Este guia complementa apenas com protocolo de
> desempate e checklist de qualidade.

Este guia complementa:

- `AGENTS.md` (fonte normativa R0 — inclui a matriz de intencao → skill)
- `.ia/docs/guides/rules-catalog.md` (catalogo de `rule_id`)
- `.ia/docs/guides/rules-governance.md` (protocolo de conflito/validacao)
- `.ia/README.md` (roteamento rapido: intencao → skill + rules + arquivos)

## Regras aplicaveis

- `RULE-GOV-001`: precedencia oficial `R0..R5`.
- `RULE-ONESHOT-001`: preservar padroes One-Shot por camada e exemplos `## Padrao ...` em skills.
- `RULE-MULTILLM-001`: manter artefatos vendor-neutral, sem lock-in.

## Protocolo de desempate entre skills

Quando mais de uma skill parecer aplicavel:

1. Priorizar a skill que corresponde ao artefato final esperado.
2. Se persistir empate, priorizar a skill com menor escopo e maior especializacao.
3. Usar as demais como complementares, sem duplicar checklist.
4. Em conflito de instrucao, resolver por precedencia `R0..R5`.
5. Registrar o desempate na task/spec.

## Regras de ouro para uso de skills

- Nao aplicar skill de modulo IA quando a demanda nao for explicitamente de IA.
- Nao usar mais de 1 skill principal na mesma etapa.
- Nao eliminar exemplos de codigo em secoes `## Padrao ...`.
- Nao transformar workflow de skill em regra global sem passar pelo catalogo de rules.

## Evidencias minimas na task/spec

- Skill principal escolhida e motivacao.
- Skills complementares (se houver) e motivo.
- `rule_id` usadas para justificar a escolha.
- Registro do desempate (quando houver).

## Checklist de validacao

- [ ] Skill principal definida e coerente com a intencao.
- [ ] Skills complementares sem sobreposicao redundante.
- [ ] `rule_id` citadas na decisao.
- [ ] Desempate registrado (quando aplicavel).
- [ ] Sem violar restricoes de escopo (ex.: mapear IA fora de demanda IA).
