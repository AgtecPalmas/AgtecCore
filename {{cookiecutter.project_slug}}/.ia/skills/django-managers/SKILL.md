---
name: django-managers
description: Projetar QuerySets e managers customizados em `managers.py` para encapsular consultas reutilizáveis e evitar N+1. Usar quando criar filtros complexos, seleção por contexto e acessos de dados de domínio.
---

# Objetivo
Centralizar regras de consulta em managers e QuerySets para reduzir duplicação e melhorar performance.

# Fluxo
1. Mapear consultas repetidas e mover a lógica para `app/managers.py`.
2. Implementar métodos explícitos com nomes de intenção clara.
3. Encadear `select_related` e `prefetch_related` para casos de listagem e detalhe.
4. Tratar erros esperados de consulta com exceções seguras.
5. Expor o manager no model com `objects = MeuManager()` quando necessário.

# Regras obrigatórias
- Não colocar regra de negócio de processo no manager; manter foco em acesso a dados.
- Não alterar arquivos da app `core/` (ver `AGENTS.md` §8.1).
- Evitar filtros implícitos ambíguos; usar assinaturas previsíveis.
- Evitar consultas em loop dentro de serializers ou views quando um QuerySet resolvido atende.
- Usar logs sem PII em falhas de consulta.

# Checklist de qualidade
- Validar se o manager reduz duplicação de consulta entre API e serviços.
- Conferir se os relacionamentos carregados evitam N+1.
- Garantir cobertura de teste para sucesso e falha.
- Revisar se o manager não acopla indevidamente apps distintos.

# Referências locais
- `AGENTS.md`
- `.ia/docs/architecture/modules.md`
- `.ia/docs/guides/patterns.md`
- `.ia/docs/guides/testing.md`
