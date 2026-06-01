# Arquitetura de Segurança

> Fonte: `authentication/security.py`, `core/cpf_anonymizer.py`, `core/middlewares/`, `.ia/docs/architecture/relatorio-arquitetural.md` (seção 5)

## Autenticação e Autorização

- **JWT** (PyJWT) com escopos e expiração — implementado em `authentication/security.py`
- **OAuth2 Password Flow** para obtenção de tokens
- Permissões validadas via `security.has_permission("modulo.acao_modelo")` como dependência FastAPI
- Usuário autenticado exposto via `security.CurrentUserByTokenDependency` nos handlers
- Segredo do token: variável de ambiente `TOKEN_JWT_SECRET` (nunca hardcoded)

## Hashing de senhas

- **Passlib** com algoritmo bcrypt
- Nunca armazenar senha em texto puro; nunca retornar hash em responses

## LGPD — Anonimização de CPF

- Módulo dedicado: `core/cpf_anonymizer.py`
- Utiliza **AES** com as chaves de ambiente:
  - `KEY_ANONYMIZATION_CPF`
  - `IV_ANONYMIZATION_CPF`
- Nunca exibir CPF completo em logs ou responses públicos
- Nunca indexar CPF em embeddings ou Elasticsearch

## Configuração e Segredos

- Todas as variáveis sensíveis vivem no `.env` e são lidas via Pydantic Settings
- Configuração global: `core.config.Settings`
- Módulos com integração externa específica (ex.: IA) devem manter settings próprios isolados de `core.config.Settings`
- **Nunca** commitar `.env` com valores reais; usar `.env.example` ou variáveis de container

## CORS e Middlewares

- Middlewares customizados em `core/middlewares/`
- Configurar CORS explicitamente para origens permitidas (não usar `allow_origins=["*"]` em produção)
- Rastreamento de erros via Sentry/Elastic APM configuráveis por variável de ambiente

## Boas práticas obrigatórias

- **Nunca** retornar dados sensíveis (CPF completo, senha, chaves) em responses
- **Sempre** validar e sanitizar payloads de entrada com Pydantic antes de processar
- **Nunca** fazer I/O síncrono em operações autenticadas — usar `async/await`
- **Nunca** acessar banco diretamente em routers — delegar para use cases
- Exceções de autenticação/autorização devem usar classes de `core.exceptions`
