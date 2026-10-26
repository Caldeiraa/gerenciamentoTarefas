```mermaid
erDiagram
    USUARIOS ||--o{ TAREFAS : "e responsavel por"
    PROJETOS ||--o{ TAREFAS : "possui"

    USUARIOS {
        INT id_usuario PK
        VARCHAR nome_usuario "NOT NULL"
        VARCHAR email_usuario UK "NOT NULL"
        VARCHAR cargo_usuario
    }

    PROJETOS {
        INT id_projeto PK
        VARCHAR nome_projeto "NOT NULL"
        VARCHAR descricao_projeto
        DATE data_inicio_projeto "NOT NULL"
        DATE data_fim_projeto
    }

    TAREFAS {
        INT id_tarefa PK
        VARCHAR titulo_tarefa "NOT NULL"
        VARCHAR descricao_tarefa
        VARCHAR status_tarefa "NOT NULL"
        VARCHAR prioridade_tarefa "NOT NULL"
        DECIMAL horas_gastas_tarefa "NOT NULL"
        DATE data_criacao_tarefa "NOT NULL"
        DATE data_conclusao_tarefa
        INT id_projeto FK "NOT NULL"
        INT id_usuario FK "NOT NULL"
    }
```

## Cardinalidades
- **PROJETOS 1 : N TAREFAS** — um projeto tem zero ou mais tarefas; cada tarefa pertence a exatamente um projeto.
- **USUARIOS 1 : N TAREFAS** — um usuário é responsável por zero ou mais tarefas; cada tarefa tem exatamente um responsável.

## Restrições
| Tabela | Restrição |
|---|---|
| USUARIOS | `email_usuario` único |
| PROJETOS | `data_fim_projeto >= data_inicio_projeto` |
| TAREFAS | `status_tarefa` em (PENDENTE, EM_ANDAMENTO, CONCLUIDA) |
| TAREFAS | `prioridade_tarefa` em (BAIXA, MEDIA, ALTA) |
| TAREFAS | `horas_gastas_tarefa >= 0` |
| TAREFAS | FKs com `ON DELETE RESTRICT` (a aplicação pergunta se deve excluir os filhos) |
