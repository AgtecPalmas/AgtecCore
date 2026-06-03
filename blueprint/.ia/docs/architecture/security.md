# Arquitetura de Segurança — AgtecCore

---

## 1. Autenticação e autorização

### 1.1 Backends DRF ativos (`base/settings.py:208-213`)

```
BasicAuthentication
SessionAuthentication
TokenAuthentication
JWTAuthentication (SimpleJWT)
```

**4 backends simultâneos**. JWT é o backend de produção esperado para clientes Flutter/FastAPI. Basic e Token possivelmente legados. **Ação sugerida**: revisar se Basic e Token ainda têm consumidores; se não, remover.

### 1.2 Tokens JWT (SimpleJWT)

```
ACCESS_TOKEN_LIFETIME  = 60 min
REFRESH_TOKEN_LIFETIME = 1 dia
```

Sem rotação de refresh habilitada nem blacklist configurada em settings. **Premissa**: não há revogação ativa de tokens; logout REST hoje é client-side.

### 1.3 Auth web

- `LOGIN_URL = /core/login`
- `LOGIN_REDIRECT_URL = /core`
- `LOGOUT_REDIRECT_URL = /core/login`
- CSRF habilitado (`CsrfViewMiddleware`).
- `CSRF_TRUSTED_ORIGINS` parametrizado via env.

### 1.4 Usuário de autenticação

- `AUTH_USER_MODEL` **não declarado** → usa `django.contrib.auth.User` default.
- A entidade de negócio `usuario.Usuario` (e seus desdobramentos `Filiado`, `Colaborador`, `Dependente`) **não substitui** o `auth.User`. Existem dois conceitos de "usuário": o de auth (Django) e o de domínio (`usuario.Usuario`). Trocar para custom user agora é caro pois há migrations antigas com FKs para `auth.User`.

### 1.5 Permissões

- `SPECTACULAR_SETTINGS.SERVE_PERMISSIONS` exige `IsAuthenticated` + `IsAdminUser` para acessar Swagger/Redoc.
- Permissões por ViewSet/ação devem ser explícitas; evitar `AllowAny` global.

### 1.6 Senha (validators ativos)

```
UserAttributeSimilarityValidator
MinimumLengthValidator
CommonPasswordValidator
NumericPasswordValidator
```

Sem `password_changed`/`password_complexity` custom adicional.

## 2. Dados sensíveis (LGPD) — campos detectados

- 
### 2.1 Mecanismos de proteção observados

- `core/cpf_anonymizer.py` (5,5 KB) — utilitário dedicado de anonimização de CPF.
- `drf-jsonmask` declarado em `requirements.in` — permite mascaramento de campos por requisição (consumidor decide o subset retornado).
- Soft-delete via `core.Base.deleted=True` em vez de apagar fisicamente — **atenção LGPD**: solicitação de eliminação real precisa de fluxo dedicado (hoje não há).

### 2.2 Gaps a tratar (**premissa** sem leitura completa dos serializers)

- 

## 3. Middleware de segurança

Ordem em `base/settings.py:89-99`:

```
SecurityMiddleware
SessionMiddleware
CommonMiddleware
CsrfViewMiddleware
AuthenticationMiddleware
MessageMiddleware
XFrameOptionsMiddleware
core.middleware.header_control.HeaderControlMiddleware
core.middleware.current_user.CurrentUserMiddleware
```

- `SecurityMiddleware` ativo (HTTPS redirects, HSTS via env — **não confirmado** quais flags `SECURE_*` estão definidas em settings; nenhuma aparece em `base/settings.py` lido).
- `XFrameOptionsMiddleware` ativo (default `DENY`).
- `CurrentUserMiddleware` — expõe usuário em thread-local; consumido por auditoria (modelo `Audit` em `core`). Atenção: tasks offline/management commands não têm request → nunca confiar em `current_user` fora do request/response cycle.

**Gaps**: settings inspecionado não declara `SECURE_PROXY_SSL_HEADER`, `SECURE_HSTS_SECONDS`, `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`. **Premissa**: definidos em arquivo de settings de produção fora do repositório, ou em variáveis de ambiente do servidor de aplicação. **Confirmar**.

## 4. Throttling

-

## 5. Auditoria

- Modelo `Audit` existe em `core/models.py` (referenciado nas migrations `0003`, `0007`).
- Flag `AUDIT_ENABLED = False` em settings → **auditoria desligada hoje**.
- Quando reativada, exige `CurrentUserMiddleware` no pipeline (já está).

## 6. Observabilidade e exposição de erros

- Sentry (`sentry-sdk`) — premissa: capturar erros sem PII (filtros antes do `before_send` não inspecionados).
- Elastic APM (`elastic-apm`) — `base/elastic.py` configura `SERVICE_NAME=AgtecCore`. Performance/traces.
- **Premissa**: tags/contexto enviados ao Sentry/APM podem conter dados de request (headers, query string) — **revisar `before_send` para garantir scrubbing de tokens/CPF**.
- Logger padrão observado: `logging.getLogger("django_debug")` com `extra={...}` estruturado.

## 7. Segredos e configuração

- `SECRET_KEY`, `DB_*`, `EMAIL_*`, `CSRF_TRUSTED_ORIGINS`, `ALLOWED_HOSTS`, `FASTAPI_*`, `FLUTTER_API_*` via `python-decouple`.

## 8. Migrations sensíveis a segurança

- 

## 9. Boas práticas operacionais (regras vigentes)

- 

## 10. Pendências de segurança consolidadas

1. ...
