
"""Módulo de conexão com o banco de dados MongoDB."""

import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError


MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017/"
)

DB_NAME = os.getenv(
    "MONGO_DB_NAME",
    "gerenciamento_tarefas"
)


def conectar_mongo():
    """Abre a conexão e retorna o cliente e o banco MongoDB."""

    try:
        cliente = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000
        )

        # Verifica se o servidor está acessível.
        cliente.admin.command("ping")

        banco = cliente[DB_NAME]

        print("\n[OK] Conexão com MongoDB estabelecida.")

        return cliente, banco

    except PyMongoError as erro:
        print(f"\n[ERRO] Não foi possível conectar ao MongoDB: {erro}")
        return None, None


def desconectar_mongo(cliente):
    """Fecha a conexão com o MongoDB."""

    if cliente is not None:
        cliente.close()
        print("\n[OK] Conexão com MongoDB encerrada.")
