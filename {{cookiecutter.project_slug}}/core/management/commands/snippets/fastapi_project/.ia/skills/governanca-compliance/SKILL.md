---
name: governanca-compliance
description: Validar a governança documental e operacional de agentes em `AGENTS.md` e `.ia/`, detectando placeholders, status inválidos, referências quebradas, hardcodes pessoais, documentos duplicados, menções a stack obsoleta em `AGENTS.md`, divergências essenciais entre skills e catálogos, e regressões do contrato `DD-MM-YYYY`/status em inglês. Usar quando o desenvolvedor pedir auditoria automatizada de governança ou antes de consolidar mudanças amplas em `.ia/`.
---

# Objetivo
Detectar regressões de governança em `AGENTS.md` e `.ia/` antes de consolidar mudanças, mantendo naming, status, referências, skills, templates e automações alinhados ao contrato canônico do projeto.

# Fluxo
1. Executar `rtk python .ia/skills/governanca-compliance/check_ia_governance.py`.
2. Ler os findings retornados por categoria.
3. Corrigir os problemas encontrados ou registrar bloqueios conhecidos.
4. Reexecutar o comando até que o resultado esperado para a etapa seja atingido.

# Regras obrigatórias
- Regra global: nenhuma skill pode criar, editar, mover ou remover arquivos sob `argus_ia_agent/`; demandas nesse módulo devem ser tratadas como análise, especificação, backlog ou orientação operacional, sem implementação direta nesse diretório.
- O script `check_ia_governance.py` é a fonte de verdade para as checagens detalhadas e para a lista exata de categorias retornadas.
- O contrato normativo validado pelo script vem de `AGENTS.md`, `.ia/docs/guides/rules-catalog.md`, templates correntes e skills ativas; a skill não deve duplicar esse catálogo em bullets operacionais.
- Findings de governança bloqueiam a etapa quando o fluxo exigir conformidade explícita, especialmente antes de fechamento documental ou consolidação de mudanças amplas em `.ia/`.
- O validador deve continuar bloqueando regressões em placeholders, referências quebradas, hardcodes pessoais, divergências de catálogo/skills, comandos sem `rtk`, contratos de naming/status/data e inconsistências entre templates e automações.
- Legado histórico deve ser tratado como legado documentado; artefato histórico não pode voltar a circular como artefato ativo fora do contrato atual.
- Quando a auditoria encontrar bloqueios conhecidos que não serão corrigidos na mesma etapa, eles devem ser registrados explicitamente na task ou spec em vez de serem ignorados.

# Checklist de qualidade
- Existe um único comando de validação.
- O comando pode ser executado na raiz do repositório.
- O output informa claramente categoria, arquivo e problema.
- O comando retorna código diferente de zero quando encontra findings.

# Referências locais
- `AGENTS.md`
- `.ia/README.md`
- `.ia/skills/governanca-compliance/check_ia_governance.py`
- `.ia/docs/reports/` (destino dos relatórios de conformidade gerados sob demanda)
