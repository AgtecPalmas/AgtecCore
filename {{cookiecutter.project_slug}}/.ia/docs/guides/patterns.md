# Padrões de Projeto (Django/DRF)

## ViewSets/Views

- Apenas orquestração: delegue regras para models/managers.
- Documente actions customizadas; prefira mixins DRF e `get_queryset` otimizados.
- Centralize filtros com `django-filter` ou filtros declarativos.

## Serializers

- Validar entrada antes de persistir; use `validate_` e `validate`.
- Use serializers específicos para leitura/escrita quando regras divergem.
- Evite lógica pesada; delegue para services.

## Services/Use Cases

- Funções puras ou classes focadas em regras de negócio e integrações externas.
- Garantir atomicidade quando necessário (`transaction.atomic`).
- Preparar QuerySets reutilizáveis para evitar N+1.

## Logs e Erros

- Use `core.excecoes` para respostas padronizadas.
- Regras de PII e filtros de log em `.ia/docs/architecture/security.md`.
