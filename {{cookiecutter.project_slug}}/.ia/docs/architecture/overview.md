# Visão Geral da Arquitetura

Backend Django + DRF do projeto **AgtecCore**, organizado como monólito modular por apps. com camada de API consumida por clientes web (templates Django + hotsites públicos), aplicativo Flutter e por uma camada externa de serviço FastAPI desacoplada.

---

## 1. Stack Inicial

| Camada                  | Tecnologia                                              | Versão            |
| ----------------------- | ------------------------------------------------------- | ----------------- |
| Linguagem               | Python                                                  | `3.12.x`          |
| Framework web           | Django                                                  | `5.12.x`          |

## 2. Stack **NÃO** presente (divergência com documentação anterior)

-

## 3. Integrações externas declaradas em `base/settings.py`

-

## 4. Objetivos arquiteturais

- Alta coesão e baixo acoplamento entre apps de domínio.
- Reaproveitamento de QuerySets via `managers.py` por app.
- Soft-delete e auditoria centralizadas em `core.Base` (campos `enabled`/`deleted`, flag global `USE_DEFAULT_MANAGER`, flag `AUDIT_ENABLED`).
- Evolução segura via migrations reversíveis.
- Type hints em helpers, services e tasks externas.
- Validação obrigatória em serializers/forms antes de persistir.

## 5. Regras transversais

- **Exceções**: helpers de `core.excecoes` para respostas DRF padronizadas.
- **Soft-delete**: modelos de domínio herdam de `core.Base` (`enabled`/`deleted` em vez de `DELETE` físico). A flag `DELETED_MANY_TO_MANY=True` propaga delete lógico para relacionamentos M2M.
- **Anonimização PII**: utilitário dedicado `core/cpf_anonymizer.py`.
- **Middleware de contexto**: `core.middleware.current_user.CurrentUserMiddleware` injeta usuário corrente em thread-local (consumido por auditoria).

## 6. Pontos de atenção imediatos

1. `AUTH_USER_MODEL` não declarado → projeto usa `django.contrib.auth.User` padrão. A entidade de negócio `usuario.Usuario` é separada do `User` Django (modelo de domínio, não auth). Mudança futura para custom user é dolorosa nesse estágio.
2. `DEFAULT_AUTHENTICATION_CLASSES` ativa **quatro** backends simultaneamente: Basic, Session, Token, JWT — superfície de ataque ampla; revisar se Basic e Token ainda são necessários.
3. `PAGE_SIZE = 200` é alto — pode mascarar problemas de performance em listagens.
4. `AUDIT_ENABLED = False` em settings mas o modelo `Audit` existe em `core.models` → auditoria desligada hoje, premissa de que será reativada.
5. `USE_DEFAULT_MANAGER = False` em settings mas `core.BaseManager` filtra `deleted=False` por default → risco de registros soft-deletados serem lidos acidentalmente.
