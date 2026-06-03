# Restrições Técnicas do Projeto

- `[RULE-ARCH-002]` É proibido acessar o banco diretamente a partir de routers.
- `[RULE-ASYNC-001]` É proibido executar operações I/O síncronas.
- `[RULE-DEP-001]` É proibido criar dependências novas sem aprovação arquitetural.
- `[RULE-TEST-001]` Toda feature nova deve possuir testes automatizados.
- `[RULE-LANG-001]` Idioma padrão das respostas: português pt-BR (conforme `AGENTS.md`).
- `[RULE-GIT-001]` **NUNCA executar `git commit`** — commits são responsabilidade exclusiva do desenvolvedor. A IA pode editar arquivos e preparar as mudanças, mas jamais commitar.

## Protocolo anti-alucinação (obrigatório)

- `[RULE-ANTIHAL-001]` Se faltar contexto ou fonte no repositório, diga explicitamente “não encontrei” e peça o mínimo necessário (arquivo/trecho/decisão).
- `[RULE-ANTIHAL-002]` Não invente nomes de módulos, rotas, funções, schemas, enums, variáveis ou comportamentos não documentados.
- Sempre que orientar uma implementação, cite as fontes consultadas (paths de arquivos do repo) e liste assunções (se houver).
- Se já existir um padrão no projeto, reutilize-o e aponte 1–2 referências reais do código/docs; não crie um “novo jeito” (ex.: chamadas Dio no Flutter).
- Na ambiguidade, ofereça opções e peça confirmação antes de implementar.
- Para UI/Flutter, siga o design system existente; se a fonte (Figma/docs/lib) não estiver documentada, solicite o link e não improvise.
