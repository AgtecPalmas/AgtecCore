# IA Embeddings - padrao para criacao em modulos existentes

## Objetivo

Este documento define as especificacoes obrigatorias para qualquer Agent de IA
que precise analisar, especificar ou planejar embeddings de um modulo ja existente no módulo de IA do projeto.


O foco e garantir padrao unico de:

- arquitetura
- qualidade de dados indexados
- seguranca
- idempotencia
- operacao e troubleshooting

## Escopo

Aplica-se a demandas de analise ou especificacao de embeddings em modulos existentes em <modulo_ia>, como exemplo:

- `atendimento`
- `convenio`
- `financeiro`
- `filiado`
- `fornecedor`

Nao cobre criacao de novo endpoint de chat nem mudancas no contrato principal de chat.

## Fontes de verdade obrigatorias

Antes de qualquer especificacao ou planejamento, o Agent deve consultar em modo leitura:

- `.ia/docs/architecture/ia_modules.md`
- `<modulo_ia>/embeddings/README.md`
- `<modulo_ia>/embeddings/*.py`
- codigo do modulo de negocio que sera indexado

Se houver divergencia entre docs e codigo, o codigo atual e a referencia tecnica final.

## Conceitos base

Ha dois tipos de embeddings no projeto:

1. Schema Embeddings (RAG estrutural)

- Baseado em fragmentos curados por desenvolvedor.
- Persistidos em `iaschemaembedding`.
- Usados para descobrir tabelas, colunas e agregacoes.

1. Content Embeddings (RAG narrativo)

- Baseado em texto real dos registros do sistema.
- Persistidos em `ia_content_embeddings`.
- Usados para busca semantica em anotacoes, descricoes, mensagens etc.

## Matriz de decisao (quando implementar)

1. Pergunta do usuario depende de estrutura de dados (tabela/campo/agregacao)?

- Sim: adicionar/ajustar Schema Embeddings.

1. Pergunta do usuario depende de texto livre ou semantica narrativa?

- Sim: adicionar/ajustar Content Embeddings.

1. Caso misto (estrutura + semantica)?

- Implementar ambos.

## Regras mandatorias

1. Nao criar nova tabela de embeddings

- Reutilizar apenas `iaschemaembedding` e `ia_content_embeddings`.

1. Nao alterar rota de chat

- O endpoint `/api/v1/ia/chat/` nao deve ser modificado.

1. Nao quebrar fail-open do startup

- `setup_db` e indexacao automatica no startup nao podem derrubar a API.

1. Manter idempotencia de indexacao

- Schema: respeitar `fragment_key` + `version`.
- Content: respeitar upsert por `source_table + source_id + source_field`.

1. Nao indexar texto vazio

- Campos vazios/brancos devem ser ignorados.

1. Respeitar `deleted = false` em buscas e retroativo

- Nunca incluir dados logicamente deletados.

1. Seguir naming de `source_table`

- Usar padrao real da tabela no banco, ex.: `convenio_convenio`, `atendimento_mensagem`.

1. Nao indexar dados sensiveis

- Proibido indexar senha, token, segredo, documento sigiloso ou payload nao necessario.

1. Preservar compatibilidade vetorial

- O projeto usa `Vector(1536)` nos models atuais.
- Mudanca de dimensao exige analise tecnica previa de compatibilidade.

1. Toda evolucao deve prever caminho retroativo

- Se incluir nova fonte narrativa, tambem incluir no `content_bulk_indexer.py`.

## Fluxo padrao de implementacao

### Etapa 1 - Analise do modulo

Mapear no modulo alvo:

- models e tabelas
- campos textuais relevantes
- eventos de create/update que exigem indexacao incremental
- risco de conteudo sensivel

Saida esperada:

- lista objetiva de campos que entram em schema/content
- justificativa funcional de cada campo

### Etapa 2 - Schema Embeddings (quando aplicavel)

Arquivo principal:

- `<modulo_ia>/embeddings/schema_catalog_indexer.py`

Passos:

1. Criar ou ajustar `SchemaFragment` no `SCHEMA_CATALOG`.
2. Preencher descricao em PT-BR objetiva para o caso de uso.
3. Informar `table_names` reais, separados por virgula.
4. Informar `allowed_aggregations` coerente com o dominio.
5. Controlar reindexacao por `version`.

Padrao para `fragment_key`:

- `<dominio>.<conceito>`
- exemplos: `convenio.convenio`, `atendimento.historico`

Quando aumentar `version`:

- mudanca relevante de descricao funcional
- mudanca de tabelas/campos representados
- mudanca de escopo semantico do fragmento

### Etapa 3 - Content Embeddings incremental (quando aplicavel)

Arquivos tipicos:

- `<modulo_ia>/embeddings/background_tasks.py`
- `modulo/.../use_cases.py` ou `modulo/.../background_tasks.py`

Passos:

1. Agendar `indexar_conteudo_narrativo` apos create/update relevante.
2. Informar `source_table`, `source_id`, `source_field`, `content_text`.
3. Enviar `metadata` minima util para contexto sem expor dados sensiveis.
4. Garantir que falha de indexacao nao interrompa fluxo principal.

Metadata recomendada:

- ids de correlacao (ex.: `atendimento_id`)
- titulo/empresa/chave de contexto nao sensivel

### Etapa 4 - Content Embeddings retroativo (obrigatorio quando nova fonte for adicionada)

Arquivo principal:

- `<modulo_ia>/embeddings/content_bulk_indexer.py`

Passos:

1. Criar funcao `_index_<fonte>(session)` no mesmo padrao existente.
2. Filtrar registros com `deleted == False`.
3. Indexar somente campos textuais nao vazios.
4. Adicionar chamada dessa funcao em `index_all()`.
5. Registrar log de quantidade indexada.

### Etapa 5 - Operacao e bootstrap

Comandos oficiais:

```bash
task ia-setup-db
task ia-index
task ia-index-content
```

Uso esperado:

1. `task ia-setup-db` para garantir extensao/tabelas/indice.
2. `task ia-index` para catalogo de schema.
3. `task ia-index-content` para carga retroativa narrativa.

## Contratos e limites tecnicos a respeitar

1. Endpoints de observabilidade/debug de embeddings

- `GET /api/v1/ia/embeddings/schema/`
- `POST /api/v1/ia/embeddings/schema/search`
- `GET /api/v1/ia/embeddings/content/`
- `POST /api/v1/ia/embeddings/content/search`

1. Limites de busca semantica

- `question`: 3..1000 caracteres
- `top_k`: 1..20

1. Distancia vetorial

- Usa operador `<=>` (cosine distance)
- menor valor = maior similaridade

## Checklist obrigatorio para PR

1. Foi definido se a demanda exige schema, content ou ambos.
2. `SchemaFragment` criado/ajustado com `fragment_key` padrao e `version` coerente.
3. Indexacao incremental conectada aos eventos de negocio corretos.
4. Indexacao retroativa adicionada no `content_bulk_indexer.py`.
5. Campos sensiveis foram excluidos da indexacao.
6. Fluxo principal permanece resiliente a falhas de embedding (sem quebrar operacao).
7. README do modulo de embeddings foi atualizado se houve mudanca de comportamento.
8. Validacao manual minima foi registrada (comandos e resultado).

## Criterios de aceite de uma demanda de embeddings

Uma demanda so e considerada concluida quando:

1. O comportamento novo esta refletido em schema/content conforme escopo aprovado.
2. Existe caminho incremental e retroativo quando aplicavel.
3. Os endpoints de embeddings retornam os registros esperados.
4. Nao houve regressao no fluxo principal do modulo.
5. A documentacao foi atualizada.

## Anti-padroes (nao fazer)

1. Indexar qualquer texto sem curadoria minima.
2. Criar embeddings de campos que nao agregam semantica real.
3. Usar `source_table` inventado ou inconsistente com o banco.
4. Esquecer de incluir nova fonte no retroativo.
5. Alterar contrato de chat para compensar falta de indexacao.
6. Tratar falha de embedding como erro fatal da operacao de negocio.

## Template de implementacao (resumo rapido)

1. Mapear campo narrativo no modulo alvo.
2. Adicionar agendamento de `indexar_conteudo_narrativo` no create/update.
3. Adicionar funcao de retroativo no `content_bulk_indexer.py`.
4. Se necessario, incluir/ajustar `SchemaFragment` no catalogo.
5. Rodar bootstrap/indexacao e validar via endpoints `/ia/embeddings/*`.
6. Atualizar documentacao tecnica.

## Referencias diretas

- `<modulo_ia>/embeddings/README.md`
- `<modulo_ia>/embeddings/schema_catalog_indexer.py`
- `<modulo_ia>/embeddings/content_bulk_indexer.py`
- `<modulo_ia>/embeddings/background_tasks.py`
- `<modulo_ia>/embeddings/schema_embedding_service.py`
- `<modulo_ia>/embeddings/content_embedding_service.py`
- `.ia/docs/architecture/ia_modules.md`
