# Tarefa: Corrigir git commit — tratar ausência de identidade global do git

## 1. Metadados

- ID da task: `task-02-06-2026-dV2kY6bH3s`
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
  - `generate_project.py` (função `init_git`)

## 3. Contexto

Durante teste real em Linux (WSL), o passo `git commit -am "Primeiro Commit"` falhou (❌) enquanto `git init`, `git add .` e `git checkout -b desenvolvimento` passaram (✅).

A causa mais provável é ausência de identidade global do git (`user.name` e `user.email`) no ambiente do usuário — condição comum em ambientes novos, WSL recém-instalado, containers e servidores CI. O git recusa o commit sem essa configuração:

```
Author identity unknown
*** Please tell me who you are.
Run:
  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"
```

A função atual em `generate_project.py`:

```python
GIT_COMMANDS = [
    "git init --initial-branch=master",
    "git add .",
    'git commit -am "Primeiro Commit"',
    "git checkout -b desenvolvimento",
]
```

O commit falha silenciosamente (retorna `False`) e o checkout ainda é executado (na branch `master` sem commits), deixando o repositório em estado inconsistente.

## 4. Objetivo

Garantir que `git commit` funcione em ambientes sem identidade global configurada, injetando uma identidade mínima via flags `-c` no comando de commit, e que o `git checkout -b desenvolvimento` só execute após commit bem-sucedido.

## 5. Escopo

- Inclui:
  - Detectar ausência de `user.name`/`user.email` no git config e injetar identidade mínima via `-c` no commit
  - Garantir que `git checkout -b desenvolvimento` só execute se o commit tiver sido bem-sucedido (há commits na branch)
  - Atualizar testes para cobrir o cenário de commit sem identidade global
- Nao inclui:
  - Modificar o git config global do usuário
  - Alterar a estrutura de branches geradas

## 6. Criterios de aceite

1. Em ambiente sem `git config --global user.name`, o commit é realizado com sucesso usando identidade mínima padrão
2. Se o commit falhar por qualquer outra razão, `git checkout -b desenvolvimento` não é executado e uma mensagem clara é exibida
3. Em ambiente com identidade global configurada, o comportamento é idêntico ao anterior (usa a identidade do usuário)
4. Testes passam com 0 falhas

## 7. Restricoes e premissas

- Restricoes:
  - Não modificar o git config global do usuário — usar apenas flags `-c` no comando pontual
  - A identidade mínima deve ser claramente identificável como gerada pelo script (ex: `AgtecCore Generator`)
- Premissas:
  - git está disponível no PATH do ambiente

## 8. Impacto esperado

- Backend/API: `não`
- Banco de dados: `não`
- Integracoes: `não`
- Seguranca/LGPD: `não`
- Testes: `sim — cenário de commit sem identidade global`
- Documentacao: `não`

## 9. Plano de execucao

1. Em `init_git()`, detectar se `user.name` e `user.email` estão configurados via `git config user.name` (retorno vazio = ausente)
2. Se ausente, montar o comando de commit com `-c user.name="AgtecCore Generator" -c user.email="agtec@palmas.to.gov.br"`
3. Tornar `git checkout -b desenvolvimento` condicional ao sucesso do commit (só executa se o commit retornou `True`)
4. Atualizar testes: mock de `subprocess.run` para simular ausência de identidade e verificar injeção dos `-c`

## 10. Controle de implementacao

- Branch base da implementacao: `task-02-06-2026-xL4jN7cW0p`
- Branch de implementacao: `task-02-06-2026-dV2kY6bH3s`
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
  - `61 passed, 0 failed`
- Logs, screenshots ou observacoes:
  - 5 novos testes em TestInitGit cobrindo: injeção de -c, commit sem flags quando identidade existe, checkout condicional ao commit, mensagem como argumento único

## 12. Definition of Done

- [ ] Implementacao concluida
- [ ] Criterios de aceite atendidos
- [ ] Testes executados ou justificativa registrada
- [ ] Documentacao atualizada
- [ ] Riscos e trade-offs registrados

## 13. Fechamento

- Riscos residuais:
  - Ambientes onde git não está no PATH — já tratado pelo `_run()` existente que captura exceção
- Proximos passos:
  - Aprovação e abertura de branch via `branch-task-aprovada`

## Descricao da solucao implementada

Criada função `_git_has_identity()` que consulta `git config --global user.name` — sem efeito colateral no config do usuário. Em `init_git()`, se a identidade estiver ausente, o comando de commit é montado com `-c user.name=AgtecCore Generator -c user.email=agtec@palmas.to.gov.br` (flags pontuais, não alteram o `.gitconfig` global). O `git checkout -b desenvolvimento` passou a ser condicional: só executa se o commit retornar sucesso, evitando estado inconsistente de repositório sem commits. Corrigido também bug latente: a mensagem "Primeiro Commit" agora é passada como elemento único na lista de argumentos (não sofre `.split()` que quebrava em dois tokens).

## Trade-offs

- **`-c` pontual vs `git config --local`**: `-c` é mais limpo — não deixa rastro no `.git/config` do projeto gerado nem no `.gitconfig` global do usuário.
- **`--global` na detecção**: verificar só o global evita falso positivo de uma config local herdada de outro repo; o projeto recém-criado não tem config local ainda.
- **Identidade fixa vs solicitada ao usuário**: optado por identidade mínima automática para não interromper o fluxo; o usuário pode alterar depois com `git config user.name`.

## Arquivos alterados

- `generate_project.py` — nova função `_git_has_identity()`; `init_git()` refatorada com commit condicional à identidade, checkout condicional ao commit e mensagem como argumento único
- `tests/test_generate_project.py` — 5 novos testes em `TestInitGit`
