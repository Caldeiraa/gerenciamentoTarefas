
from pymongo import MongoClient


# Configuração de acesso ao MongoDB
DB_CONFIG = {
    "host": "localhost",
    "port": 27017,
    "username": None,   # opcional, preencher se houver autenticação
    "password": None,   # opcional
    "authSource": "admin",
    "database": "gerenciamento_tarefas",
}

def _criar_uri(config):
    """Constrói a URI de conexão a partir do dicionário DB_CONFIG."""
    auth_part = ""
    if config.get("username"):
        auth_part = f"{config['username']}:{config['password']}@"
    host = config.get("host", "localhost")
    port = config.get("port", 27017)
    return f"mongodb://{auth_part}{host}:{port}/"

def conectar():
    """Abre e retorna um cliente MongoClient conectado ao banco 'gerenciamento_tarefas'.

    Retorna None e imprime o erro caso a conexão falhe.
    """
    try:
        uri = _criar_uri(DB_CONFIG)
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # Verifica a conexão
        client.admin.command('ping')
        return client[DB_CONFIG["database"]]
    except PyMongoError as e:
        print(f"\n[ERRO] Não foi possível conectar ao MongoDB: {e}")
    return None

def desconectar(db):
    """Fecha a conexão ao MongoDB, caso esteja aberta."""
    # PyMongo libera recursos ao fechar o cliente; aqui garantimos o fechamento explícito.
    if hasattr(db, "client"):
        db.client.close()

