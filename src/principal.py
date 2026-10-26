"""Módulo principal — ponto de entrada e integração de todos os módulos.

Responsável pelo fluxo do programa: splash screen → menu principal → ações.
Estrutura conforme RNF04: model, controller, conexion, sql, reports, utils, principal.
"""

from src.conexion.db_connection import conectar, desconectar
from src.utils.config import OPCOES_MENU
from src.utils.splash_screen import exibir_splash_screen
from src.reports.reports import menu_relatorios
from src.controller import controller


# ═══════════════════════════════════════════════════════════════════
#  MENUS DE INSERÇÃO (RF04)
# ═══════════════════════════════════════════════════════════════════

def _menu_inserir_entidade(conexao):
    """RF04 — Menu de entidades → escolha → inserção → repetir."""
    while True:
        print("\n" + "=" * 44)
        print("         INSERIR REGISTROS")
        print("=" * 44)
        print("  1 - Usuário")
        print("  2 - Projeto")
        print("  3 - Tarefa")
        print("  0 - Voltar ao menu principal")
        print("=" * 44)
        try:
            opcao = input("Escolha a entidade (0-3): ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if opcao == "0":
            break
        elif opcao == "1":
            _inserir_usuario(conexao)
        elif opcao == "2":
            _inserir_projeto(conexao)
        elif opcao == "3":
            _inserir_tarefa(conexao)
        else:
            print("\nOpção inválida.")


def _inserir_usuario(conexao):
    while True:
        print("\n--- INSERIR USUÁRIO ---")
        try:
            nome = input("Nome: ").strip()
            email = input("E-mail: ").strip()
            cargo = input("Cargo (ou Enter para vazio): ").strip() or None
            u = controller.inserir_usuario(conexao, nome, email, cargo)
            print(f"\n✓ Usuário inserido com sucesso: {u}")
        except ValueError as e:
            print(f"\n✗ {e}")
        if input("\nDeseja inserir outro usuário? (S/N): ").strip().upper() != "S":
            break


def _inserir_projeto(conexao):
    while True:
        print("\n--- INSERIR PROJETO ---")
        try:
            nome = input("Nome do projeto: ").strip()
            descricao = input("Descrição (ou Enter para vazio): ").strip() or None
            data_inicio = input("Data de início (AAAA-MM-DD): ").strip()
            data_fim = input("Data de término (AAAA-MM-DD ou Enter para nulo): ").strip() or None
            p = controller.inserir_projeto(conexao, nome, descricao, data_inicio, data_fim)
            print(f"\n✓ Projeto inserido com sucesso: {p}")
        except ValueError as e:
            print(f"\n✗ {e}")
        if input("\nDeseja inserir outro projeto? (S/N): ").strip().upper() != "S":
            break


def _inserir_tarefa(conexao):
    while True:
        print("\n--- INSERIR TAREFA ---")
        try:
            titulo = input("Título: ").strip()
            descricao = input("Descrição (ou Enter para vazio): ").strip() or None
            status = input("Status (PENDENTE / EM_ANDAMENTO / CONCLUIDA): ").strip().upper()
            prioridade = input("Prioridade (BAIXA / MEDIA / ALTA): ").strip().upper()
            horas = input("Horas gastas: ").strip()
            data_criacao = input("Data de criação (AAAA-MM-DD): ").strip()
            data_conclusao = input("Data de conclusão (AAAA-MM-DD ou Enter): ").strip() or None
            id_projeto = int(input("ID do projeto: ").strip())
            id_usuario = int(input("ID do usuário responsável: ").strip())
            t = controller.inserir_tarefa(
                conexao, titulo, descricao, status, prioridade,
                horas, data_criacao, data_conclusao, id_projeto, id_usuario
            )
            print(f"\n✓ Tarefa inserida com sucesso: {t}")
        except ValueError as e:
            print(f"\n✗ {e}")
        if input("\nDeseja inserir outra tarefa? (S/N): ").strip().upper() != "S":
            break


# ═══════════════════════════════════════════════════════════════════
#  MENUS DE REMOÇÃO (RF05)
# ═══════════════════════════════════════════════════════════════════

def _menu_remover_entidade(conexao):
    """RF05 — Menu de entidades → listagem → seleção → confirmação → remoção."""
    while True:
        print("\n" + "=" * 44)
        print("         REMOVER REGISTROS")
        print("=" * 44)
        print("  1 - Usuário")
        print("  2 - Projeto")
        print("  3 - Tarefa")
        print("  0 - Voltar ao menu principal")
        print("=" * 44)
        try:
            opcao = input("Escolha a entidade (0-3): ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if opcao == "0":
            break
        elif opcao == "1":
            _remover_usuario(conexao)
        elif opcao == "2":
            _remover_projeto(conexao)
        elif opcao == "3":
            _remover_tarefa(conexao)
        else:
            print("\nOpção inválida.")


def _remover_usuario(conexao):
    while True:
        print("\n--- REMOVER USUÁRIO ---")
        usuarios = controller.listar_usuarios(conexao)
        if not usuarios:
            print("  Nenhum usuário cadastrado.")
            break
        for u in usuarios:
            print(f"  ID: {u.id_usuario} | Nome: {u.nome_usuario}")
        try:
            id_u = int(input("\nDigite o ID do usuário para remover: ").strip())
            confirmacao = input(f"Confirma exclusão do ID {id_u}? (S/N): ").strip().upper()
            if confirmacao == "S":
                try:
                    controller.excluir_usuario(conexao, id_u)
                    print(f"\n✓ Usuário ID {id_u} excluído com sucesso.")
                except ValueError as e:
                    if "tarefa(s) vinculada(s)" in str(e):
                        print(f"\n⚠ {e}")
                        cascata = input("Deseja excluir também as tarefas vinculadas? (S/N): ").strip().upper()
                        if cascata == "S":
                            controller.excluir_usuario(conexao, id_u, excluir_filhos=True)
                            print(f"\n✓ Usuário ID {id_u} e suas tarefas excluídos.")
                        else:
                            print("Operação cancelada.")
                    else:
                        print(f"\n✗ {e}")
            else:
                print("Operação cancelada.")
        except ValueError as e:
            print(f"\n✗ {e}")
        if input("\nDeseja remover outro usuário? (S/N): ").strip().upper() != "S":
            break


def _remover_projeto(conexao):
    while True:
        print("\n--- REMOVER PROJETO ---")
        projetos = controller.listar_projetos(conexao)
        if not projetos:
            print("  Nenhum projeto cadastrado.")
            break
        for p in projetos:
            print(f"  ID: {p.id_projeto} | Nome: {p.nome_projeto}")
        try:
            id_p = int(input("\nDigite o ID do projeto para remover: ").strip())
            confirmacao = input(f"Confirma exclusão do ID {id_p}? (S/N): ").strip().upper()
            if confirmacao == "S":
                try:
                    controller.excluir_projeto(conexao, id_p)
                    print(f"\n✓ Projeto ID {id_p} excluído com sucesso.")
                except ValueError as e:
                    if "tarefa(s) vinculada(s)" in str(e):
                        print(f"\n⚠ {e}")
                        cascata = input("Deseja excluir também as tarefas vinculadas? (S/N): ").strip().upper()
                        if cascata == "S":
                            controller.excluir_projeto(conexao, id_p, excluir_filhos=True)
                            print(f"\n✓ Projeto ID {id_p} e suas tarefas excluídos.")
                        else:
                            print("Operação cancelada.")
                    else:
                        print(f"\n✗ {e}")
            else:
                print("Operação cancelada.")
        except ValueError as e:
            print(f"\n✗ {e}")
        if input("\nDeseja remover outro projeto? (S/N): ").strip().upper() != "S":
            break


def _remover_tarefa(conexao):
    while True:
        print("\n--- REMOVER TAREFA ---")
        tarefas = controller.listar_tarefas(conexao)
        if not tarefas:
            print("  Nenhuma tarefa cadastrada.")
            break
        for t in tarefas:
            print(f"  ID: {t.id_tarefa} | Título: {t.titulo_tarefa}")
        try:
            id_t = int(input("\nDigite o ID da tarefa para remover: ").strip())
            confirmacao = input(f"Confirma exclusão do ID {id_t}? (S/N): ").strip().upper()
            if confirmacao == "S":
                controller.excluir_tarefa(conexao, id_t)
                print(f"\n✓ Tarefa ID {id_t} excluída com sucesso.")
            else:
                print("Operação cancelada.")
        except ValueError as e:
            print(f"\n✗ {e}")
        if input("\nDeseja remover outra tarefa? (S/N): ").strip().upper() != "S":
            break


# ═══════════════════════════════════════════════════════════════════
#  MENUS DE ATUALIZAÇÃO (RF06)
# ═══════════════════════════════════════════════════════════════════

def _menu_atualizar_entidade(conexao):
    """RF06 — Menu → listagem → seleção → novos valores → exibir atualizado."""
    while True:
        print("\n" + "=" * 44)
        print("         ATUALIZAR REGISTROS")
        print("=" * 44)
        print("  1 - Usuário")
        print("  2 - Projeto")
        print("  3 - Tarefa")
        print("  0 - Voltar ao menu principal")
        print("=" * 44)
        try:
            opcao = input("Escolha a entidade (0-3): ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if opcao == "0":
            break
        elif opcao == "1":
            _atualizar_usuario(conexao)
        elif opcao == "2":
            _atualizar_projeto(conexao)
        elif opcao == "3":
            _atualizar_tarefa(conexao)
        else:
            print("\nOpção inválida.")


def _atualizar_usuario(conexao):
    while True:
        print("\n--- ATUALIZAR USUÁRIO ---")
        usuarios = controller.listar_usuarios(conexao)
        if not usuarios:
            print("  Nenhum usuário cadastrado.")
            break
        for u in usuarios:
            print(f"  ID: {u.id_usuario} | Nome: {u.nome_usuario} | E-mail: {u.email_usuario} | Cargo: {u.cargo_usuario}")
        try:
            id_u = int(input("\nDigite o ID do usuário para atualizar: ").strip())
            atual = controller.buscar_usuario(conexao, id_u)
            if not atual:
                print(f"\n✗ Usuário ID {id_u} não encontrado.")
                continue
            print(f"\nValores atuais: {atual}")
            print("(Pressione Enter para manter o valor atual)")
            nome = input(f"Novo nome [{atual.nome_usuario}]: ").strip() or atual.nome_usuario
            email = input(f"Novo e-mail [{atual.email_usuario}]: ").strip() or atual.email_usuario
            cargo = input(f"Novo cargo [{atual.cargo_usuario}]: ").strip() or atual.cargo_usuario
            atualizado = controller.atualizar_usuario(conexao, id_u, nome, email, cargo)
            print(f"\n✓ Registro atualizado: {atualizado}")
        except ValueError as e:
            print(f"\n✗ {e}")
        if input("\nDeseja atualizar outro usuário? (S/N): ").strip().upper() != "S":
            break


def _atualizar_projeto(conexao):
    while True:
        print("\n--- ATUALIZAR PROJETO ---")
        projetos = controller.listar_projetos(conexao)
        if not projetos:
            print("  Nenhum projeto cadastrado.")
            break
        for p in projetos:
            print(f"  ID: {p.id_projeto} | Nome: {p.nome_projeto} | Início: {p.data_inicio_projeto} | Fim: {p.data_fim_projeto}")
        try:
            id_p = int(input("\nDigite o ID do projeto para atualizar: ").strip())
            atual = controller.buscar_projeto(conexao, id_p)
            if not atual:
                print(f"\n✗ Projeto ID {id_p} não encontrado.")
                continue
            print(f"\nValores atuais: {atual}")
            print("(Pressione Enter para manter o valor atual)")
            nome = input(f"Novo nome [{atual.nome_projeto}]: ").strip() or atual.nome_projeto
            descricao = input(f"Nova descrição [{atual.descricao_projeto}]: ").strip() or atual.descricao_projeto
            di = input(f"Nova data início [{atual.data_inicio_projeto}]: ").strip() or str(atual.data_inicio_projeto)
            df = input(f"Nova data fim [{atual.data_fim_projeto}]: ").strip() or (str(atual.data_fim_projeto) if atual.data_fim_projeto else None)
            atualizado = controller.atualizar_projeto(conexao, id_p, nome, descricao, di, df)
            print(f"\n✓ Registro atualizado: {atualizado}")
        except ValueError as e:
            print(f"\n✗ {e}")
        if input("\nDeseja atualizar outro projeto? (S/N): ").strip().upper() != "S":
            break


def _atualizar_tarefa(conexao):
    while True:
        print("\n--- ATUALIZAR TAREFA ---")
        tarefas = controller.listar_tarefas(conexao)
        if not tarefas:
            print("  Nenhuma tarefa cadastrada.")
            break
        for t in tarefas:
            print(f"  ID: {t.id_tarefa} | Título: {t.titulo_tarefa} | Status: {t.status_tarefa}")
        try:
            id_t = int(input("\nDigite o ID da tarefa para atualizar: ").strip())
            atual = controller.buscar_tarefa(conexao, id_t)
            if not atual:
                print(f"\n✗ Tarefa ID {id_t} não encontrada.")
                continue
            print(f"\nValores atuais: {atual}")
            print("(Pressione Enter para manter o valor atual)")
            titulo = input(f"Novo título [{atual.titulo_tarefa}]: ").strip() or atual.titulo_tarefa
            descricao = input(f"Nova descrição [{atual.descricao_tarefa}]: ").strip() or atual.descricao_tarefa
            status = input(f"Novo status [{atual.status_tarefa}]: ").strip().upper() or atual.status_tarefa
            prioridade = input(f"Nova prioridade [{atual.prioridade_tarefa}]: ").strip().upper() or atual.prioridade_tarefa
            horas = input(f"Horas gastas [{atual.horas_gastas_tarefa}]: ").strip() or str(atual.horas_gastas_tarefa)
            dc = input(f"Data criação [{atual.data_criacao_tarefa}]: ").strip() or str(atual.data_criacao_tarefa)
            dconcl = input(f"Data conclusão [{atual.data_conclusao_tarefa}]: ").strip() or (str(atual.data_conclusao_tarefa) if atual.data_conclusao_tarefa else None)
            id_proj = input(f"ID projeto [{atual.id_projeto}]: ").strip() or str(atual.id_projeto)
            id_usr = input(f"ID usuário [{atual.id_usuario}]: ").strip() or str(atual.id_usuario)
            atualizado = controller.atualizar_tarefa(
                conexao, id_t, titulo, descricao, status, prioridade,
                horas, dc, dconcl, int(id_proj), int(id_usr)
            )
            print(f"\n✓ Registro atualizado: {atualizado}")
        except ValueError as e:
            print(f"\n✗ {e}")
        if input("\nDeseja atualizar outra tarefa? (S/N): ").strip().upper() != "S":
            break


# ═══════════════════════════════════════════════════════════════════
#  MENU PRINCIPAL (RF02)
# ═══════════════════════════════════════════════════════════════════

def _exibir_menu():
    print("\n" + "=" * 52)
    print("   GERENCIADOR DE TAREFAS — MENU PRINCIPAL")
    print("=" * 52)
    for codigo, descricao in OPCOES_MENU.items():
        print(f"    {codigo} — {descricao}")
    print("=" * 52)


def main():
    """Fluxo completo: conexão → splash → menu → ações → desconexão."""
    conexao = conectar()
    if conexao is None:
        print("\n[ERRO] Não foi possível iniciar o sistema sem conexão com o banco.")
        print("Verifique as configurações em src/conexion/db_connection.py")
        return

    try:
        # RF01 — Splash screen
        exibir_splash_screen(conexao)

        # RF02 — Menu principal exibido continuamente
        while True:
            _exibir_menu()
            try:
                opcao = input("Escolha uma opção (1-5): ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n\nEncerrando o sistema. Até logo!")
                break

            if opcao == "1":
                menu_relatorios(conexao)
            elif opcao == "2":
                _menu_inserir_entidade(conexao)
            elif opcao == "3":
                _menu_remover_entidade(conexao)
            elif opcao == "4":
                _menu_atualizar_entidade(conexao)
            elif opcao == "5":
                print("\nEncerrando o sistema. Até logo!")
                break
            else:
                print("\nOpção inválida. Digite um número de 1 a 5.")
    finally:
        desconectar(conexao)


if __name__ == "__main__":
    main()
