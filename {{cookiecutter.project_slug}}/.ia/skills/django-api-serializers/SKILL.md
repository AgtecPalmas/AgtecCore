---
name: django-api-serializers
description: Construir e manter serializers DRF em `api/serializers/` para validação de entrada, serialização de saída e proteção de dados sensíveis. Usar quando criar ou alterar contratos de API.
---

# Objetivo
Garantir contratos de API consistentes, validação robusta e respostas seguras.

# Fluxo
1. Criar serializer no app correto em `api/serializers/<entidade>.py`.
2. Definir campos de leitura e escrita de forma explícita.
3. Implementar `validate_<campo>` e `validate()` para regras de entrada.
4. Delegar lógica de negócio pesada para `services.py` ou `use_cases.py`.
5. Ajustar `routers` e `views` que dependem do serializer.

# Regras obrigatórias
- Validar payload antes de persistir.
- Separar serializer de leitura e escrita quando regras divergirem.
- Omitir ou anonimizar dados sensíveis conforme LGPD.
- Evitar acessar banco de forma ineficiente dentro de validações.
- Preservar mensagens de erro seguras e consistentes.

# Checklist de qualidade
- Cobrir casos felizes e falhas de validação em testes.
- Revisar compatibilidade com paginação e filtros da API.
- Confirmar que campos internos (`deleted`, `enabled`, tokens) não vazam sem necessidade.
- Revisar impacto em documentação de API e consumidores existentes.

# Referências locais
- `AGENTS.md`
- `.ia/docs/guides/patterns.md`
- `.ia/docs/architecture/security.md`
- `.ia/docs/guides/testing.md`
