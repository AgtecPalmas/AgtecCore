# Estrutura Modular

> Este documento define o padrão modular esperado para apps Django neste projeto.

## Padrão por app

```
<app>/
├── __init__.py
├── apps.py
├── admin.py                    # registro no Django admin
├── models.py                   # ORM e Regras de Negócio (FatModel)
├── managers.py                 # QuerySets/managers customizados
├── signals.py                  # opcional
├── tasks.py                    # opcional (tasks Celery, se instalado)
├── urls.py                     # rotas web (templates)
├── views/                      # CBVs web (ou views.py único)
├── forms/ ou forms.py          # formulários Django (web)
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

## Variações permitidas

- `services.py` ou `use_cases.py` para lógica de domínio (não ambos — escolher por projeto)
- `views.py` único no lugar de `views/` quando o app for simples

---

## Regras transversais

### Soft-delete

Modelos de domínio herdam de `core.Base` (campos `enabled`/`deleted`). Não usar `Model.delete()` direto — o `Base.delete()` faz update em `deleted=True`, `enabled=False`.

### Manager padrão

`core.BaseManager` filtra `deleted=False` por default. Para ler registros soft-deletados, usar `objects.all_with_deleted()`.

### CurrentUserMiddleware

O usuário corrente é exposto via thread-local para auditoria. Jobs offline e tasks Celery fora do ciclo HTTP precisam injetar usuário manualmente.

### Otimização ORM

`select_related`/`prefetch_related` por padrão em ViewSets de leitura. Definir `get_queryset()` no QuerySet/Manager, não na view.

### Migrations

Pequenas, reversíveis. `RunPython`/`RunSQL` devem ser idempotentes.

### Logs estruturados

Usar `logging.getLogger("django_debug")` com `extra={"chave": valor}`.

---

## Exemplo de estrutura de um app completo

```
usuario/
├── __init__.py
├── apps.py
├── admin.py
├── models.py              # Usuario model herdando de core.Base
├── managers.py           # UsuarioManager com QuerySet customizado
├── api/
│   ├── __init__.py
│   ├── routers.py        # router.register(r'users', UsuarioViewSet)
│   ├── views/
│   │   └── usuario_viewset.py
│   └── serializers/
│       └── usuario_serializer.py
├── services.py           # UsuarioService com regras de negócio
├── tasks.py              # tarefas Celery (se Celery estiver instalado)
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_api.py
└── migrations/
    └── 0001_initial.py
```