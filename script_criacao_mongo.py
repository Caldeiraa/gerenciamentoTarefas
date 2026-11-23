
"""Script de criação das coleções MongoDB para o projeto C3.

Cria as coleções usuarios, projetos e tarefas no banco
gerenciamento_tarefas, caso ainda não existam.

Uso:
    python script_criacao_mongo.py
"""

from src.conexion.mongo_connection import (
    conectar_mongo,
    desconectar_mongo
)


COLECOES = ["usuarios", "projetos", "tarefas"]


def criar_colecoes(banco):
    """Cria as coleções necessárias, caso ainda não existam."""

    colecoes_existentes = banco.list_collection_names()

    for nome in COLECOES:
        if nome not in colecoes_existentes:
            banco.create_collection(nome)
            print(f"[OK] Coleção '{nome}' criada.")
        else:
            print(f"[INFO] Coleção '{nome}' já existe.")


def main():
    cliente, banco = conectar_mongo()

    if banco is None:
        print("[ERRO] Não foi possível conectar ao MongoDB.")
        return

    try:
        criar_colecoes(banco)
        print("\n[OK] Verificação das coleções concluída.")
    finally:
        desconectar_mongo(cliente)


if __name__ == "__main__":
    main()
