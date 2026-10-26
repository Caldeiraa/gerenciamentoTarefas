"""Controller — lógica de negócio e validações para cada entidade.

Cada método recebe a conexão, executa as validações das regras de negócio
(RN01–RN08) e delega a construção do SQL ao módulo src.sql.queries.
"""

import re
from datetime import date

from src.sql import queries
from src.model.models import Usuario, Projeto, Tarefa


# ═══════════════════════════════════════════════════════════════════
#  Helpers internos
# ═══════════════════════════════════════════════════════════════════

_STATUS_VALIDOS = ("PENDENTE", "EM_ANDAMENTO", "CONCLUIDA")
_PRIORIDADES_VALIDAS = ("BAIXA", "MEDIA", "ALTA")


def _validar_email(email):
    """RN01 — formato básico de e-mail."""
    padrao = r'^[\w\.\-]+@[\w\.\-]+\.\w+$'
    if not re.match(padrao, email):
        raise ValueError(f"E-mail '{email}' tem formato inválido.")


def _registro_existe(cursor, sql_fn, id_valor):
    """RN08 — verifica se um registro existe no banco."""
    sql, params = sql_fn(id_valor)
    cursor.execute(sql, params)
    return cursor.fetchone()[0] > 0


def _parse_data(texto, nome_campo):
    """Converte string AAAA-MM-DD em date, com mensagem amigável."""
    try:
        partes = texto.strip().split("-")
        return date(int(partes[0]), int(partes[1]), int(partes[2]))
    except (ValueError, IndexError):
        raise ValueError(f"Data '{texto}' inválida para {nome_campo}. Use o formato AAAA-MM-DD.")


# ═══════════════════════════════════════════════════════════════════
#  USUÁRIOS
# ═══════════════════════════════════════════════════════════════════

def inserir_usuario(conexao, nome, email, cargo):
    """RF04 + RN01 + RN08."""
    if not nome or not email:
        raise ValueError("Nome e e-mail são obrigatórios.")
    _validar_email(email)
    cursor = conexao.cursor()
    try:
        sql, params = queries.sql_inserir_usuario(nome, email, cargo)
        cursor.execute(sql, params)
        conexao.commit()
        return Usuario(cursor.lastrowid, nome, email, cargo)
    except Exception as e:
        conexao.rollback()
        raise ValueError(f"Erro ao inserir usuário: {e}")
    finally:
        cursor.close()


def listar_usuarios(conexao):
    cursor = conexao.cursor()
    try:
        sql, params = queries.sql_listar_usuarios()
        cursor.execute(sql, params)
        return [Usuario(*row) for row in cursor.fetchall()]
    finally:
        cursor.close()


def buscar_usuario(conexao, id_usuario):
    cursor = conexao.cursor()
    try:
        sql, params = queries.sql_buscar_usuario(id_usuario)
        cursor.execute(sql, params)
        row = cursor.fetchone()
        return Usuario(*row) if row else None
    finally:
        cursor.close()


def atualizar_usuario(conexao, id_usuario, nome, email, cargo):
    """RF06 + RN01 + RN08."""
    cursor = conexao.cursor()
    try:
        if not _registro_existe(cursor, queries.sql_usuario_existe, id_usuario):
            raise ValueError(f"Usuário ID {id_usuario} não encontrado.")
        if email:
            _validar_email(email)
        sql, params = queries.sql_atualizar_usuario(id_usuario, nome, email, cargo)
        cursor.execute(sql, params)
        conexao.commit()
        return buscar_usuario(conexao, id_usuario)
    except ValueError:
        conexao.rollback()
        raise
    except Exception as e:
        conexao.rollback()
        raise ValueError(f"Erro ao atualizar usuário: {e}")
    finally:
        cursor.close()


def excluir_usuario(conexao, id_usuario, excluir_filhos=False):
    """RF05 — verifica se há tarefas vinculadas antes de excluir."""
    cursor = conexao.cursor()
    try:
        if not _registro_existe(cursor, queries.sql_usuario_existe, id_usuario):
            raise ValueError(f"Usuário ID {id_usuario} não encontrado.")

        sql_count, p = queries.sql_usuario_possui_tarefas(id_usuario)
        cursor.execute(sql_count, p)
        qtd = cursor.fetchone()[0]

        if qtd > 0 and not excluir_filhos:
            raise ValueError(
                f"Usuário ID {id_usuario} possui {qtd} tarefa(s) vinculada(s). "
                "Exclua as tarefas primeiro ou confirme a exclusão em cascata."
            )
        if qtd > 0 and excluir_filhos:
            sql_del, p2 = queries.sql_excluir_tarefas_usuario(id_usuario)
            cursor.execute(sql_del, p2)

        sql, params = queries.sql_excluir_usuario(id_usuario)
        cursor.execute(sql, params)
        conexao.commit()
        return True
    except ValueError:
        conexao.rollback()
        raise
    except Exception as e:
        conexao.rollback()
        raise ValueError(f"Erro ao excluir usuário: {e}")
    finally:
        cursor.close()


# ═══════════════════════════════════════════════════════════════════
#  PROJETOS
# ═══════════════════════════════════════════════════════════════════

def inserir_projeto(conexao, nome, descricao, data_inicio_str, data_fim_str):
    """RF04 + RN06."""
    if not nome or not data_inicio_str:
        raise ValueError("Nome e data de início são obrigatórios.")
    data_inicio = _parse_data(data_inicio_str, "data de início")
    data_fim = _parse_data(data_fim_str, "data de término") if data_fim_str else None
    if data_fim and data_fim < data_inicio:
        raise ValueError("RN06: Data de término não pode ser anterior à data de início.")
    cursor = conexao.cursor()
    try:
        sql, params = queries.sql_inserir_projeto(nome, descricao, data_inicio, data_fim)
        cursor.execute(sql, params)
        conexao.commit()
        return Projeto(cursor.lastrowid, nome, descricao, data_inicio, data_fim)
    except Exception as e:
        conexao.rollback()
        raise ValueError(f"Erro ao inserir projeto: {e}")
    finally:
        cursor.close()


def listar_projetos(conexao):
    cursor = conexao.cursor()
    try:
        sql, params = queries.sql_listar_projetos()
        cursor.execute(sql, params)
        return [Projeto(*row) for row in cursor.fetchall()]
    finally:
        cursor.close()


def buscar_projeto(conexao, id_projeto):
    cursor = conexao.cursor()
    try:
        sql, params = queries.sql_buscar_projeto(id_projeto)
        cursor.execute(sql, params)
        row = cursor.fetchone()
        return Projeto(*row) if row else None
    finally:
        cursor.close()


def atualizar_projeto(conexao, id_projeto, nome, descricao, data_inicio_str, data_fim_str):
    """RF06 + RN06 + RN08."""
    cursor = conexao.cursor()
    try:
        if not _registro_existe(cursor, queries.sql_projeto_existe, id_projeto):
            raise ValueError(f"Projeto ID {id_projeto} não encontrado.")
        data_inicio = _parse_data(data_inicio_str, "data de início") if data_inicio_str else None
        data_fim = _parse_data(data_fim_str, "data de término") if data_fim_str else None
        if data_inicio and data_fim and data_fim < data_inicio:
            raise ValueError("RN06: Data de término não pode ser anterior à data de início.")
        sql, params = queries.sql_atualizar_projeto(id_projeto, nome, descricao, data_inicio, data_fim)
        cursor.execute(sql, params)
        conexao.commit()
        return buscar_projeto(conexao, id_projeto)
    except ValueError:
        conexao.rollback()
        raise
    except Exception as e:
        conexao.rollback()
        raise ValueError(f"Erro ao atualizar projeto: {e}")
    finally:
        cursor.close()


def excluir_projeto(conexao, id_projeto, excluir_filhos=False):
    """RF05 — verifica tarefas vinculadas antes de excluir."""
    cursor = conexao.cursor()
    try:
        if not _registro_existe(cursor, queries.sql_projeto_existe, id_projeto):
            raise ValueError(f"Projeto ID {id_projeto} não encontrado.")

        sql_count, p = queries.sql_projeto_possui_tarefas(id_projeto)
        cursor.execute(sql_count, p)
        qtd = cursor.fetchone()[0]

        if qtd > 0 and not excluir_filhos:
            raise ValueError(
                f"Projeto ID {id_projeto} possui {qtd} tarefa(s) vinculada(s). "
                "Exclua as tarefas primeiro ou confirme a exclusão em cascata."
            )
        if qtd > 0 and excluir_filhos:
            sql_del, p2 = queries.sql_excluir_tarefas_projeto(id_projeto)
            cursor.execute(sql_del, p2)

        sql, params = queries.sql_excluir_projeto(id_projeto)
        cursor.execute(sql, params)
        conexao.commit()
        return True
    except ValueError:
        conexao.rollback()
        raise
    except Exception as e:
        conexao.rollback()
        raise ValueError(f"Erro ao excluir projeto: {e}")
    finally:
        cursor.close()


# ═══════════════════════════════════════════════════════════════════
#  TAREFAS
# ═══════════════════════════════════════════════════════════════════

def inserir_tarefa(conexao, titulo, descricao, status, prioridade,
                   horas_gastas, data_criacao_str, data_conclusao_str,
                   id_projeto, id_usuario):
    """RF04 + RN02–RN07."""
    if not titulo:
        raise ValueError("Título da tarefa é obrigatório.")
    if status not in _STATUS_VALIDOS:
        raise ValueError(f"RN03: Status inválido. Use: {', '.join(_STATUS_VALIDOS)}.")
    if prioridade not in _PRIORIDADES_VALIDAS:
        raise ValueError(f"RN04: Prioridade inválida. Use: {', '.join(_PRIORIDADES_VALIDAS)}.")
    try:
        horas = float(horas_gastas)
    except (ValueError, TypeError):
        raise ValueError("Horas gastas devem ser um número.")
    if horas < 0:
        raise ValueError("RN05: Horas gastas não podem ser negativas.")

    data_criacao = _parse_data(data_criacao_str, "data de criação")
    data_conclusao = _parse_data(data_conclusao_str, "data de conclusão") if data_conclusao_str else None

    if data_conclusao and status != "CONCLUIDA":
        raise ValueError("RN07: Data de conclusão só pode ser preenchida quando status = CONCLUIDA.")
    if status == "CONCLUIDA" and not data_conclusao:
        raise ValueError("RN07: Tarefa CONCLUIDA deve ter data de conclusão.")

    cursor = conexao.cursor()
    try:
        # RN02 — verifica FK
        if not _registro_existe(cursor, queries.sql_projeto_existe, id_projeto):
            raise ValueError(f"RN02: Projeto ID {id_projeto} não existe.")
        if not _registro_existe(cursor, queries.sql_usuario_existe, id_usuario):
            raise ValueError(f"RN02: Usuário ID {id_usuario} não existe.")

        sql, params = queries.sql_inserir_tarefa(
            titulo, descricao, status, prioridade, horas,
            data_criacao, data_conclusao, id_projeto, id_usuario
        )
        cursor.execute(sql, params)
        conexao.commit()
        return Tarefa(cursor.lastrowid, titulo, descricao, status, prioridade,
                      horas, data_criacao, data_conclusao, id_projeto, id_usuario)
    except ValueError:
        conexao.rollback()
        raise
    except Exception as e:
        conexao.rollback()
        raise ValueError(f"Erro ao inserir tarefa: {e}")
    finally:
        cursor.close()


def listar_tarefas(conexao):
    cursor = conexao.cursor()
    try:
        sql, params = queries.sql_listar_tarefas()
        cursor.execute(sql, params)
        return [Tarefa(*row) for row in cursor.fetchall()]
    finally:
        cursor.close()


def buscar_tarefa(conexao, id_tarefa):
    cursor = conexao.cursor()
    try:
        sql, params = queries.sql_buscar_tarefa(id_tarefa)
        cursor.execute(sql, params)
        row = cursor.fetchone()
        return Tarefa(*row) if row else None
    finally:
        cursor.close()


def atualizar_tarefa(conexao, id_tarefa, titulo, descricao, status, prioridade,
                     horas_gastas, data_criacao_str, data_conclusao_str,
                     id_projeto, id_usuario):
    """RF06 + RN02–RN08."""
    cursor = conexao.cursor()
    try:
        if not _registro_existe(cursor, queries.sql_tarefa_existe, id_tarefa):
            raise ValueError(f"Tarefa ID {id_tarefa} não encontrada.")
        if status not in _STATUS_VALIDOS:
            raise ValueError(f"RN03: Status inválido. Use: {', '.join(_STATUS_VALIDOS)}.")
        if prioridade not in _PRIORIDADES_VALIDAS:
            raise ValueError(f"RN04: Prioridade inválida. Use: {', '.join(_PRIORIDADES_VALIDAS)}.")
        try:
            horas = float(horas_gastas)
        except (ValueError, TypeError):
            raise ValueError("Horas gastas devem ser um número.")
        if horas < 0:
            raise ValueError("RN05: Horas gastas não podem ser negativas.")

        data_criacao = _parse_data(data_criacao_str, "data de criação") if data_criacao_str else None
        data_conclusao = _parse_data(data_conclusao_str, "data de conclusão") if data_conclusao_str else None

        if data_conclusao and status != "CONCLUIDA":
            raise ValueError("RN07: Data de conclusão só permitida para status CONCLUIDA.")

        if not _registro_existe(cursor, queries.sql_projeto_existe, id_projeto):
            raise ValueError(f"RN02: Projeto ID {id_projeto} não existe.")
        if not _registro_existe(cursor, queries.sql_usuario_existe, id_usuario):
            raise ValueError(f"RN02: Usuário ID {id_usuario} não existe.")

        sql, params = queries.sql_atualizar_tarefa(
            id_tarefa, titulo, descricao, status, prioridade, horas,
            data_criacao, data_conclusao, id_projeto, id_usuario
        )
        cursor.execute(sql, params)
        conexao.commit()
        return buscar_tarefa(conexao, id_tarefa)
    except ValueError:
        conexao.rollback()
        raise
    except Exception as e:
        conexao.rollback()
        raise ValueError(f"Erro ao atualizar tarefa: {e}")
    finally:
        cursor.close()


def excluir_tarefa(conexao, id_tarefa):
    """RF05."""
    cursor = conexao.cursor()
    try:
        if not _registro_existe(cursor, queries.sql_tarefa_existe, id_tarefa):
            raise ValueError(f"Tarefa ID {id_tarefa} não encontrada.")
        sql, params = queries.sql_excluir_tarefa(id_tarefa)
        cursor.execute(sql, params)
        conexao.commit()
        return True
    except ValueError:
        conexao.rollback()
        raise
    except Exception as e:
        conexao.rollback()
        raise ValueError(f"Erro ao excluir tarefa: {e}")
    finally:
        cursor.close()
