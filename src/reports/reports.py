"""Módulo de relatórios (RF03).

RF03.1 — Resumo por usuário (GROUP BY)
RF03.2 — Tarefas com nome do projeto e responsável (JOIN)
RF03.3 — Tarefas por projeto e por status (opcional)
"""


# ═══════════════════════════════════════════════════════════════════
#  SQL dos relatórios (concatenação de texto, sem ORM)
# ═══════════════════════════════════════════════════════════════════

_SQL_RELATORIO_USUARIO = (
    "SELECT u.nome_usuario, "
    "COUNT(t.id_tarefa) AS total_tarefas, "
    "SUM(CASE WHEN t.status_tarefa = 'CONCLUIDA' THEN 1 ELSE 0 END) AS concluidas, "
    "COALESCE(SUM(t.horas_gastas_tarefa), 0) AS horas_totais "
    "FROM usuarios u "
    "LEFT JOIN tarefas t ON t.id_usuario = u.id_usuario "
    "GROUP BY u.id_usuario, u.nome_usuario "
    "ORDER BY horas_totais DESC"
)

_SQL_TAREFAS_DETALHADAS = (
    "SELECT t.id_tarefa, t.titulo_tarefa, p.nome_projeto, u.nome_usuario, "
    "t.status_tarefa, t.prioridade_tarefa, t.horas_gastas_tarefa "
    "FROM tarefas t "
    "INNER JOIN projetos p ON p.id_projeto = t.id_projeto "
    "INNER JOIN usuarios u ON u.id_usuario = t.id_usuario "
    "ORDER BY p.nome_projeto, t.id_tarefa"
)

_SQL_TAREFAS_PROJETO_STATUS = (
    "SELECT p.nome_projeto, t.status_tarefa, COUNT(t.id_tarefa) AS qtd "
    "FROM tarefas t "
    "INNER JOIN projetos p ON p.id_projeto = t.id_projeto "
    "GROUP BY p.nome_projeto, t.status_tarefa "
    "ORDER BY p.nome_projeto, t.status_tarefa"
)


# ═══════════════════════════════════════════════════════════════════
#  Funções de exibição
# ═══════════════════════════════════════════════════════════════════

def _linha(largura=72):
    print("-" * largura)


def relatorio_resumo_usuario(conexao):
    """RF03.1 — GROUP BY: total de tarefas, concluídas e horas por usuário."""
    print("\n" + "=" * 72)
    print("RELATÓRIO 1 — Resumo por Usuário (GROUP BY)")
    print("=" * 72)
    cursor = conexao.cursor()
    try:
        cursor.execute(_SQL_RELATORIO_USUARIO)
        rows = cursor.fetchall()
        if not rows:
            print("  Nenhum registro encontrado.")
            return
        print(f"  {'USUÁRIO':<20} {'TOTAL':>8} {'CONCLUÍDAS':>12} {'HORAS':>10}")
        _linha()
        for row in rows:
            nome, total, concluidas, horas = row
            print(f"  {nome:<20} {total:>8} {concluidas:>12} {horas:>10.2f}")
        _linha()
    finally:
        cursor.close()


def relatorio_tarefas_detalhadas(conexao):
    """RF03.2 — JOIN: tarefas com nome do projeto e responsável."""
    print("\n" + "=" * 72)
    print("RELATÓRIO 2 — Tarefas Detalhadas (JOIN)")
    print("=" * 72)
    cursor = conexao.cursor()
    try:
        cursor.execute(_SQL_TAREFAS_DETALHADAS)
        rows = cursor.fetchall()
        if not rows:
            print("  Nenhuma tarefa encontrada.")
            return
        print(f"  {'ID':>4} {'TÍTULO':<22} {'PROJETO':<20} {'RESPONSÁVEL':<15} {'STATUS':<14} {'PRIOR.':<8} {'HORAS':>6}")
        _linha()
        for row in rows:
            id_t, titulo, projeto, usuario, status, prior, horas = row
            print(f"  {id_t:>4} {titulo:<22} {projeto:<20} {usuario:<15} {status:<14} {prior:<8} {horas:>6.2f}")
        _linha()
    finally:
        cursor.close()


def relatorio_tarefas_projeto_status(conexao):
    """RF03.3 — Tarefas por projeto e por status (opcional)."""
    print("\n" + "=" * 72)
    print("RELATÓRIO 3 — Tarefas por Projeto e Status")
    print("=" * 72)
    cursor = conexao.cursor()
    try:
        cursor.execute(_SQL_TAREFAS_PROJETO_STATUS)
        rows = cursor.fetchall()
        if not rows:
            print("  Nenhum registro encontrado.")
            return
        print(f"  {'PROJETO':<30} {'STATUS':<16} {'QTD':>6}")
        _linha()
        for row in rows:
            projeto, status, qtd = row
            print(f"  {projeto:<30} {status:<16} {qtd:>6}")
        _linha()
    finally:
        cursor.close()


def menu_relatorios(conexao):
    """Submenu de relatórios integrado ao menu principal."""
    while True:
        print("\n" + "=" * 44)
        print("         RELATÓRIOS")
        print("=" * 44)
        print("  1 - Resumo por usuário (GROUP BY)")
        print("  2 - Tarefas detalhadas (JOIN)")
        print("  3 - Tarefas por projeto e status")
        print("  0 - Voltar ao menu principal")
        print("=" * 44)
        try:
            opcao = input("Escolha uma opção (0-3): ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if opcao == "1":
            relatorio_resumo_usuario(conexao)
        elif opcao == "2":
            relatorio_tarefas_detalhadas(conexao)
        elif opcao == "3":
            relatorio_tarefas_projeto_status(conexao)
        elif opcao == "0":
            break
        else:
            print("\nOpção inválida. Digite um número de 0 a 3.")

        input("\nPressione Enter para continuar...")
