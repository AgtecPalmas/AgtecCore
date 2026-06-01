# Arquitetura do Sistema

> Este documento deve ser preenchido pelo agente de IA ao analisar o projeto gerado pelo template, usando `django-onboarding-checklist`. until then, serve como referência da estrutura esperada.

---

## 1. Visão geral

`{{ cookiecutter.project_description | default("Descrição do projeto a ser preenchida") }}`

---

## 2. Stack e infraestrutura

Versões detalhadas em `overview.md` §1. Resumo:

| Camada | Tecnologia |
| --- | --- |
| Backend | Django + DRF |
| Banco de dados | PostgreSQL |
| Autenticação | A definir (SimpleJWT, Session, Token) |

---

## 3. Catálogo de apps Django

Apps próprios em `settings.py` (`INSTALLED_APPS`). Responsabilidade inferida pelos modelos de cada app.

| App | Responsabilidade | Observações |
| --- | --- | --- |
| `{{ cookiecutter.project_slug }}` | App principal do projeto | A ser preenchido |
| `core` | Base, exceções, middleware, utilitários | Presente em todo projeto Django |

### Catálogos derivados em `base/settings.py`

- `FASTAPI_APPS` (X apps) — escopo replicado/consumido pelo FastAPI externo. **Premissa**: lista controla o que o FastAPI espelha.
- `FLUTTER_APPS` (X apps) — escopo da API exposta ao app Flutter.
- `IGNORED_APPS` — apps escondidos do menu administrativo.

> **Nota**:apps de terceiros (rest_framework, django.contrib.*, etc.) não são listados nesta tabela.

---

## 4. Estrutura modular

Padrão por app definido em `modules.md`. Desvios do padrão devem ser documentados aqui.

---

## 5. Fluxos principais de negócio

1. `{{ cookiecutter.fluxo_principal | default("A ser documentado quando o projeto for detalhado") }}`

---

## 6. Integrações externas

| Integração | Direção | Mecanismo | App responsável | Observações |
| --- | --- | --- | --- | --- |
| `{{ cookiecutter.integracao_externa_1 | default("A definir") }}` | `{{ cookiecutter.direcao_1 | default("A definir") }}` | `{{ cookiecutter.mecanismo_1 | default("A definir") }}` | `{{ cookiecutter.observacao_1 | default("A definir") }}` |

---

## 7. Segurança e autenticação

Detalhado em `security.md`. Resumo:

- Auth REST: `{{ cookiecutter.auth_backends | default("A configurar conforme necessidade") }}`
- LGPD: utilitários de anonimização em `core/cpf_anonymizer.py` (se aplicável)
- `CurrentUserMiddleware` injeta usuário em thread-local (consumido por auditoria, se ativa)

---

## 8. Pontos de atenção / débito técnico

1. `{{ cookiecutter.ponto_atencao_1 | default("A ser identificado durante análise do projeto") }}`