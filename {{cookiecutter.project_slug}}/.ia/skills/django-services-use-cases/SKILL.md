---
name: django-services-use-cases
description: Criar e evoluir regras de negócio em `services.py` ou `use_cases.py` por app. Usar quando implementar fluxos de domínio, integrações externas e operações com múltiplas escritas.
---

# Objetivo
Concentrar regras de negócio fora da camada HTTP para melhorar testabilidade e reuso.

# Fluxo
1. Identificar a regra de negócio e definir o app dono do fluxo.
2. Criar função ou classe focada em um caso de uso.
3. Encapsular operações de escrita múltipla com `transaction.atomic()` quando necessário.
4. Integrar com managers e serializers sem acoplamento indevido.
5. Expor retorno simples e previsível para consumo pela API.

# Regras obrigatórias
- Evitar lógica de domínio em views e serializers.
- Não alterar arquivos da app `core/` (ver `AGENTS.md` §8.1).
- Evitar dependência direta de models de outro app sem contrato claro.
- Garantir mensagens de erro seguras e alinhadas a `core.excecoes` quando aplicável.
- Não registrar PII em logs.
- Tratar integrações externas com timeout, retries e falhas controladas quando aplicável.

# Checklist de qualidade
- Cobrir cenário feliz, validações e falhas de negócio em testes.
- Verificar idempotência quando houver reprocessamento possível.
- Revisar performance de consultas no fluxo completo.
- Validar se o caso de uso está coeso e sem responsabilidades extras.

# Referências locais
- `AGENTS.md`
- `.ia/docs/architecture/modules.md`
- `.ia/docs/guides/patterns.md`
- `.ia/docs/architecture/security.md`
- `.ia/docs/guides/constraints.md`
