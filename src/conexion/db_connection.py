import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError


# Configuração de acesso ao MongoDB
DB_CONFIG = {
    "host": os.getenv("MONGO_HOST", "localhost"),
    "port": int(os.getenv("MONGO_PORT", "27017")),
    "username": os.getenv("MONGO_USER"),
    "password": os.getenv("MONGO_PASSWORD"),
    "authSource": os.getenv("MONGO_AUTH_DB", "admin"),
    "database": os.getenv("MONGO_DB_NAME", "gerenciamento_tarefas"),
}


def _criar_uri(config):
    auth_part = ""
    if config.get("username"):
        auth_part = f"{config['username']}:{config['password']}@"
    host = config.get("host", "localhost")
    port = config.get("port", 27017)
    return f"mongodb://{auth_part}{host}:{port}/"


def conectar():
    """Conecta ao MongoDB e retorna o banco de dados."""
    try:
        uri = _criar_uri(DB_CONFIG)
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        return client[DB_CONFIG["database"]]
    except PyMongoError as e:
        print(f"\n[ERRO] Não foi possível conectar ao MongoDB: {e}")
    return None


def desconectar(db):
    """Fecha a conexão com o MongoDB."""
    if db is not None and hasattr(db, "client"):
        db.client.close()



