---
name: django-tests-pytest
description: Escrever e revisar testes automatizados com `pytest`, `pytest-django` e TestContainers para models, API e casos de uso do projeto, executando-os com a `.venv` ativa e pelo fluxo do repositório que provisiona dependências via TestContainers. Usar quando adicionar feature, bugfix, refactor ou alterar contrato de endpoint.
---

# Objetivo
Garantir cobertura de regressão com testes determinísticos por app e por camada.

# Fluxo
1. Confirmar que a `.venv` do projeto está ativa e que o fluxo do repositório para provisionar dependências via TestContainers está disponível antes de executar `pytest`.
2. Criar ou atualizar testes em `app/tests/` seguindo `test_*.py`.
3. Cobrir pelo menos cenário feliz, validação e falha relevante.
4. Usar `APIClient` para API e fixtures explícitas para setup.
5. Validar consultas críticas com `assertNumQueries` quando houver risco de N+1.
6. Executar a suíte segmentada do app antes da finalização usando a `.venv` do projeto e o fluxo com TestContainers.

# Regras obrigatórias

- Os testes devem ser obrigatoriamente executados via TestContainer
- Sempre ativar o ambiente virtual com o comando `rtk source .venv/bin/activate` antes de rodar os testes
- Manter testes determinísticos e sem dependência de ordem.
- Evitar dados sensíveis reais em massa de teste; usar `model_bakery` ou factories próprias.
- Preferir `reverse`/`reverse_lazy` para URLs quando viável.
- Não introduzir novas dependências de teste sem aprovação.
- Garantir que novas regras de negócio tenham cobertura automatizada.
- Nunca usar `pytest` global ou Python fora da `.venv` do projeto.
- Se o serviço `db` do `dev.docker-compose.yml` ou o Postgres alvo estiver indisponível, registrar bloqueio explícito com o comando tentado e o motivo — não fallback para SQLite, não banco compartilhado de outro ambiente.

# Checklist de qualidade

- Revisar se o teste falha quando a regra quebra.
- Confirmar autenticação e permissões em testes de API.
- Validar status code e payload de resposta.
- Registrar no artefato da task os comandos executados, confirmando uso da `.venv` e do fluxo com TestContainers, ou o bloqueio encontrado.

# Comandos úteis

- `rtk source .venv/bin/activate && python -m pytest <app>/tests/`
- `rtk source .venv/bin/activate && python -m pytest --collect-only <alvo>`
- `rtk source .venv/bin/activate && task test`

# Referências locais

- `AGENTS.md`
- `.ia/docs/guides/testing.md`
- `.ia/docs/guides/patterns.md`
- `pyproject.toml`
