# Sistema de Gerenciamento de Tarefas

Sistema de gerenciamento de usuários, projetos e tarefas desenvolvido para a disciplina de **Banco de Dados** (Prof. Howard Roatti - 2026/2). Persistência em **MySQL 8.0+** utilizando **Python 3**.

---

## 👥 Integrantes do Grupo

| Integrante | Responsabilidade |
|---|---|
| **Murilo** | Banco de dados e modelagem (SQL, integridade, relatórios) |
| **Davi** | Operações CRUD (regras de negócio e controladores) |
| **George** | Interface e integração (menus, fluxo, splash screen, documentação) |

---

## 🛠️ Pré-requisitos

- **Python 3.10+**
- **MySQL Server 8.0+** (ou MySQL Workbench)
- Biblioteca Python: `mysql-connector-python`

---

## 🚀 1. Preparação do Banco de Dados (MySQL)

Tanto na **Máquina Virtual (Linux)** quanto na **Máquina Física (Windows)**, é necessário criar o banco e as tabelas executando o script SQL:

1. Abra o **MySQL Workbench** (ou terminal do MySQL).
2. Abra e execute o arquivo:
   ```sql
   script_criacao.sql
   ```
   *Ou via terminal:*
   ```bash
   mysql -u root -p < script_criacao.sql
   ```
3. Isso criará o banco de dados `gerenciamento_tarefas`, todas as tabelas (`usuarios`, `projetos`, `tarefas`), restrições e registros de teste.

---

## ⚙️ 2. Configurar Credenciais do Banco

Abra o arquivo `src/conexion/db_connection.py` e certifique-se de que a senha corresponde ao seu MySQL:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "SUA_SENHA_AQUI",    # Ajuste para a senha do seu MySQL 
    "database": "gerenciamento_tarefas",
    "charset": "utf8mb4",
    "collation": "utf8mb4_unicode_ci",
}
```

---

## 🖥️ 3. Como Executar na Máquina Física (Windows)

1. **Instalar a biblioteca do conector MySQL:**
   ```powershell
   pip install mysql-connector-python
   ```

2. **Entrar na pasta raiz do projeto:**
   ```powershell
   cd c:\caminho\para\gerenciamentoTarefas
   ```

3. **Executar o sistema:**
   ```powershell
   python -m src.principal
   ```

---

## 🐧 4. Como Executar na Máquina Virtual (Linux)

1. **Instalar as dependências necessárias:**
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip
   pip3 install mysql-connector-python
   ```

2. **Entrar na pasta raiz do projeto:**
   ```bash
   cd ~/gerenciamentoTarefas
   ```

3. **Executar o sistema:**
   ```bash
   python3 -m src.principal
   ```

---

## 📁 Estrutura do Projeto

```text
gerenciamentoTarefas/
├── script_criacao.sql       # Script DDL + dados iniciais
├── modelo_relacional.md     # Diagrama ER e cardinalidades
├── requisitos.md            # Especificações de requisitos e regras
├── PROMPTS.md               # Histórico de uso de IA (conforme edital)
├── README.md                # Instruções de execução
└── src/
    ├── conexion/            # Conexão com o banco (db_connection.py)
    ├── controller/          # Regras de negócio e validações (controller.py)
    ├── model/               # Entidades Usuario, Projeto, Tarefa (models.py)
    ├── reports/             # Relatórios GROUP BY e JOIN (reports.py)
    ├── sql/                 # Consultas SQL por concatenação (queries.py)
    ├── utils/               # Configurações e Splash Screen (RF01)
    └── principal.py         # Ponto de entrada do sistema (RF02)
```

---

## 📋 Funcionalidades Implementadas

- **RF01 — Splash Screen:** Exibe contagem dinâmica de registros, integrantes, disciplina e professor.
- **RF02 — Menu Principal:** Navegação contínua entre as funcionalidades.
- **RF03 — Relatórios:**
  - *RF03.1 (GROUP BY):* Resumo de tarefas e horas gastas por usuário.
  - *RF03.2 (JOIN):* Detalhamento de tarefas com projeto e usuário responsável.
  - *RF03.3:* Tarefas agrupadas por projeto e status.
- **RF04 — Inserir Registros:** Usuários, projetos e tarefas com validações completas.
- **RF05 — Remover Registros:** Exclusão com proteção de integridade referencial (FK) e opção em cascata.
- **RF06 — Atualizar Registros:** Atualização de atributos com visualização imediata do resultado.
- **RN01 a RN08:** Validações de email, horas positivas, consistência de datas e integridade referencial.

## 🎥 Vídeo Demonstrativo

O vídeo apresenta o funcionamento do Sistema de Gerenciamento de Tarefas, desenvolvido em Python com banco de dados MySQL para a disciplina de Banco de Dados da FAESA, semestre 2026/2, sob orientação do professor Howard Roatti.

A demonstração inclui:
- Tela inicial (Splash Screen) e menu principal;
- Relatórios e consultas ao banco de dados;
- Inserção de registros;
- Atualização de registros;
- Remoção de registros;
- Encerramento do sistema.

▶️ [Clique aqui para assistir ao vídeo demonstrativo](https://youtu.be/u7krmySS0_I)