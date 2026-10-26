# Sistema de Gerenciamento de Tarefas — Requisitos

Disciplina: Banco de Dados — Prof. Howard Roatti — Semestre 2026/2
Banco de dados: MySQL | Linguagem: a definir pelo grupo (ambiente Linux)

## 1. Objetivo
Controlar usuários, projetos e tarefas, permitindo acompanhar o andamento do trabalho por meio de relatórios de tarefas concluídas e tempo gasto.

## 2. Entidades
- **USUARIOS**: pessoas que executam tarefas.
- **PROJETOS**: agrupam um conjunto de tarefas.
- **TAREFAS**: unidades de trabalho, atribuídas a um usuário e vinculadas a um projeto.

Relacionamentos:
- Um projeto possui várias tarefas (1:N).
- Um usuário é responsável por várias tarefas (1:N).

## 3. Requisitos funcionais

### RF01 — Splash screen
Ao iniciar, exibir o nome do sistema, a quantidade de registros de cada tabela (`select count(1) total_<entidade> from <entidade>`), os nomes dos integrantes do grupo, a disciplina, o semestre e o professor.

### RF02 — Menu principal (exibido continuamente)
1. Relatórios
2. Inserir registros
3. Remover registros
4. Atualizar registros
5. Sair

### RF03 — Relatórios
- **RF03.1 (agrupamento, GROUP BY):** total de tarefas, tarefas concluídas e total de horas gastas por usuário.
- **RF03.2 (junção, JOIN):** listagem de tarefas com nome do projeto e nome do responsável.
- **RF03.3 (opcional):** tarefas por projeto e por status.

### RF04 — Inserir registros
Menu de entidades → usuário escolhe → informa cada atributo → inserção → pergunta se deseja inserir outro.

### RF05 — Remover registros
Menu de entidades → listagem (PK + campo descritivo) → seleção → confirmação → remoção → pergunta se deseja remover outro.
- Se o registro for FK em outra tabela (usuário ou projeto com tarefas), informar o usuário e perguntar se deseja excluir também os registros filhos.

### RF06 — Atualizar registros
Menu de entidades → listagem → seleção → informar novos valores (exceto PK) → atualização → exibir o registro atualizado → pergunta se deseja atualizar outro.

## 4. Regras de negócio
- RN01: e-mail do usuário é único.
- RN02: toda tarefa pertence a um projeto e possui um responsável.
- RN03: status da tarefa: `PENDENTE`, `EM_ANDAMENTO` ou `CONCLUIDA`.
- RN04: prioridade da tarefa: `BAIXA`, `MEDIA` ou `ALTA`.
- RN05: horas gastas não podem ser negativas.
- RN06: data de término do projeto, quando informada, não pode ser anterior à data de início.
- RN07: data de conclusão só é preenchida quando o status é `CONCLUIDA`.
- RN08: antes de inserir, verificar se o registro já existe; antes de atualizar/excluir, verificar se existe.

## 5. Requisitos não funcionais
- RNF01: executar na VM Linux da disciplina.
- RNF02: consultas SQL montadas por concatenação de texto (sem ORM).
- RNF03: interface de console amigável (menus claros, mensagens de erro e confirmação).
- RNF04: código organizado em `model`, `controller`, `conexion`, `sql`, `reports`, `utils` e `principal`.
- RNF05: prompts de IA registrados em `PROMPTS.md`; commits de todos os integrantes no GitHub (professor `howardroatti` como colaborador).

## 6. Entregáveis
Script de criação das tabelas, código-fonte, diagrama relacional (PDF/PNG), vídeo no YouTube, README.md (Linux) e PROMPTS.md.
