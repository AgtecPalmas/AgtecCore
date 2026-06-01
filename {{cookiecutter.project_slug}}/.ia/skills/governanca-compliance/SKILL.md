---
name: governanca-compliance
description: Validar a governança documental e operacional de agentes em `AGENTS.md` e `.ia/`, detectando placeholders, status inválidos, referências quebradas, hardcodes pessoais, documentos duplicados, menções a stack obsoleta em `AGENTS.md`, divergências essenciais entre skills e catálogos, e regressões do contrato `DD-MM-YYYY`/status em inglês. Usar quando o desenvolvedor pedir auditoria automatizada de governança ou antes de consolidar mudanças amplas em `.ia/`.
---

# Objetivo
Detectar regressões de governança antes que elas se espalhem pelo repositório, reduzindo a dependência de auditorias manuais periódicas.

# Fluxo
1. Executar `rtk python .ia/skills/governanca-compliance/check_ia_governance.py`.
2. Ler os findings retornados por categoria.
3. Corrigir os problemas encontrados ou registrar bloqueios conhecidos.
4. Reexecutar o comando até que o resultado esperado para a etapa seja atingido.

# Regras obrigatórias
- O comando deve falhar quando encontrar placeholder em documento canônico.
- O comando deve falhar quando encontrar task em `done/` com status diferente de `done`.
- O comando deve falhar quando encontrar referência local quebrada em documentos correntes ou templates correntes.
- O comando deve falhar quando encontrar caminho pessoal hardcoded em documentos correntes ou scripts de governança.
- O comando deve falhar quando encontrar documentos canônicos com conteúdo idêntico (categoria `duplicate_doc`) em paths diferentes de `.ia/`.
- O comando deve falhar quando `AGENTS.md` mencionar tecnologias declaradas ausentes em `.ia/docs/architecture/overview.md` sem qualificação (categoria `agents_md_freshness`). Lista atual de termos monitorados: Redis, Celery, Elasticsearch.
- O comando deve falhar quando AGENTS, README e os diretórios reais de skills estiverem divergentes de forma essencial.
- O comando deve falhar quando um `SKILL.md` não contiver as seções `# Objetivo` ou `# Regras obrigatórias` (categoria `skill_missing_section`).
- O comando deve falhar quando a frontmatter `description:` de um `SKILL.md` não declarar um gatilho explícito (padrão `Usar quando`, `Usar sempre que` ou equivalente — categoria `skill_description_trigger`).
- O comando deve falhar quando encontrar termos placeholder genéricos (`XPTO`, `LOREM`, `LOREM IPSUM`, `TODO_FIXME`) em `AGENTS.md`, `CLAUDE.md` ou qualquer `SKILL.md` (categoria `placeholder_term`).
- O comando deve falhar quando a mesma task existir simultaneamente em `todo/` e `done/` (categoria `task_duplicate_lifecycle`).
- O comando deve falhar quando uma task tiver múltiplos campos `Status da task` com valores conflitantes (categorias `task_multiple_status_fields` e `task_conflicting_status_fields`).
- O comando deve falhar quando taskipy apontar para script local inexistente (categoria `taskipy_broken_path`).
- O comando deve falhar quando scripts geradores em `.ia/skills/**/*.py` emitirem termos placeholder genéricos, exceto o próprio validador (categoria `generator_placeholder_term`).
- O comando deve falhar quando comandos executáveis de agente em `AGENTS.md` ou `SKILL.md` não usarem prefixo `rtk` (categoria `agent_command_missing_rtk`).
- O comando deve falhar quando task aberta em `todo/` não usar `task-DD-MM-YYYY-<hash_alfanumerico_10>.md`, ou quando task nova concluída tiver data inválida no nome (categoria `task_filename_date_contract`).
- O comando deve falhar quando metadados canônicos de tasks novas, templates ou specs usarem data fora de `DD-MM-YYYY` (categoria `metadata_date_contract`).
- O comando deve falhar quando spec corrente na raiz ou spec FastAPI ativa usar nome fora do contrato aprovado, preservando legado concluído quando explicitamente marcado como `done`/`superseded` (categoria `spec_filename_date_contract`).
- O comando deve falhar quando specs usarem status fora do enum em inglês, ou specs em `done/` tiverem status diferente de `done`/`superseded` (categoria `spec_status_contract`).
- O comando deve falhar quando reports correntes não declararem `Data`, `Status do relatorio`, `Escopo` e `Validacao executada` no contrato aprovado (categoria `report_metadata_contract`).
- O comando deve falhar quando documentos canônicos, templates ou skills mencionarem `DD_MM_YYYY`, `DD/MM/YYYY` ou `YYYY-MM-DD` sem contexto explícito de legado, bloqueio ou retrocompatibilidade (categoria `legacy_date_reference_contract`).
- O comando deve falhar quando o template legado no antigo diretório de tasks voltar a existir competindo com `.ia/docs/templates/task-template.md` (categoria `legacy_template_reference`).
- O comando deve falhar quando `.ia/docs/templates/task-template.md` divergir do contrato mínimo exigido pelas automações de branch e encerramento (categoria `task_template_contract`).

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
