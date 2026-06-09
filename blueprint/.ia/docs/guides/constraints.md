# Restrições Técnicas do Projeto

- Não introduzir dependências novas sem aprovação arquitetural prévia.
- Regras de negócio devem obrigatoriamente residir no models, aplicando o conceito de Fat Models do Django.
- Evite consultas com N+1; use `select_related`/`prefetch_related` e QuerySets explícitos.
- Evite SQL bruto; quando indispensável, documente, teste e cubra com migrações reversíveis.
- Toda feature nova deve incluir testes automatizados (domínio e API) alinhados ao pytest-django e TestContainer's.
