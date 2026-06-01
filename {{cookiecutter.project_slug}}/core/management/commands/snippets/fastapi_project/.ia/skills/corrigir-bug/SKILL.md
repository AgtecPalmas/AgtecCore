---
name: corrigir-bug
description: Diagnostica e corrige bugs no projeto Argus seguindo o protocolo anti-alucinação. Use quando o usuário reportar um erro, exceção, comportamento inesperado, ou falha em teste. Também ativa automaticamente quando o contexto menciona "bug", "erro", "exception", "falha", "não funciona" ou stack traces.
---

# Corrigir Bug — Argus

# Objetivo
Diagnosticar e corrigir bugs com base em evidências do código real, reproduzindo a falha quando possível e atacando a causa raiz.

# Regras obrigatórias
- Regra global: nenhuma skill pode criar, editar, mover ou remover arquivos sob `argus_ia_agent/`; demandas nesse módulo devem ser tratadas como análise, especificação, backlog ou orientação operacional, sem implementação direta nesse diretório.
- Ler o stack trace e o código afetado antes de propor correção.
- Não inventar módulos, funções, payloads ou comportamentos.
- Registrar na task os arquivos consultados, causa raiz e validação executada.
- Usar comandos com prefixo `rtk` quando documentar execução.

## Protocolo de diagnóstico

Antes de qualquer mudança:
1. **Reproduzir**: entender o contexto exato do erro (stack trace, rota, payload)
2. **Localizar**: identificar o arquivo e linha onde o problema ocorre
3. **Analisar causa raiz**: não tratar sintoma sem entender a causa
4. **Citar fontes**: sempre referenciar o arquivo/trecho real do código

## Restrições do protocolo anti-alucinação

- Nunca inventar nomes de módulos, funções ou comportamentos não documentados
- Se faltar contexto, pedir explicitamente o stack trace, arquivo ou trecho relevante
- Só propor correção depois de ler o código afetado
- Citar os arquivos consultados ao explicar a correção

## Checklist de diagnóstico

- [ ] Ler o stack trace completo e identificar o arquivo/linha raiz
- [ ] Ler o código do arquivo afetado (não só a linha do erro)
- [ ] Verificar se o padrão violado está documentado em `.ia/docs/guides/patterns.md`
- [ ] Verificar constraints em `.ia/docs/guides/constraints.md`
- [ ] Identificar se é erro de tipo, lógica, I/O, autenticação ou banco

## Categorias comuns de bug

### Erro de banco / SQLAlchemy
- Verificar se está usando `async` session corretamente (`await db.execute(...)`)
- Verificar se o model herda de `CoreBase` (`core/database.py`)
- Nunca usar sessão síncrona em contexto async

### Erro de validação / Pydantic
- Verificar se o schema herda corretamente (`*Base`, `*Create`, `*Update`, `*InDBBase`)
- Verificar campos `Optional` e `model_config = ConfigDict(from_attributes=True)`
- Pydantic v2: usar `model_validate()` em vez de `from_orm()`

### Erro de autenticação / permissão
- Verificar `CurrentUserByTokenDependency` no router
- Verificar `has_permission("modulo.acao_modelo")` no `Depends`
- Checar `core/security.py` para o padrão correto

### Erro em endpoints com filiado autenticado
- Verificar se endpoint self-service esta recebendo `filiado_id` indevidamente
- Verificar se o use case resolve filiado via `get_filiado_by_auth_user`
- Verificar se o erro ocorre por override de autenticacao em teste retornando objeto dummy em vez de `Usuario`
- Checar regra: `.ia/docs/guides/regra-endpoint-filiado-autenticado.md`

### Erro no módulo IA
- Verificar se a rota `/api/v1/ia/chat/` foi acidentalmente modificada
- Verificar se `run_context` está sendo passado corretamente para as tools
- Checar `argus_ia_agent/config.py` para configurações (`IaSettings`)

### Erro em testes
- Confirmar que Docker está rodando: `docker info`
- Confirmar que deps estão sincronizadas: `rtk uv sync`
- Verificar se TestContainers está sendo inicializado corretamente

## Formato da correção

Ao propor a correção:
1. Explicar **o que causou** o bug (causa raiz)
2. Mostrar **o código atual** (problemático)
3. Mostrar **o código corrigido**
4. Explicar **por que a correção resolve** o problema
5. Sugerir **teste** para validar a correção

## Referências de padrões

- Padrões gerais: `.ia/docs/guides/patterns.md`
- Constraints: `.ia/docs/guides/constraints.md`
- Módulo IA: `.ia/docs/architecture/ia_modules.md`
- Segurança: `.ia/docs/architecture/security.md`
- Testes: `.ia/docs/testing/strategy.md`
