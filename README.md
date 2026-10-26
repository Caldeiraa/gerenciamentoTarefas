# Sistema de Gerenciamento de Tarefas

Sistema de gerenciamento de usuários, projetos e tarefas com persistência em **MySQL 8.0.16+**, desenvolvido como trabalho da disciplina de **Banco de Dados** do curso de Análise e Desenvolvimento de Sistemas (FAESA).

## Integrantes

| Integrante | Responsabilidade |
|---|---|
| George | Menu principal, tela inicial, integração dos módulos, README e revisão final |
| Murilo | Modelagem do banco, script SQL |
| Davi | Implementação do CRUD |

## Funcionalidades

O sistema implementa os seguintes requisitos funcionais:

- **RF01 — Splash screen:** exibe nome do sistema, contagem de registros de cada tabela, integrantes, disciplina, semestre e professor.
- **RF02 — Menu principal:** exibido continuamente com as opções: Relatórios, Inserir, Remover, Atualizar, Sair.
- **RF03 — Relatórios:**
  - RF03.1: Resumo por usuário com total de tarefas, concluídas e horas gastas (`GROUP BY`).
  - RF03.2: Listagem de tarefas com nome do projeto e responsável (`JOIN`).
  - RF03.3: Tarefas por projeto e por status.
- **RF04 — Inserir registros:** menu de entidades → inserção → pergunta se deseja inserir outro.
- **RF05 — Remover registros:** listagem → seleção → confirmação → remoção (com tratamento de FK e exclusão em cascata).
- **RF06 — Atualizar registros:** listagem → seleção → novos valores → exibição do registro atualizado.

## Regras de Negócio

| Código | Descrição |
|---|---|
| RN01 | E-mail do usuário é único |
| RN02 | Toda tarefa pertence a um projeto e possui um responsável |
| RN03 | Status: `PENDENTE`, `EM_ANDAMENTO` ou `CONCLUIDA` |
| RN04 | Prioridade: `BAIXA`, `MEDIA` ou `ALTA` |
| RN05 | Horas gastas não podem ser negativas |
| RN06 | Data de término do projeto não pode ser anterior à data de início |
| RN07 | Data de conclusão só é preenchida quando status = `CONCLUIDA` |
| RN08 | Verificação de existência antes de inserir, atualizar ou excluir |

## Estrutura do Projeto

```
gerenciamentoTarefas/
├── script_criacao.sql           # DDL + dados iniciais (MySQL)
├── modelo_relacional.md         # Diagrama ER (Mermaid)
├── requisitos.md                # Requisitos extraídos do edital
├── PROMPTS.md                   # Registro de uso de IA
├── README.md                    # Este arquivo
└── src/
    ├── __init__.py
    ├── principal.py             # Ponto de entrada e integração
    ├── conexion/
    │   ├── __init__.py
    │   └── db_connection.py     # Conexão MySQL (DB-API)
    ├── model/
    │   ├── __init__.py
    │   └── models.py            # Classes Usuario, Projeto, Tarefa
    ├── controller/
    │   ├── __init__.py
    │   └── controller.py        # Validações e regras de negócio
    ├── sql/
    │   ├── __init__.py
    │   └── queries.py           # Consultas SQL (concatenação de texto)
    ├── reports/
    │   ├── __init__.py
    │   └── reports.py           # Relatórios RF03.1, RF03.2, RF03.3
    └── utils/
        ├── __init__.py
        ├── config.py            # Configurações centrais
        └── splash_screen.py     # Tela inicial (RF01)
```

## Pré-requisitos

- **Linux** (VM da disciplina)
- **Python 3** instalado
- **MySQL 8.0.16+** com o banco `gerenciamento_tarefas` criado
- **mysql-connector-python** instalado:
  ```bash
  pip3 install mysql-connector-python
  ```

## Como Executar

### 1. Criar o banco de dados

No terminal MySQL:

```sql
source script_criacao.sql;
```

Isso criará o banco `gerenciamento_tarefas`, as tabelas e os dados iniciais.

### 2. Configurar a conexão

Edite o arquivo `src/conexion/db_connection.py` e informe as credenciais do MySQL:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "SUA_SENHA_AQUI",
    "database": "gerenciamento_tarefas",
}
```

### 3. Executar o sistema

Na raiz do projeto:

```bash
python3 -m src.principal
```

## Modelo Relacional

```
USUARIOS (id_usuario PK, nome_usuario, email_usuario UK, cargo_usuario)
PROJETOS (id_projeto PK, nome_projeto, descricao_projeto, data_inicio_projeto, data_fim_projeto)
TAREFAS  (id_tarefa PK, titulo_tarefa, descricao_tarefa, status_tarefa, prioridade_tarefa,
           horas_gastas_tarefa, data_criacao_tarefa, data_conclusao_tarefa,
           id_projeto FK → PROJETOS, id_usuario FK → USUARIOS)
```

- **USUARIOS 1:N TAREFAS** — um usuário é responsável por zero ou mais tarefas.
- **PROJETOS 1:N TAREFAS** — um projeto possui zero ou mais tarefas.

## Tecnologias

- Python 3
- MySQL 8.0.16+
- mysql-connector-python (DB-API 2.0)
- SQL por concatenação de texto (sem ORM, conforme RNF02)