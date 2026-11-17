"""Script de criação e seed das coleções MongoDB para o projeto C3.

Este script pode ser executado antes de iniciar a aplicação para garantir que
as coleções ``usuarios``, ``projetos`` e ``tarefas`` existam e contenham
registros de exemplo compatíveis com o modelo relacional descrito em
``requisitosC3.txt``.

Uso:
    python script_criacao_mongo.py

O script:
  1. Conecta ao MongoDB usando ``src.conexion.db_connection.conectar``.
  2. Opcionalmente limpa as coleções existentes (``drop``) para evitar
     duplicação de dados ao ser reexecutado.
  3. Insere documentos de exemplo para usuários, projetos e tarefas,
     respeitando as chaves de referência ``id_usuario`` e ``id_projeto``.

Observação:
  - Caso o ambiente MongoDB exija autenticação, preencha os campos
    ``username`` e ``password`` em ``DB_CONFIG`` dentro de
    ``src/conexion/db_connection.py``.
  - Não há dependência de ORM/ODM; utilizamos apenas o driver ``pymongo``.
"""

from src.conexion.db_connection import conectar, desconectar
from pymongo.errors import DuplicateKeyError

# Dados de exemplo (conforme o modelo relacional da C2)
USUARIOS_EXEMPLO = [
    {"_id": 1, "nome_usuario": "Alice", "email_usuario": "alice@example.com", "cargo_usuario": "Desenvolvedor"},
    {"_id": 2, "nome_usuario": "Bob",   "email_usuario": "bob@example.com",   "cargo_usuario": "Gerente"},
    {"_id": 3, "nome_usuario": "Carol", "email_usuario": "carol@example.com", "cargo_usuario": "Analista"},
]

PROJETOS_EXEMPLO = [
    {"_id": 1, "nome_projeto": "Projeto Alpha", "descricao_projeto": "Primeiro projeto", "data_inicio_projeto": "2026-01-01", "data_fim_projeto": "2026-06-30"},
    {"_id": 2, "nome_projeto": "Projeto Beta",  "descricao_projeto": "Segundo projeto",  "data_inicio_projeto": "2026-07-01", "data_fim_projeto": None},
]

TAREFAS_EXEMPLO = [
    {
        "_id": 1,
        "titulo_tarefa": "Design da UI",
        "descricao_tarefa": "Criar mockups da interface",
        "status_tarefa": "PENDENTE",
        "prioridade_tarefa": "ALTA",
        "horas_gastas_tarefa": 0,
        "data_criacao_tarefa": "2026-02-10",
        "data_conclusao_tarefa": None,
        "id_projeto": 1,
        "id_usuario": 1,
    },
    {
        "_id": 2,
        "titulo_tarefa": "Implementação backend",
        "descricao_tarefa": "Desenvolver API REST",
        "status_tarefa": "EM_ANDAMENTO",
        "prioridade_tarefa": "MEDIA",
        "horas_gastas_tarefa": 12.5,
        "data_criacao_tarefa": "2026-03-01",
        "data_conclusao_tarefa": None,
        "id_projeto": 1,
        "id_usuario": 2,
    },
    {
        "_id": 3,
        "titulo_tarefa": "Testes unitários",
        "descricao_tarefa": "Cobertura > 80%",
        "status_tarefa": "CONCLUIDA",
        "prioridade_tarefa": "BAIXA",
        "horas_gastas_tarefa": 5,
        "data_criacao_tarefa": "2026-01-15",
        "data_conclusao_tarefa": "2026-01-20",
        "id_projeto": 2,
        "id_usuario": 3,
    },
]


def inserir_colecoes(db):
    """Insere as coleções e documentos de exemplo.

    Se a coleção já existir, os documentos são inseridos com ``_id``
    explícito; caso já existam, o erro ``DuplicateKeyError`` é ignorado.
    """
    # Usuários
    usuarios = db["usuarios"]
    for doc in USUARIOS_EXEMPLO:
        try:
            usuarios.insert_one(doc)
        except DuplicateKeyError:
            pass

    # Projetos
    projetos = db["projetos"]
    for doc in PROJETOS_EXEMPLO:
        try:
            projetos.insert_one(doc)
        except DuplicateKeyError:
            pass

    # Tarefas
    tarefas = db["tarefas"]
    for doc in TAREFAS_EXEMPLO:
        try:
            tarefas.insert_one(doc)
        except DuplicateKeyError:
            pass


def main():
    db = conectar()
    if not db:
        print("Falha ao conectar ao MongoDB. Verifique a configuração em src/conexion/db_connection.py")
        return
    # Opcional: limpar coleções existentes para ambiente de desenvolvimento
    # db.drop_collection("usuarios")
    # db.drop_collection("projetos")
    # db.drop_collection("tarefas")

    inserir_colecoes(db)
    print("Coleções criadas e dados de exemplo inseridos com sucesso.")
    desconectar(db)

if __name__ == "__main__":
    main()

