"""Módulo de conexão com o banco de dados MySQL (DB-API 2.0).

Configurar as credenciais abaixo conforme o ambiente da VM Linux da disciplina.
"""

import mysql.connector
from mysql.connector import Error


# ── Configuração de acesso ao banco ─────────────────────────────────
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "murilo123",            # preencher com a senha do MySQL da VM
    "database": "gerenciamento_tarefas",
    "charset": "utf8mb4",
    "collation": "utf8mb4_unicode_ci",
}


def conectar():
    """Abre e retorna uma conexão com o banco gerenciamento_tarefas.

    Retorna None e imprime o erro caso a conexão falhe.
    """
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
