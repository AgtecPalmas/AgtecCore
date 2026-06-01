# Governanca de Rules IA (Multi-LLM)

## Objetivo

Definir o protocolo operacional para criacao, atualizacao, conflito e validacao de rules no projeto.

## 1) Modelo minimo de rule canonica

Toda rule canonica deve ter:

- `rule_id` unico
- `statement` verificavel
- camada de precedencia (`R0..R5`)
- fonte canonica
- status (`ativo`, `legado-controlado`, `deprecado`)
- `justification` (por que a regra existe)
- evidencia de repositorio (quando aplicavel)
- validacao minima (comando/check)

## 2) Protocolo de precedencia

- `R0` > `R1` > `R2` > `R3` > `R4` > `R5`
- Em conflito:
  1. registrar conflito (`rule_id` vs `rule_id`);
  2. manter a regra da camada superior;
  3. ajustar artefato de camada inferior;
  4. atualizar task/spec com a decisao e evidencias.

## 3) Protocolo de selecao de skills

Toda demanda deve explicitar:

- skill principal;
- skills complementares (se houver);
- `rule_id` usadas para justificar a escolha.

Em sobreposicao de skills:

1. priorizar skill do artefato final esperado;
2. usar skill mais especializada como principal;
3. evitar duplicidade de checklist;
4. resolver conflito por precedencia `R0..R5`;
5. registrar desempate na task/spec.

Fonte canônica da matriz:

- `AGENTS.md`
- `.ia/docs/guides/skills-decision.md`

## 4) Protocolo para regras legadas

Quando uma regra alvo divergir do estado real do codigo:

1. classificar como `legado-controlado`;
2. anexar evidencia concreta (arquivo/trecho);
3. definir regra de nao expansao do legado;
4. planejar convergencia em spec/task propria.

Exemplo atual:

- `RULE-EXC-001` (acesso direto a DB em `authentication/routers.py`) esta em `legado-controlado`.

## 5) Rule Quality Gate (obrigatorio por demanda de IA)

Checklist minimo:

- [ ] precedencia aplicada (`R0..R5`);
- [ ] `rule_id` relevantes citadas na decisao;
- [ ] skill principal definida e coerente com a intencao;
- [ ] desempate registrado quando houver sobreposicao de skills;
- [ ] sem referencias quebradas nos artefatos ativos;
- [ ] sem conflito textual ativo nao resolvido;
- [ ] excecoes legadas documentadas (se houver);
- [ ] comandos de validacao registrados na task.

## 6) Comandos de validacao sugeridos

```bash
rg -n "RULE-[A-Z]+-[0-9]+" AGENTS.md .ia/**/*.md
```

```bash
rg -n "Matriz intenção -> skill principal|Protocolo de desempate de skills|skills-decision.md" \
AGENTS.md .ia/docs/guides/skills-decision.md .ia/skills/*/SKILL.md
```

```bash
rg -n "^##\\s+Padr[aã]o" .ia/skills/*/SKILL.md
```

```bash
rg -n "\\.github/copilot-instructions\\.md|\\.github/instructions/ia-agent\\.instructions\\.md|tasks/flutter" \
AGENTS.md .ia/docs/guides/constraints.md .ia/docs/guides/project-context.md \
.ia/docs/guides/patterns.md .ia/docs/guides/regra-endpoint-filiado-autenticado.md \
.ia/docs/architecture/*.md .ia/docs/testing/strategy.md \
.ia/docs/templates/*.md .ia/skills/*/SKILL.md
```

## 7) Responsabilidade

- Fonte normativa: `AGENTS.md` (`R0`)
- Catalogo canonico: `.ia/docs/guides/rules-catalog.md`
- Matriz de decisao de skills: `.ia/docs/guides/skills-decision.md`
- Governanca operacional: este documento
