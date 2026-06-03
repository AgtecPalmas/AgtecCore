# Tarefa: Corrigir execução de manage.py — substituir "python" por sys.executable

## 1. Metadados

- ID da task: `task-02-06-2026-xL4jN7cW0p`
- Status da task: `done`
- Prioridade: `high`
- Tipo: `bugfix`
- Modulo/area: `tooling / generate_project.py`
- Responsavel: `equipe de produto`
- Solicitante: `equipe de produto`
- Data de criacao: `02-06-2026`
- Ultima atualizacao: `02-06-2026`

## 2. Referencias

- Spec/PRD: `não se aplica`
- TechSpec: `não se aplica`
- Task relacionada: `done-task-02-06-2026-hK9wZ3rX1n` (criação do generate_project.py)
- Board/issue externa: `não se aplica`
- Fontes consultadas:
  - `generate_project.py` (linha com constante `PYTHON`)

## 3. Contexto

Durante teste real em Linux (Ubuntu/WSL), a etapa de build das apps padrão falhou com:

```
[Errno 2] No such file or directory: 'python'
Falha ao construir usuario — execute manualmente
[Errno 2] No such file or directory: 'python'
Falha ao construir configuracao_core — execute manualmente
```

A causa é a constante definida no script:

```python
PYTHON = "py" if sys.platform.startswith("win") else "python"
```

Em Ubuntu, Debian e WSL, o executável padrão é `python3`, não `python`. A constante também é utilizada em `hooks/post_gen_project.py` original, mas ali o hook rodava dentro do venv do CookieCutter onde `python` estava disponível. No novo script, `PYTHON` é usado para chamar `manage.py build` — e o comando falha porque o shell não encontra `python` no PATH.

A correção canônica é usar `sys.executable`, que sempre aponta para o interpretador Python que está executando o próprio script — garantindo que o mesmo binário (seja `python`, `python3`, `.venv/bin/python`, etc.) seja usado para invocar `manage.py`.

## 4. Objetivo

Substituir a constante `PYTHON` por `sys.executable` em `generate_project.py`, eliminando a dependência de `python` estar no PATH do sistema.

## 5. Escopo

- Inclui:
  - Remover a constante `PYTHON` e substituir todas as suas ocorrências por `sys.executable`
  - Atualizar testes que cubram o caminho de execução de `manage.py build`
- Nao inclui:
  - Alterar `hooks/post_gen_project.py` (legado CookieCutter, fora do escopo)
  - Alterar lógica de build em si

## 6. Criterios de aceite

1. Em Linux/WSL, `python generate_project.py` conclui o build das apps padrão sem erro `No such file or directory`
2. Em Windows, o comportamento é mantido (`sys.executable` aponta para `python.exe` ou `py.exe` conforme o ambiente)
3. Testes passam com 0 falhas

## 7. Restricoes e premissas

- Restricoes:
  - `sys.executable` está disponível na stdlib desde Python 2 — sem nova dependência
- Premissas:
  - O script é sempre executado dentro do venv do AgtecCore (onde `sys.executable` é o Python do venv)

## 8. Impacto esperado

- Backend/API: `não`
- Banco de dados: `não`
- Integracoes: `não`
- Seguranca/LGPD: `não`
- Testes: `sim — verificar mock de subprocess com sys.executable`
- Documentacao: `não`

## 9. Plano de execucao

1. Remover `PYTHON = ...` do módulo
2. Substituir todas as referências a `PYTHON` por `sys.executable` (apenas em `build_default_apps`)
3. Rodar suite de testes

## 10. Controle de implementacao

- Branch base da implementacao: `dev`
- Branch de implementacao: `task-02-06-2026-xL4jN7cW0p`
- Skills usadas: `workflow-demandas`
- Arquivos previstos:
  - `generate_project.py`
  - `tests/test_generate_project.py`
- Status de aprovacao: `approved`
- Execucao de testes: `executada`
- Comandos executados:
  - `rtk python3 -m pytest tests/test_generate_project.py -q`

## 11. Evidencias

- Resultado de testes:
  - `56 passed, 0 failed`
- Logs, screenshots ou observacoes:
  - 3 novos testes adicionados: uso de sys.executable, existência do executável, ausência da constante PYTHON

## 12. Definition of Done

- [ ] Implementacao concluida
- [ ] Criterios de aceite atendidos
- [ ] Testes executados ou justificativa registrada
- [ ] Documentacao atualizada
- [ ] Riscos e trade-offs registrados

## 13. Fechamento

- Riscos residuais: `nenhum — sys.executable é a forma idiomática e portável`
- Proximos passos:
  - Aprovação e abertura de branch via `branch-task-aprovada`

## Descricao da solucao implementada

Removida a constante `PYTHON = "py" if sys.platform.startswith("win") else "python"` do módulo. A chamada de `manage.py build` em `build_default_apps()` passou a usar `sys.executable` diretamente, que sempre aponta para o interpretador Python em execução — seja `python`, `python3`, `.venv/bin/python`, `python.exe` ou qualquer outro, em qualquer plataforma (Windows, Windows WSL, Linux, macOS).

## Trade-offs

- `sys.executable` vs detecção de PATH: `sys.executable` é a abordagem idiomática e portável da stdlib; detectar `python`/`python3` no PATH seria frágil e redundante, pois o script já está sendo executado por um interpretador conhecido.

## Arquivos alterados

- `generate_project.py` — removida constante `PYTHON`; `build_default_apps` usa `sys.executable`
- `tests/test_generate_project.py` — 3 novos testes em `TestBuildDefaultAppsExecutable`
