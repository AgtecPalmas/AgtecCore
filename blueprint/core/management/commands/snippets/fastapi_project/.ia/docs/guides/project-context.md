# Contexto Operacional do Projeto

> Camada de precedência: **R1** (junto a `.ia/docs/guides/constraints.md`)
>
> **Template** — preencher com os dados reais do projeto gerado. Use a skill `atualizar-artefatos-ia` para manter atualizado.

Este projeto é um backend FastAPI modular orientado a segurança, performance e manutenibilidade.

---

## Banco de dados

> Documentar o banco principal e extensões utilizadas.

- **Banco principal**: PostgreSQL — A confirmar versão e extensões (ex.: pgvector, pg_trgm)
- **ORM**: SQLAlchemy async/sync — verificar `core/database.py`
- **Configuração**: via `core/config.py` e variável de ambiente `DATABASE_URL`

---

## Cache (se configurado)

> Documentar se Redis ou outro mecanismo de cache está ativo.

- **Cache**: A confirmar — verificar `core/redis.py` e variáveis de ambiente
- **Uso**: A documentar (respostas, sessões de agente, invalidação por escrita)
- **Diretriz**: cache apenas para dados não sensíveis; invalidar após operações de escrita

---

## Busca avançada (se configurada)

> Documentar se Elasticsearch ou outro mecanismo de busca está ativo.

- **Busca**: A confirmar — verificar `core/elastic.py` e variáveis de ambiente
- **Diretriz**: mecanismo de busca não é fonte de verdade; nunca indexar dados sensíveis

---

## Módulo de IA (se existir)

> Documentar o módulo de IA de alto nível aqui. Detalhar em `.ia/docs/architecture/ia_modules.md`.

- **Módulo**: A confirmar — verificar se existe diretório dedicado
- **Restrição**: agentes não devem alterar arquivos do módulo de IA sem autorização explícita em task/spec

---

## Observabilidade (se configurada)

> Documentar as ferramentas de observabilidade ativas.

- **Error tracking**: A confirmar (ex.: Sentry) — verificar `main.py`
- **APM**: A confirmar — verificar dependências e configuração
- **Logging**: A confirmar — verificar padrão de logging no projeto

---

## Diretrizes operacionais

- Cache deve ser usado apenas para dados não sensíveis.
- Mecanismos de busca não são fonte de verdade; nunca indexar dados sensíveis (CPF, senhas, chaves).
- Sempre invalidar cache após operações de escrita.

## Diretrizes do git

- Nunca executar comandos git diretamente no terminal.
- Exceção operacional: quando `AGENTS.md` exigir uma etapa oficial de branch ou merge, usar exclusivamente os scripts Python versionados em `.ia/skills/` que encapsulam essa automação.
