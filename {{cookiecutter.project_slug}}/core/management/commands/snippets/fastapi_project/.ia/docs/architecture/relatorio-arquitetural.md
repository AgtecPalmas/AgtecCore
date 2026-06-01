# Relatório Arquitetural — FastAPI

> **Template** — preencher após análise inicial do projeto gerado. Este documento serve como relatório factual da arquitetura atual; não é planejamento futuro. Use a skill `atualizar-artefatos-ia` para mantê-lo atualizado.

---

## 1. Contexto do projeto

> Descrever em 2–3 parágrafos o propósito do serviço FastAPI, sua relação com o ecossistema Django e os principais consumidores (Flutter, web, outros serviços).

---

## 2. Stack confirmada

> Preencher após verificar `pyproject.toml` e arquivos de configuração.

| Camada | Tecnologia | Versão |
|---|---|---|
| Framework web | FastAPI | A confirmar |
| Servidor ASGI/dev | Uvicorn | A confirmar |
| Servidor produção | Gunicorn | A confirmar |
| ORM | SQLAlchemy | A confirmar |
| Banco principal | PostgreSQL | A confirmar |
| Sessão async | AsyncSession + asyncpg | A confirmar |
| Schemas/validação | Pydantic v2 | A confirmar |
| Auth | OAuth2 Bearer + JWT | Implementado em `authentication/security.py` |
| Cache | Redis (se configurado) | A confirmar |
| Observabilidade | A confirmar | Verificar `main.py` |
| Testes | pytest, pytest-asyncio, TestContainers | A confirmar |

Python: A confirmar — verificar `pyproject.toml`.

---

## 3. Organização da aplicação

> Descrever a estrutura de entrada, routers e módulos do projeto.

- `main.py`: instância FastAPI, lifespan, CORS, observabilidade.
- `core/routers.py`: router principal com prefixo `settings.api_str`.
- `core/config.py`: settings do ambiente.
- `core/database.py`: engines sync/async.

### Módulos registrados

> Listar os módulos de domínio após análise do `core/routers.py`:

```
- authentication
- <listar módulos>
```

---

## 4. Padrão por módulo

> Confirmar se o padrão abaixo está seguido; registrar desvios observados.

- `routers.py` → endpoints e dependências
- `schemas.py` → contratos Pydantic
- `models.py` → modelos SQLAlchemy
- `use_cases.py` → regra de aplicação

**Desvios conhecidos:**

> Documentar aqui qualquer módulo que não segue o padrão, com justificativa.

---

## 5. Autenticação e autorização

> Descrever o fluxo de autenticação JWT confirmado no projeto.

- Mecanismo: A confirmar — verificar `authentication/security.py`
- Permissões: A confirmar — verificar `core/security.py`
- Modelos compartilhados com Django: A documentar após análise

---

## 6. Módulo de IA (se existir)

> Se o projeto tiver módulo de IA, documentar aqui os aspectos de alto nível e detalhar em `.ia/docs/architecture/ia_modules.md`.

---

## 7. Integrações externas

> Listar as integrações confirmadas após análise.

| Sistema | Direção | Mecanismo | Observação |
|---|---|---|---|
| Django (ecossistema) | Entrada | JWT compartilhado | A detalhar |
| A confirmar | A confirmar | A confirmar | A confirmar |

---

## 8. Pontos de atenção identificados

> Registrar os pontos críticos observados durante a análise inicial do projeto.

1. A confirmar — executar `governanca-compliance` após onboarding inicial.

---

## 9. Restrições operacionais confirmadas

> Registrar as restrições específicas deste projeto além das globais de `AGENTS.md`.

1. O módulo `core/` não deve ser alterado por agentes sem autorização explícita.
2. A confirmar — adicionar restrições específicas do projeto após análise.
