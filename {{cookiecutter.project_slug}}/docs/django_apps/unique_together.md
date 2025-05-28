# Usando Unique Together

O campo `unique_together` é usado dentro da classe `Meta` do Model para indicar quais campos deverão ser únicos.

## Exemplos de Uso

### Sobrescrevendo a deleção lógica ou unique do campo do model
```
class Meta:
   ...
   unique_together = ['cpf', 'created_at']
```
Da forma acima, utilizamos o `created_at` apenas como apoio, pois não é possível definir o unique_together somente com um campo, no caso, CPF. Assim usando `created_at` ou `deleted` eles serão ignorados e verificado apenas o primeiro campo passado.

### Utilizando dois ou mais campos
```
class Meta:
   ...
   unique_together = [('cpf', 'created_at'), ('email', 'firebase')]
```
Em forma de lista de tuplas, conseguimos enviar mais campos como forma de validação.
No exemplo acima tanto CPF não pode existir na base quanto Email e Firebase, combinados, também não podem existir.
