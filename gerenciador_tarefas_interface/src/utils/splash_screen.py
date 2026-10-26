"""Tela inicial e contagem de registros no banco relacional."""

from src.utils.config import NOME_SISTEMA, DISCIPLINA, PROFESSOR, SEMESTRE, INTEGRANTES, TABELAS


def contar_registros(conexao, tabelas=None):
    """Retorna a contagem real de cada tabela usando uma conexão DB-API.

    A conexão deve ser criada pelo módulo de conexão do grupo.
    """
    if conexao is None:
        return None

    resultado = {}
    cursor = conexao.cursor()
    try:
        for tabela in (tabelas if tabelas is not None else TABELAS):
            # Apenas nomes definidos no código; nunca receber nome de tabela do usuário.
            if tabela not in TABELAS:
                raise ValueError("Tabela não autorizada: " + tabela)
            cursor.execute(f"SELECT COUNT(1) AS total_{tabela} FROM {tabela}")
            resultado[tabela] = cursor.fetchone()[0]
    finally:
        cursor.close()
    return resultado


def exibir_tela_inicial(conexao=None):
    largura = 62
    print("\n" + "=" * largura)
    print(NOME_SISTEMA.center(largura))
    print("=" * largura)
    print("TOTAL DE REGISTROS EXISTENTES")
    if conexao is None:
        print("  Banco de dados não conectado; contagem indisponível.")
    else:
        try:
            for tabela, total in contar_registros(conexao).items():
                print(f"  {tabela.upper():<22}: {total}")
        except Exception as erro:
            print(f"  Não foi possível consultar os registros: {erro}")
    print("\nDESENVOLVIDO POR:")
    for integrante in INTEGRANTES:
        print("  - " + integrante)
    print(f"\nDISCIPLINA: {DISCIPLINA}")
    print(f"SEMESTRE: {SEMESTRE}")
    print(f"PROFESSOR: {PROFESSOR}")
    print("=" * largura)
