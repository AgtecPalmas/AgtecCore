---
name: adicionar-embeddings
description: Adiciona suporte a embeddings vetoriais no módulo de IA do projeto usando pgvector. Use quando o usuário pedir para adicionar busca semântica, embeddings, vetorização de documentos, ou memória de longo prazo ao módulo de IA. Também ativa automaticamente quando o contexto menciona "embeddings", "busca semântica", "pgvector", "vetorização" ou arquivos no módulo de IA do projeto.
---

# Adicionar Embeddings — Módulo de IA

# Objetivo
Adicionar ou evoluir suporte a embeddings vetoriais no módulo de IA do projeto, preservando isolamento de configurações, uso de pgvector e contratos de rota existentes.

## Pré-requisitos

Antes de começar:
1. Ler `.ia/docs/architecture/ia_modules.md` (escopo e regras do módulo de IA)
2. Ler `.ia/docs/architecture/relatorio-arquitetural.md` (configuração de pgvector/cache/memória)
3. Verificar estrutura atual do módulo de embeddings no projeto
4. Criar arquivo de task em `.ia/docs/tasks/todo/task-DD-MM-YYYY-<hash_alfanumerico_10>.md`

## Estrutura sugerida do módulo de embeddings

```
<modulo_ia>/embeddings/
├── __init__.py
├── service.py          # serviço de geração e busca de embeddings
├── models.py           # model SQLAlchemy com coluna Vector (pgvector)
├── schemas.py          # schemas Pydantic para request/response
└── use_cases.py        # lógica de indexação e busca
```

## Checklist de implementação

- [ ] Verificar se `pgvector` está instalado e migração executada
- [ ] Criar/atualizar `service.py` com geração e busca de embeddings
- [ ] Criar model com coluna `Vector` do pgvector se necessário
- [ ] Criar use case de indexação (ingestão de documentos)
- [ ] Criar use case de busca semântica (similaridade por cosseno)
- [ ] Integrar o serviço de embeddings na tool ou agente relevante
- [ ] Criar testes automatizados
- [ ] Confirmar que rotas existentes não foram modificadas

## Regras obrigatórias

1. Nunca modificar rotas de contrato público sem task/spec explícita
2. Nunca criar schemas do módulo de IA para outros módulos
3. Embeddings devem ser gerados de forma assíncrona
4. Configurações de embedding em settings isolados do módulo de IA — nunca em `core.config.Settings`
5. Não alterar arquivos do módulo de IA sem autorização explícita em task aprovada

## Padrão de model com pgvector

```python
from pgvector.sqlalchemy import Vector
from core.database import CoreBase
from sqlalchemy.orm import Mapped, mapped_column

class DocumentoEmbedding(CoreBase):
    __tablename__ = "documento_embedding"
    conteudo: Mapped[str] = mapped_column(nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(1536), nullable=False)
    fonte: Mapped[str] = mapped_column(nullable=True)
```

## Padrão de busca por similaridade

```python
from pgvector.sqlalchemy import Vector
from sqlalchemy import select

async def buscar_similares(db, query_embedding: list[float], limit: int = 5):
    stmt = (
        select(DocumentoEmbedding)
        .order_by(DocumentoEmbedding.embedding.cosine_distance(query_embedding))
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()
```

## Configuração isolada

- Configurações de embedding ficam no arquivo de settings do módulo de IA
- Nunca usar `core/config.py` (`Settings`) para configurações do módulo de IA
- Variáveis de ambiente específicas de IA ficam isoladas no settings do módulo

## Referências de código

- Arquitetura do módulo de IA: `.ia/docs/architecture/ia_modules.md`
- Relatório arquitetural: `.ia/docs/architecture/relatorio-arquitetural.md`
