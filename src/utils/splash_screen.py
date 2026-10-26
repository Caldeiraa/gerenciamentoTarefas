"""Splash screen — tela inicial do sistema (RF01).

Exibe: nome do sistema, contagem de registros, integrantes, disciplina,
semestre e professor.
"""

from src.utils.config import (
    NOME_SISTEMA, DISCIPLINA, PROFESSOR, SEMESTRE, INTEGRANTES, TABELAS
)
from src.sql.queries import sql_contar_tabela


def _contar_registros(conexao):
    """Consulta a quantidade de registros em cada tabela."""
    resultado = {}
    cursor = conexao.cursor()
    try:
        for tabela in TABELAS:
            sql, params = sql_contar_tabela(tabela)
            cursor.execute(sql, params)
            resultado[tabela] = cursor.fetchone()[0]
    finally:
        cursor.close()
    return resultado


def exibir_splash_screen(conexao=None):
    """RF01 — Tela inicial com contagem de registros."""
    largura = 62
    print("\n" + "=" * largura)
    print(NOME_SISTEMA.center(largura))
    print("=" * largura)

    print("\nTOTAL DE REGISTROS EXISTENTES:")
    if conexao is None:
        print("  Banco de dados não conectado; contagem indisponível.")
    else:
        try:
            contagens = _contar_registros(conexao)
            for tabela, total in contagens.items():
                print(f"  {tabela.upper():<22}: {total}")
        except Exception as erro:
            print(f"  Não foi possível consultar os registros: {erro}")

    print("\nDESENVOLVIDO POR:")
    for integrante in INTEGRANTES:
        print(f"  - {integrante}")

    print(f"\nDISCIPLINA : {DISCIPLINA}")
    print(f"SEMESTRE   : {SEMESTRE}")
    print(f"PROFESSOR  : {PROFESSOR}")
    print("=" * largura)
    input("\nPressione Enter para continuar...")
