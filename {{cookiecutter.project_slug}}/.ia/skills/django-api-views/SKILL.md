---
name: django-api-views
description: Implementar endpoints DRF em `api/views/` e roteamento em `api/routers.py` e `base/urls_api.py`. Usar quando criar ou ajustar ViewSets/ReadOnlyViewSets, permissões, filtros e orquestração de casos de uso.
---

# Objetivo
Manter a camada HTTP enxuta, previsível e alinhada ao padrão REST do projeto.

# Fluxo
1. Implementar ou alterar classe em `app/api/views/<entidade>.py`.
2. Definir autenticação, permissões e `queryset` otimizado.
3. Associar serializer adequado e filtros declarativos.
4. Registrar endpoint em `app/api/routers.py`.
5. Validar prefixo de rota em `base/urls_api.py` (`<app>/api/v1/`).

# Regras obrigatórias
- Tratar a view como orquestração; mover regra de negócio para serviços/use cases.
- Não alterar arquivos da app `core/` (ver `AGENTS.md` §8.1).
- Aplicar permissões por endpoint e evitar configuração permissiva global.
- Preferir `select_related` e `prefetch_related` no `queryset`.
- Manter comportamento explícito para listagem, detalhe e ordenação.
- Preservar respostas de erro seguras sem vazar dados sensíveis.

# Checklist de qualidade
- Confirmar autenticação esperada (JWT, sessão ou token) por endpoint.
- Revisar `search_fields`, `ordering_fields` e filtros para evitar consultas caras.
- Garantir que os nomes de rota e basename estejam coerentes com o domínio.
- Validar status codes HTTP e contratos de resposta.

# Referências locais
- `AGENTS.md`
- `base/urls_api.py`
- `.ia/docs/architecture/modules.md`
- `.ia/docs/architecture/security.md`
- `.ia/docs/guides/patterns.md`
