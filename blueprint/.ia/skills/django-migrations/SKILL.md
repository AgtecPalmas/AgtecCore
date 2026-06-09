---
name: django-migrations
description: Planejar, gerar e revisar migrations Django com foco em segurança de produção. Usar quando houver mudanças de schema, índices, constraints ou backfill de dados.
---

# Objetivo
Evoluir schema de forma incremental, reversível e com risco operacional controlado.

# Fluxo
1. Preparar mudança mínima necessária no model.
2. Gerar migração por app com `rtk python manage.py makemigrations <app>`.
3. Revisar arquivo gerado e separar mudanças grandes em etapas.
4. Aplicar localmente com `rtk python manage.py migrate`.
5. Validar impacto em consultas, índices e compatibilidade da API.

# Regras obrigatórias
- Manter migrations pequenas, com nome e intenção claros.
- Não alterar arquivos da app `core/` (ver `AGENTS.md` §8.1).
- Evitar operações de alto lock sem planejamento.
- Separar alteração estrutural de backfill quando necessário.
- Garantir reversibilidade quando tecnicamente viável.
- Documentar impacto de produção na task da demanda.

# Checklist de qualidade
- Verificar dependências entre migrações de apps diferentes.
- Revisar operações destrutivas (`RemoveField`, `AlterField`) com atenção.
- Confirmar criação de índices úteis para filtros e ordenação reais.
- Executar testes essenciais após migração.

# Comandos úteis
- `rtk python manage.py makemigrations <app>`
- `rtk python manage.py migrate`
- `rtk python manage.py showmigrations`

# Referências locais
- `.ia/docs/architecture/modules.md`
- `.ia/docs/architecture/overview.md`
- `.ia/docs/guides/constraints.md`
