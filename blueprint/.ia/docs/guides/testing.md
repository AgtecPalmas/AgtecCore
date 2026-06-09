# Estratégia de Testes

## Ferramentas

- Os testes devem ser escritos usando o TestContainers, https://testcontainers.com, para execução isolada e consistente, garantindo que cada teste tenha seu próprio ambiente de banco de dados e dependências.
- Pytest + pytest-django
- Django test client / DRF APIClient
- model_bakery ou factories próprias para dados de teste

## Regras

- Tests devem ser determinísticos e isolar efeitos (use `transactional_db` ou fixtures que limpam estado).
- Prefira `APIClient` para testes de API e `assertNumQueries` para monitorar N+1.
- Cubra casos felizes e de validação em serializers/services.
- Não introduzir dependências novas de teste sem aprovação.

## Estrutura

- Coloque testes por app em `app/tests/` seguindo padrão `test_*.py`.
- Use fixtures compartilhadas em `conftest.py` quando fizer sentido.

## API

- Prefixo global: /api/v1/.
- Utilize `reverse`/`resolve` ou `reverse_lazy` para construir URLs; evite strings hardcoded quando possível.
