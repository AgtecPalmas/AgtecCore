# Arquitetura do Sistema — AgtecCore

---

## 1. Visão geral

- 

Domínio de negócio inferido: ...

## 2. Stack e infraestrutura

Versionamento detalhado em `overview.md` §1. Resumo:

- 

## 3. Catálogo de apps Django

X apps próprios em `INSTALLED_APPS` (excluindo libs de terceiros). Responsabilidade inferida pelos modelos de cada app.

| App                    | Responsabilidade                          | Observações                                  |
| ---------------------- | ----------------------------------------- | -------------------------------------------- |
...


Apps de **debug** ativados condicionalmente quando `DEBUG=True`: `django_extensions`, `debug_toolbar` (silk comentado).

### Catálogos derivados em `base/settings.py`

- `FASTAPI_APPS` (X apps) — escopo replicado/consumido pelo FastAPI externo. **Premissa**: lista controla o que o FastAPI espelha.
- `FLUTTER_APPS` (X apps) — escopo da API exposta ao app Flutter.
- `IGNORED_APPS` — apps escondidos do menu administrativo.

## 4. Estrutura modular

Padrão por app definido em `modules.md`. Desvios observados:

- 

## 5. Fluxos principais de negócio (inferência)

1. 

## 6. Integrações externas

| Integração                   | Direção                                     | Mecanismo                         | App responsável         | Observações                                            |
| ---------------------------- | ------------------------------------------- | --------------------------------- | ----------------------- | ------------------------------------------------------ |
| FastAPI externo              | (premissa) FastAPI → Postgres compartilhado | DB compartilhado + `pgvector`     | —                       | `FASTAPI_*` em settings, sem consumo no código Django. |
| App Flutter                  | Flutter → Django API                        | REST `/api/v1/` + JWT/Token       | Todos em `FLUTTER_APPS` | Credenciais `FLUTTER_API_*` p/ dev.                    |

## 7. Segurança e autenticação

Detalhado em `security.md`. Resumo:

- Auth REST: SimpleJWT (60min access / 1d refresh) + Session + Basic + Token (4 backends ativos).
- Pagina login Django web: `/core/login`.
- LGPD: app `privacidade` + helper `core/cpf_anonymizer.py`. PII concentrada em `usuario` (29 campos detectados).
- `CurrentUserMiddleware` injeta usuário em thread-local (consumido por auditoria).

## 8. Pontos de atenção / débito técnico

1. 