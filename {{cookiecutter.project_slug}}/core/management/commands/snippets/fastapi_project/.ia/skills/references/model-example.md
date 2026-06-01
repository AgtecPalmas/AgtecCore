# Referência One-Shot: Model

> Fonte real: `filiado/cargotrabalho/models.py`
> Padrão canônico de model SQLAlchemy do projeto Argus.

## Padrão de model com CoreBase

```python
from typing import Optional
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import CoreBase


class NomeModelo(CoreBase):
    __tablename__ = "modulo_nomemodelo"

    # Campos próprios do modelo (nunca redeclarar id, deleted, created_at, updated_at, enabled)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relacionamento (exemplo com FK)
    outro_modelo_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("modulo_outromodelo.id"), nullable=True
    )
    outro_modelo = relationship("OutroModelo", foreign_keys=[outro_modelo_id])
```

## Campos providos automaticamente por CoreBase

| Campo | Tipo | Comportamento |
| ------- | ------ | --------------- |
| `id` | UUID | PK auto-gerada (`uuid4`) |
| `deleted` | bool | Soft delete (default `False`) |
| `created_at` | datetime | Preenchido automaticamente |
| `updated_at` | datetime | Atualizado com `onupdate` |
| `enabled` | bool | Ativo/inativo (default `True`) |

**Nunca redeclarar esses campos no model filho.**

## Regras obrigatórias (model)

- `RULE-MODEL-001`: model **deve** herdar de `CoreBase` (`core/database.py`)
- `__tablename__` segue o padrão `modulo_nomemodelo` (snake_case)
- Campos nullable devem declarar `Mapped[Optional[T]]` + `nullable=True`
- Campos não-nullable devem declarar `Mapped[T]` + `nullable=False`
- Relacionamentos via `relationship()` com `foreign_keys` explícito quando ambíguo
- Migrações via Alembic (`migrations/`) — nunca alterar estrutura diretamente no banco
