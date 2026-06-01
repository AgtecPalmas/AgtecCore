# Regra de Endpoint para Filiado Autenticado

## Objetivo

Padronizar implementacoes de endpoints que operam no contexto do filiado logado, evitando regressao de assinatura com `filiado_id` exposto em query/body/path quando a intencao e self-service.

## Quando aplicar

Aplicar esta regra quando o endpoint representa acao do proprio filiado autenticado, por exemplo:

- `fetch-by-filiado` do proprio usuario
- `subscription-action` de inscricao do proprio usuario
- endpoints de check-in/consulta de status da propria inscricao

## Regra de assinatura (router)

Para endpoints self-service do filiado autenticado:

1. O router deve receber `usuario: security.CurrentUserByTokenDependency`.
2. O router nao deve receber `filiado_id` por query/body/path.
3. O router apenas orquestra e delega para o use case.

Excecao:

- `filiado_id` pode existir apenas em endpoint administrativo/operacional, com justificativa de negocio explicita e permissao adequada.

## Regra de resolucao de filiado (use_case)

No use case:

1. Resolver filiado via `authentication.security.get_filiado_by_auth_user(db=db, user=usuario)`.
2. Se retornar `None`, responder com erro de dominio (`NotFoundException("Filiado nao encontrado.")` ou equivalente do modulo).
3. Usar apenas `filiado.id` resolvido internamente nas queries/regras de negocio.

## Regra de contrato Flutter

Se o endpoint for self-service do filiado autenticado:

1. A spec deve declarar explicitamente que `filiado_id` nao deve ser enviado.
2. O checklist de integracao deve validar remocao de `filiado_id` no cliente.
3. Mudancas de assinatura devem ter secao "de/para" na spec.

## Regra de testes

Para testes que sobrescrevem autenticacao:

1. Override de `get_current_usuario_by_token` deve retornar `Usuario` real (nao objeto dummy).
2. Evitar comparar `django_user_id` com UUID por erro de tipo; manter formato compativel ao fluxo real.
3. Cobrir cenarios:
   - usuario autenticado com filiado valido
   - usuario autenticado sem filiado (erro esperado)

## Checklist rapido

- [ ] Endpoint self-service sem `filiado_id` na assinatura HTTP
- [ ] Router com `CurrentUserByTokenDependency`
- [ ] Use case resolve filiado via `get_filiado_by_auth_user`
- [ ] Erro coerente quando filiado nao existe
- [ ] Testes com override retornando `Usuario`
- [ ] Spec Flutter atualizada com de/para e checklist
