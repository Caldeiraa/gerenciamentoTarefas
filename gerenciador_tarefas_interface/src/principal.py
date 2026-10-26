"""Menu principal e ponto de integração com os módulos do grupo."""

from src.utils.config import OPCOES_MENU
from src.utils.splash_screen import exibir_tela_inicial


def exibir_menu():
    print("\n" + "=" * 44)
    print("GERENCIADOR DE TAREFAS - MENU PRINCIPAL")
    print("=" * 44)
    for codigo, descricao in OPCOES_MENU.items():
        print(f"  {codigo} - {descricao}")
    print("=" * 44)


def modulo_pendente(nome):
    print(f"\nO módulo '{nome}' será integrado pelo grupo.")


def executar(conexao=None, acoes=None):
    """Executa a interface; acoes mapeia opções às funções dos colegas.

    Exemplo: acoes={"1": funcao_relatorios, "2": funcao_inserir}.
    As funções integradas podem receber a conexão como argumento.
    """
    acoes = acoes or {}
    exibir_tela_inicial(conexao)
    while True:
        exibir_menu()
        try:
            opcao = input("Escolha uma opção (1-5): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando o sistema. Até logo!")
            break

        if opcao == "5":
            print("\nEncerrando o sistema. Até logo!")
            break
        if opcao not in OPCOES_MENU:
            print("\nOpção inválida. Digite um número de 1 a 5.")
            continue

        if opcao in acoes:
            try:
                acoes[opcao](conexao)
            except Exception as erro:
                print(f"\nErro ao executar o módulo: {erro}")
        else:
            modulo_pendente(OPCOES_MENU[opcao])


if __name__ == "__main__":
    executar()
