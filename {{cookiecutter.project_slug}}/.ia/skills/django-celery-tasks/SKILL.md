---
name: django-celery-tasks
description: Projetar tarefas assíncronas com Celery em `tasks.py` para processos longos ou desacoplados do request HTTP. Usar quando houver trabalho em background, integração externa ou processamento em lote.
---

# Objetivo

> **Stack atual:** Celery **não está instalado** neste projeto (ver `.ia/docs/architecture/overview.md` §2). Esta skill é **preparatória** — aplicar somente quando Celery for incorporado à stack ou para revisão arquitetural antecipada. Hoje, processos assíncronos usam fallback síncrono (ex.: `assinatura_documento/tasks.py`).

Projetar processamento assíncrono com segurança operacional, idempotência e rastreabilidade quando Celery for aprovado/incorporado ou em revisão arquitetural antecipada.

# Fluxo
1. Definir se a operação realmente precisa sair da requisição síncrona.
2. Confirmar decisão arquitetural para Celery antes de implementar task real em `app/tasks.py`; sem Celery ativo, documentar fallback síncrono explícito.
3. Garantir idempotência para permitir reexecução sem efeito colateral indevido.
4. Registrar eventos relevantes sem PII e com contexto suficiente para observabilidade.
5. Integrar disparo da task a partir de services/use cases.

# Regras obrigatórias
- Não colocar regra de negócio distribuída entre view e task sem coordenação explícita.
- Tratar falhas transitórias com política de retry adequada.
- Evitar payloads gigantes no broker; passar IDs e resolver dados no worker.
- Preservar consistência transacional ao enfileirar tarefas após persistência.

# Checklist de qualidade
- Validar comportamento em reprocessamento.
- Confirmar impacto em banco e integrações externas.
- Garantir monitoramento e logs mínimos para diagnóstico.
- Cobrir fluxo crítico com teste unitário de orquestração quando aplicável.

# Referências locais
- `.ia/docs/guides/patterns.md`
- `.ia/docs/architecture/overview.md`
- `.ia/docs/architecture/security.md`
