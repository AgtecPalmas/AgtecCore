# Auditoria Core

## O que é
A Auditoria cria um histórico com todos os campos prévios e atuais quando algum objeto sofre qualquer tipo de modificação.

## Como Usar

### Global
Necessário adicionar as seguintes linhas no arquivo `settings.py` dentro da pasta `base`:
```
# Ativar Auditoria
AUDIT_ENABLED = True

# Auditoria também seja feita nos relacionamentos M2M
DELETED_MANY_TO_MANY = True
```

### Específico
Caso não queira ativar a Auditoria em todo o projeto, é possível utilizar a variável `auditar` dentro da classe `Meta` do Model em questão.
```
class SeuModel(Base):
    ...

    class Meta:
        auditar = True
```