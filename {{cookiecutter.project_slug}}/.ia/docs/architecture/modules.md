# Estrutura Modular — AgtecCore

## Padrão alvo por app

```
<app>/
├── __init__.py
├── apps.py
├── admin.py                    # registro no Django admin
├── models.py                   # ORM e Regras de Negócio (FatModel)
├── managers.py                 # QuerySets/managers customizados
├── signals.py                  # opcional, ver tabela §3
├── tasks.py                    # opcional; hoje só assinatura_documento tem fallback síncrono para Celery ausente
├── urls.py                     # rotas web (templates)
├── views/                      # CBVs web (alguns apps mantêm views.py único)
├── forms/  ou forms.py         # formulários Django (web)
├── templates/                  # templates HTML do app
├── static/                     # estáticos do app (opcional)
├── fixtures/                   # opcional
├── migrations/
├── tests/                      # pytest por domínio
└── api/
    ├── __init__.py
    ├── routers.py              # registro de ViewSets no DRF
    ├── views/                  # ViewSets/CBVs DRF
    └── serializers/            # serializers DRF
```

## 1. Variações observadas (não obrigatórias hoje)

-

## 2. `services.py` x `use_cases.py`

-

## 3. `signals.py`

-

## 4. `tasks.py`

-
## 5. Regras transversais

- **Soft-delete**: modelos de domínio herdam de `core.Base` (campos `enabled`/`deleted`). Não usar `Model.delete()` direto; o `Base.delete()` faz update em `deleted=True`, `enabled=False` (ver `core/models.py:223+`).
- **Manager padrão**: `core.BaseManager` filtra `deleted=False` por default; a flag global `USE_DEFAULT_MANAGER=False` em settings ativa esse comportamento. Para ler registros soft-deletados, usar `objects.all_with_deleted()` (verificar API real em `core/models.py`).
- **`CurrentUserMiddleware`**: o usuário corrente é exposto via thread-local para auditoria. Jobs offline e eventuais tasks futuras fora do ciclo HTTP precisam injetar usuário manualmente (não há request).
- **Otimização ORM**: `select_related`/`prefetch_related` por padrão em ViewSets de leitura. Definir `get_queryset()` no QuerySet/Manager, não na view.
- **Migrations**: pequenas, reversíveis. `RunPython`/`RunSQL` devem ser idempotentes (modelo: `core/migrations/0008_enable_pgvector_extension.py`).
- **Logs estruturados**: usar `logging.getLogger("django_debug")` com `extra={"chave": valor}`.
