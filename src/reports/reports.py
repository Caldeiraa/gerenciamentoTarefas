
"""Módulo de relatórios (RF03).

RF03.1 — Resumo por usuário (AGGREGATE)
RF03.2 — Tarefas com nome do projeto e responsável (LOOKUP)
RF03.3 — Tarefas por projeto e por status (AGGREGATE)
"""


def _linha(largura=72):
    print("-" * largura)


def relatorio_resumo_usuario(banco):
    """RF03.1 — Total de tarefas, concluídas e horas por usuário."""

    print("\n" + "=" * 72)
    print("RELATÓRIO 1 — Resumo por Usuário (AGGREGATE)")
    print("=" * 72)

    pipeline = [
        {
            "$lookup": {
                "from": "tarefas",
                "localField": "_id",
                "foreignField": "id_usuario",
                "as": "tarefas"
            }
        },
        {"$unwind": {"path": "$tarefas", "preserveNullAndEmptyArrays": True}},
        {
            "$group": {
                "_id": "$_id",
                "nome_usuario": {"$first": "$nome_usuario"},
                "total_tarefas": {
                    "$sum": {
                        "$cond": [{"$ne": ["$tarefas._id", None]}, 1, 0]
                    }
                },
                "concluidas": {
                    "$sum": {
                        "$cond": [
                            {"$eq": ["$tarefas.status_tarefa", "CONCLUIDA"]},
                            1,
                            0
                        ]
                    }
                },
                "horas_totais": {
                    "$sum": {"$ifNull": ["$tarefas.horas_gastas_tarefa", 0]}
                }
            }
        },
        {"$sort": {"horas_totais": -1}}
    ]

    rows = list(banco["usuarios"].aggregate(pipeline))

    if not rows:
        print("  Nenhum registro encontrado.")
        return

    print(f"  {'USUÁRIO':<20} {'TOTAL':>8} {'CONCLUÍDAS':>12} {'HORAS':>10}")
    _linha()

    for row in rows:
        nome = row.get("nome_usuario", "")
        total = row.get("total_tarefas", 0)
        concluidas = row.get("concluidas", 0)
        horas = row.get("horas_totais", 0)

        print(f"  {nome:<20} {total:>8} {concluidas:>12} {horas:>10.2f}")

    _linha()


def relatorio_tarefas_detalhadas(banco):
    """RF03.2 — Tarefas com nome do projeto e responsável."""

    print("\n" + "=" * 72)
    print("RELATÓRIO 2 — Tarefas Detalhadas (LOOKUP)")
    print("=" * 72)

    pipeline = [
        {
            "$lookup": {
                "from": "projetos",
                "localField": "id_projeto",
                "foreignField": "_id",
                "as": "projeto"
            }
        },
        {
            "$lookup": {
                "from": "usuarios",
                "localField": "id_usuario",
                "foreignField": "_id",
                "as": "usuario"
            }
        },
        {
            "$unwind": {
                "path": "$projeto",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$unwind": {
                "path": "$usuario",
                "preserveNullAndEmptyArrays": True
            }
        },
        {"$sort": {"_id": 1}}
    ]

    rows = list(banco["tarefas"].aggregate(pipeline))

    if not rows:
        print("  Nenhuma tarefa encontrada.")
        return

    print(
        f"  {'ID':>4} {'TÍTULO':<22} {'PROJETO':<20} "
        f"{'RESPONSÁVEL':<15} {'STATUS':<14} {'PRIOR.':<8} {'HORAS':>6}"
    )
    _linha()

    for row in rows:
        id_t = row.get("_id", 0)
        titulo = row.get("titulo_tarefa", "")
        projeto = row.get("projeto", {}).get("nome_projeto", "Não informado")
        usuario = row.get("usuario", {}).get("nome_usuario", "Não informado")
        status = row.get("status_tarefa", "")
        prioridade = row.get("prioridade_tarefa", "")
        horas = row.get("horas_gastas_tarefa", 0)

        print(
            f"  {id_t:>4} {titulo:<22} {projeto:<20} "
            f"{usuario:<15} {status:<14} {prioridade:<8} {horas:>6.2f}"
        )

    _linha()


def relatorio_tarefas_projeto_status(banco):
    """RF03.3 — Quantidade de tarefas por projeto e status."""

    print("\n" + "=" * 72)
    print("RELATÓRIO 3 — Tarefas por Projeto e Status")
    print("=" * 72)

    pipeline = [
        {
            "$group": {
                "_id": {
                    "id_projeto": "$id_projeto",
                    "status": "$status_tarefa"
                },
                "quantidade": {"$sum": 1}
            }
        },
        {
            "$lookup": {
                "from": "projetos",
                "localField": "_id.id_projeto",
                "foreignField": "_id",
                "as": "projeto"
            }
        },
        {
            "$unwind": {
                "path": "$projeto",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$project": {
                "_id": 0,
                "nome_projeto": {
                    "$ifNull": ["$projeto.nome_projeto", "Não informado"]
                },
                "status": "$_id.status",
                "quantidade": 1
            }
        },
        {"$sort": {"nome_projeto": 1, "status": 1}}
    ]

    rows = list(banco["tarefas"].aggregate(pipeline))

    if not rows:
        print("  Nenhum registro encontrado.")
        return

    print(f"  {'PROJETO':<30} {'STATUS':<16} {'QTD':>6}")
    _linha()

    for row in rows:
        projeto = row.get("nome_projeto", "")
        status = row.get("status", "")
        quantidade = row.get("quantidade", 0)

        print(f"  {projeto:<30} {status:<16} {quantidade:>6}")

    _linha()


def menu_relatorios(banco):
    """Submenu de relatórios integrado ao menu principal."""

    while True:
        print("\n" + "=" * 44)
        print("         RELATÓRIOS")
        print("=" * 44)
        print("  1 - Resumo por usuário (AGGREGATE)")
        print("  2 - Tarefas detalhadas (LOOKUP)")
        print("  3 - Tarefas por projeto e status")
        print("  0 - Voltar ao menu principal")
        print("=" * 44)

        try:
            opcao = input("Escolha uma opção (0-3): ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if opcao == "1":
            relatorio_resumo_usuario(banco)
        elif opcao == "2":
            relatorio_tarefas_detalhadas(banco)
        elif opcao == "3":
            relatorio_tarefas_projeto_status(banco)
        elif opcao == "0":
            break
        else:
            print("\nOpção inválida. Digite um número de 0 a 3.")

        input("\nPressione Enter para continuar...")
