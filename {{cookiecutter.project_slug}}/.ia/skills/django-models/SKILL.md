---
name: django-models
description: Definir e evoluir models Django ORM do monólito modular AgtecCore. Usar quando criar ou alterar entidades de domínio em `models.py`, campos, relacionamentos, constraints e índices.
---

# Objetivo
Implementar modelos consistentes com a arquitetura modular do projeto, preservando integridade de dados, legibilidade e performance.

# Fluxo
1. Identificar o app de domínio responsável e evitar espalhar regras entre apps.
2. Definir ou ajustar a entidade em `app/models.py` herdando de `core.models.Base` quando aplicável.
3. Configurar `Meta` com `verbose_name`, `verbose_name_plural`, `indexes` e `ordering` quando necessário.
4. Revisar relacionamentos (`ForeignKey`, `OneToOne`, `ManyToMany`) e `on_delete` com foco em segurança dos dados.
5. Planejar migração pequena e reversível em arquivo separado.

# Regras obrigatórias
- Manter regras de negócio fora de `ModelViewSet` e evitar acoplamento indevido entre apps.
- Não alterar arquivos da app `core/` (ver `AGENTS.md` §8.1).
- Priorizar Django ORM; evitar SQL bruto sem justificativa explícita.
- Preparar campos e índices pensando em consultas reais de API e filtros.
- Evitar exposição desnecessária de dados sensíveis; alinhar modelagem com LGPD.
- Usar nomes de campos claros e aderentes ao domínio.

# Checklist de qualidade
- Validar impacto dos novos campos em serialização e filtros.
- Confirmar necessidade de `db_index`, índice condicional ou composto.
- Verificar se mudanças exigem ajustes em fixtures, admin e testes.
- Garantir que a migração resultante seja pequena, clara e reversível.

# Referências locais
- `AGENTS.md`
- `.ia/docs/architecture/overview.md`
- `.ia/docs/architecture/modules.md`
- `.ia/docs/architecture/security.md`
- `.ia/docs/guides/constraints.md`
