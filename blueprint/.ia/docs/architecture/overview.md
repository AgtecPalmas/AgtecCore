# Visão Geral da Arquitetura

Backend Django + DRF do projeto, organizado como monólito modular por apps. A camada de API pode ser consumida por clientes web (templates Django + hotsites públicos).
---

## 1. Stack Inicial

| Camada | Tecnologia | Versão |
| --- | --- | --- |
| Linguagem | Python | `{{ cookiecutter.python_version }}` |
| Framework web | Django | `{{ cookiecutter.django_version }}` |
| API | Django REST Framework | `{{ cookiecutter.drf_version }}` |
| Banco de dados | PostgreSQL | `{{ cookiecutter.postgresql_version }}` |

> **Nota**: versões são defaults do template e podem ser alterados no `cookiecutter.json` ou durante a geração do projeto.

---

## 2. Stack **NÃO** presente (a confirmar no projeto gerado)

- Celery (tarefas assíncronas) — instalar se necessário
- Redis (filas e cache) — instalar se necessário
- Elasticsearch (busca) — instalar se necessário
- Outras tecnologias opcionais documentadas em `.ia/docs/guides/constraints.md`

---

## 3. Integrações externas declaradas em `settings.py`

`{{ cookiecutter.integracoes_externas | default("A definir no projeto gerado — documentar aqui as integrações com serviços externos (e-mail, SMS, pagamentos, etc.)") }}`

---

## 4. Objetivos arquiteturais

- Alta coesão e baixo acoplamento entre apps de domínio.
- Reaproveitamento de QuerySets via `managers.py` por app.
- Soft-delete e auditoria centralizadas em `core.Base` (campos `enabled`/`deleted`, flag global `USE_DEFAULT_MANAGER`, flag `AUDIT_ENABLED`).
- Evolução segura via migrations reversíveis.
- Type hints em helpers, services e tasks externas.
- Validação obrigatória em serializers/forms antes de persistir.

---

## 5. Regras transversais

- **Exceções**: helpers de `core.excecoes` para respostas DRF padronizadas.
- **Soft-delete**: modelos de domínio herdam de `core.Base` (`enabled`/`deleted` em vez de `DELETE` físico). A flag `DELETED_MANY_TO_MANY=True` propaga delete lógico para relacionamentos M2M.
- **Anonimização PII**: utilitário dedicado `core/cpf_anonymizer.py` (se aplicável ao projeto).
- **Middleware de contexto**: `core.middleware.current_user.CurrentUserMiddleware` injeta usuário corrente em thread-local (consumido por auditoria, se ativa).

---

## 6. Pontos de atenção imediatos

> Estes são pontos de atenção genéricos para qualquer projeto Django/DRF. Ajustar conforme o projeto gerado.

1. `AUTH_USER_MODEL` não declarado → projeto usa `django.contrib.auth.User` padrão. Se o projeto requer um model de usuário customizado, declarar em `settings.py` antes de criar migrations.
2. `DEFAULT_AUTHENTICATION_CLASSES` — verificar quais backends são necessários; remover os não utilizados para reduzir superfície de ataque.
3. `PAGE_SIZE` em configurações de paginação — ajustar conforme necessidade real do projeto.
4. `AUDIT_ENABLED` — auditoria desligada por padrão. Se necessária, ativar e verificar se `CurrentUserMiddleware` está na cadeia de middleware.
5. `USE_DEFAULT_MANAGER` — verificar comportamento esperado para registros soft-deletados; `BaseManager` filtra `deleted=False` por default.

---

## 7. Autenticação e Autorização

| Aspecto | Status no projeto |
| --- | --- |
| Backends ativos | `{{ cookiecutter.auth_backends | default("A configurar no projeto") }}` |
| Token/Session/JWT | `{{ cookiecutter.auth_type | default("A configurar conforme necessidade") }}` |
| Custom User Model | `{{ cookiecutter.custom_user_model | default("Não — usa django.contrib.auth.User") }}` |

---

## 8. Observabilidade

| Ferramenta | Proposta | Status |
| --- | --- | --- |
| Sentry | Error tracking | `{{ cookiecutter.sentry_enabled | default("A configurar se necessário") }}` |
| Logging estruturado | Django logging | Ativo por padrão |
| APM/Metrics | `{{ cookiecutter.apm_enabled | default("A configurar se necessário") }}` |

---

## 9. Segurança e LGPD

- Autenticação: backends configurados em `settings.py`
- Autorização: permissões DRF por ViewSet
- LGPD: utilitários de anonimização em `core/cpf_anonymizer.py` (se aplicável)
- Soft-delete: método preferencial de remoção (não `DELETE` físico)

---

*Última atualização: `{{ cookiecutter.data_criacao | default("DD-MM-YYYY") }}` — Documento gerado pelo template CookieCutter*