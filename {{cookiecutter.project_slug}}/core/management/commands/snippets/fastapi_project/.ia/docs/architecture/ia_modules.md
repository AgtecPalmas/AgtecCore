# Módulo de IA

> **Template** — preencher se o projeto tiver módulo de IA (embeddings, agentes, RAG). Se o projeto não tiver módulo de IA, este arquivo pode ser ignorado ou removido.
>
> Use a skill `atualizar-artefatos-ia` para manter este documento atualizado após implementações.

---

## 1. Visão geral

> Descrever o propósito do módulo de IA deste projeto: o que ele faz, quais endpoints expõe e quais módulos de domínio consome.

---

## 2. Localização e estrutura

> Documentar o diretório raiz do módulo de IA e sua estrutura interna.

```
<nome_modulo_ia>/
├── <submodulo_agentes>/     # agentes/orquestração
├── <submodulo_embeddings>/  # embeddings/busca vetorial (se existir)
├── <submodulo_chat>/        # interface de chat/streaming (se existir)
├── config.py                # settings isolados do módulo de IA
└── ...
```

---

## 3. Runtime e orquestração

> Documentar o framework de agentes/orquestração utilizado.

- **Runtime**: A confirmar
- **Agentes**: A documentar
- **Memória de sessão**: A confirmar (Redis, banco, etc.)
- **Memória longa**: A confirmar (pgvector, etc.)

---

## 4. Embeddings e busca vetorial (se existir)

> Documentar a implementação de embeddings.

- **Extensão PostgreSQL**: A confirmar (pgvector, etc.)
- **Tabelas de embeddings**: A documentar após análise
- **Dimensão dos vetores**: A confirmar
- **Modelo de geração**: A confirmar

---

## 5. Configuração isolada

> O módulo de IA deve manter sua configuração isolada do `core.config.Settings`.

- **Arquivo de config**: A confirmar (ex.: `<modulo_ia>/config.py`)
- **Variáveis de ambiente específicas de IA**: A documentar — nunca misturar com settings gerais

---

## 6. Endpoints expostos

> Listar os endpoints do módulo de IA.

| Rota | Método | Descrição | Sensibilidade |
|---|---|---|---|
| A confirmar | A confirmar | A confirmar | A confirmar |

---

## 7. Restrições operacionais

> Documentar as restrições específicas para agentes ao trabalhar com este módulo.

1. Agentes não devem alterar arquivos do módulo de IA sem autorização explícita em task/spec.
2. A confirmar — adicionar restrições específicas após análise do módulo.
