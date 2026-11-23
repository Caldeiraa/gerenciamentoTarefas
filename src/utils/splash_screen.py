
"""Tela inicial do sistema."""

from src.utils.config import (
    NOME_SISTEMA,
    DISCIPLINA,
    PROFESSOR,
    SEMESTRE,
    INTEGRANTES,
    TABELAS
)


def _contar_registros(banco):
    """Consulta a quantidade de documentos em cada coleção."""
    resultado = {}

    for colecao in TABELAS:
        resultado[colecao] = banco[colecao].count_documents({})

    return resultado


def exibir_splash_screen(banco=None):
    """Exibe a tela inicial com a contagem de registros."""
    largura = 62


    print("\n" + "=" * largura)
    print(NOME_SISTEMA.center(largura))
    print("=" * largura)

    print("\nTOTAL DE REGISTROS EXISTENTES:")

    if banco is None:
        print("  Banco de dados não conectado; contagem indisponível.")
    else:
        try:
            contagens = _contar_registros(banco)

            for colecao, total in contagens.items():
                print(f"  {colecao.upper():<22}: {total}")

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
