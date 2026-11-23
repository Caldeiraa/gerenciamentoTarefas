"""Script de criação das coleções no MongoDB e inserção de dados iniciais."""

from pymongo import ASCENDING
from pymongo.errors import PyMongoError

from src.conexion.mongo_connection import conectar_mongo, desconectar_mongo


# Coleções do sistema
COLECOES = ["usuarios", "projetos", "tarefas"]


# Dados iniciais para teste
SEED_USUARIOS = [
    {
        "_id": 1,
        "nome_usuario": "Murilo",
        "email_usuario": "murilo@exemplo.com",
        "cargo_usuario": "Analista",
    },
    {
        "_id": 2,
        "nome_usuario": "Davi",
        "email_usuario": "davi@exemplo.com",
        "cargo_usuario": "Desenvolvedor",
    },
    {
        "_id": 3,
        "nome_usuario": "George",
        "email_usuario": "george@exemplo.com",
        "cargo_usuario": "Desenvolvedor",
    },
]

SEED_PROJETOS = [
    {
        "_id": 1,
        "nome_projeto": "Trabalho de Banco de Dados",
        "descricao_projeto": "CRUD com MySQL",
        "data_inicio_projeto": "2026-10-01",
        "data_fim_projeto": "2026-10-30",
    },
    {
        "_id": 2,
        "nome_projeto": "Site da Turma",
        "descricao_projeto": "Página institucional",
        "data_inicio_projeto": "2026-10-05",
        "data_fim_projeto": None,
    },
]

SEED_TAREFAS = [
    {
        "_id": 1,
        "titulo_tarefa": "Modelar banco",
        "descricao_tarefa": "Diagrama no Mermaid",
        "status_tarefa": "CONCLUIDA",
        "prioridade_tarefa": "ALTA",
        "horas_gastas_tarefa": 4.50,
        "data_criacao_tarefa": "2026-10-02",
        "data_conclusao_tarefa": "2026-10-04",
        "id_projeto": 1,
        "id_usuario": 1,
    },
    {
        "_id": 2,
        "titulo_tarefa": "Criar script SQL",
        "descricao_tarefa": "Tabelas e restrições",
        "status_tarefa": "CONCLUIDA",
        "prioridade_tarefa": "ALTA",
        "horas_gastas_tarefa": 3.00,
        "data_criacao_tarefa": "2026-10-04",
        "data_conclusao_tarefa": "2026-10-05",
        "id_projeto": 1,
        "id_usuario": 1,
    },
    {
        "_id": 3,
        "titulo_tarefa": "Implementar CRUD",
        "descricao_tarefa": "Inserir/atualizar",
        "status_tarefa": "EM_ANDAMENTO",
        "prioridade_tarefa": "ALTA",
        "horas_gastas_tarefa": 6.25,
        "data_criacao_tarefa": "2026-10-06",
        "data_conclusao_tarefa": None,
        "id_projeto": 1,
        "id_usuario": 2,
    },
    {
        "_id": 4,
        "titulo_tarefa": "Criar menu e splash",
        "descricao_tarefa": "Interface console",
        "status_tarefa": "PENDENTE",
        "prioridade_tarefa": "MEDIA",
        "horas_gastas_tarefa": 0.00,
        "data_criacao_tarefa": "2026-10-06",
        "data_conclusao_tarefa": None,
        "id_projeto": 1,
        "id_usuario": 3,
    },
    {
        "_id": 5,
        "titulo_tarefa": "Definir layout",
        "descricao_tarefa": "Wireframe",
        "status_tarefa": "PENDENTE",
        "prioridade_tarefa": "BAIXA",
        "horas_gastas_tarefa": 0.00,
        "data_criacao_tarefa": "2026-10-07",
        "data_conclusao_tarefa": None,
        "id_projeto": 2,
        "id_usuario": 3,
    },
]


def criar_colecoes(banco):
    """Cria as coleções caso ainda não existam."""
    colecoes_existentes = banco.list_collection_names()

    for nome in COLECOES:
        if nome not in colecoes_existentes:
            banco.create_collection(nome)
            print(f"  [OK] Coleção '{nome}' criada.")
        else:
            print(f"  [INFO] Coleção '{nome}' já existe.")


def criar_indices(banco):
    """Cria os índices das coleções."""
    banco["usuarios"].create_index(
        [("email_usuario", ASCENDING)],
        unique=True,
        name="idx_usuarios_email_unique",
    )
    print("  [OK] Índice único criado em usuarios.email_usuario")

    banco["tarefas"].create_index(
        [("id_projeto", ASCENDING)],
        name="idx_tarefas_projeto",
    )
    print("  [OK] Índice criado em tarefas.id_projeto")

    banco["tarefas"].create_index(
        [("id_usuario", ASCENDING)],
        name="idx_tarefas_usuario",
    )
    print("  [OK] Índice criado em tarefas.id_usuario")


def inserir_seed(banco):
    """Insere os dados iniciais se as coleções estiverem vazias."""
    if banco["usuarios"].count_documents({}) == 0:
        banco["usuarios"].insert_many(SEED_USUARIOS)
        print(f"  [OK] {len(SEED_USUARIOS)} usuário(s) inserido(s).")
    else:
        print(f"  [INFO] Coleção 'usuarios' já contém dados.")

    if banco["projetos"].count_documents({}) == 0:
        banco["projetos"].insert_many(SEED_PROJETOS)
        print(f"  [OK] {len(SEED_PROJETOS)} projeto(s) inserido(s).")
    else:
        print(f"  [INFO] Coleção 'projetos' já contém dados.")

    if banco["tarefas"].count_documents({}) == 0:
        banco["tarefas"].insert_many(SEED_TAREFAS)
        print(f"  [OK] {len(SEED_TAREFAS)} tarefa(s) inserida(s).")
    else:
        print(f"  [INFO] Coleção 'tarefas' já contém dados.")



# ---------------------------------------------------------------------------
#  Ponto de entrada
# ---------------------------------------------------------------------------

def main():
    """Executa a criação das coleções, índices e inserção dos dados seed."""
    cliente, banco = conectar_mongo()

    if banco is None:
        print("[ERRO] Não foi possível conectar ao MongoDB.")
        return

    try:
        print("\n1) Verificando coleções...")
        criar_colecoes(banco)

        print("\n2) Criando índices...")
        criar_indices(banco)

        print("\n3) Inserindo dados pré-cadastrados (seed)...")
        inserir_seed(banco)

        print("\n[OK] Script de criação/migração concluído com sucesso.")

    except PyMongoError as e:
        print(f"\n[ERRO] Falha durante a execução do script: {e}")

    finally:
        desconectar_mongo(cliente)


if __name__ == "__main__":
    main()
