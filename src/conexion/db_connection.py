
"""Módulo de conexão com o banco de dados MySQL."""

import os
import mysql.connector
from mysql.connector import Error


# Configurações obtidas das variáveis de ambiente.
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "gerenciamento_tarefas"),
    "charset": "utf8mb4",
    "collation": "utf8mb4_unicode_ci",
}


def conectar():
    """Abre e retorna uma conexão com o banco de dados."""

    if not DB_CONFIG["password"]:
        print(
            "\n[ERRO] A variável de ambiente DB_PASSWORD não foi configurada."
        )
        return None

    try:
        conexao = mysql.connector.connect(**DB_CONFIG)

        if conexao.is_connected():
            return conexao

    except Error as e:
        print(f"\n[ERRO] Não foi possível conectar ao banco de dados: {e}")

    return None


def desconectar(conexao):
    """Fecha a conexão, se estiver ativa."""

    if conexao and conexao.is_connected():
        conexao.close()
