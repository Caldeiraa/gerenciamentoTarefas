"""Controller — lógica de negócio, validações e operações CRUD no MongoDB (PyMongo).

Cada método recebe o objeto database (db) retornado por conectar(), executa as
validações das regras de negócio (RN01–RN08) e opera diretamente nas coleções
'usuarios', 'projetos' e 'tarefas' via PyMongo.
"""

import re
from datetime import date

from pymongo.errors import PyMongoError
from src.model.models import Usuario, Projeto, Tarefa

_STATUS_VALIDOS = ("PENDENTE", "EM_ANDAMENTO", "CONCLUIDA")
_PRIORIDADES_VALIDAS = ("BAIXA", "MEDIA", "ALTA")


def _validar_email(email):
    """RN01 — formato básico de e-mail."""
    padrao = r'^[\w\.\-]+@[\w\.\-]+\.\w+$'
    if not re.match(padrao, email):
        raise ValueError(f"E-mail '{email}' tem formato inválido.")


def _proximo_id(collection):
    """Gera o próximo _id inteiro sequencial para manter compatibilidade com o seed."""
    ultimo = collection.find_one(sort=[("_id", -1)])
    if ultimo and isinstance(ultimo.get("_id"), int):
        return ultimo["_id"] + 1
    return 1


def _registro_existe(collection, id_valor):
    """RN08 — verifica se um documento com o _id informado existe na coleção."""
    try:
        id_int = int(id_valor)
    except (ValueError, TypeError):
        return False
    return collection.count_documents({"_id": id_int}, limit=1) > 0


def _validar_data_str(texto, nome_campo):
    """Valida string no formato AAAA-MM-DD e retorna a string normalizada."""
    try:
        valor = texto.strip()
        partes = valor.split("-")
        if len(partes) != 3:
            raise ValueError
        data_obj = date(int(partes[0]), int(partes[1]), int(partes[2]))
        return data_obj.strftime("%Y-%m-%d")
    except (ValueError, IndexError, AttributeError):
        raise ValueError(f"Data '{texto}' inválida para {nome_campo}. Use o formato AAAA-MM-DD.")


def _doc_para_usuario(doc):
    return Usuario(
        id_usuario=doc.get("_id"),
        nome_usuario=doc.get("nome_usuario", ""),
        email_usuario=doc.get("email_usuario", ""),
        cargo_usuario=doc.get("cargo_usuario", ""),
    )


def _doc_para_projeto(doc):
    return Projeto(
        id_projeto=doc.get("_id"),
        nome_projeto=doc.get("nome_projeto", ""),
        descricao_projeto=doc.get("descricao_projeto", ""),
        data_inicio_projeto=doc.get("data_inicio_projeto"),
        data_fim_projeto=doc.get("data_fim_projeto"),
    )


def _doc_para_tarefa(doc):
    return Tarefa(
        id_tarefa=doc.get("_id"),
        titulo_tarefa=doc.get("titulo_tarefa", ""),
        descricao_tarefa=doc.get("descricao_tarefa", ""),
        status_tarefa=doc.get("status_tarefa", "PENDENTE"),
        prioridade_tarefa=doc.get("prioridade_tarefa", "MEDIA"),
        horas_gastas_tarefa=doc.get("horas_gastas_tarefa", 0.0),
        data_criacao_tarefa=doc.get("data_criacao_tarefa"),
        data_conclusao_tarefa=doc.get("data_conclusao_tarefa"),
        id_projeto=doc.get("id_projeto"),
        id_usuario=doc.get("id_usuario"),
    )


# ==============================================================================
#  USUÁRIOS
# ==============================================================================

def inserir_usuario(conexao, nome, email, cargo):
    """RF04 + RN01 + RN08 — insere novo usuário com insert_one."""
    if not nome or not email:
        raise ValueError("Nome e e-mail são obrigatórios.")
    _validar_email(email)

    usuarios = conexao["usuarios"]
    if usuarios.count_documents({"email_usuario": email.strip()}, limit=1) > 0:
        raise ValueError(f"Já existe um usuário cadastrado com o e-mail '{email}'.")

    try:
        novo_id = _proximo_id(usuarios)
        documento = {
            "_id": novo_id,
            "nome_usuario": nome.strip(),
            "email_usuario": email.strip(),
            "cargo_usuario": cargo.strip() if cargo else "",
        }
        usuarios.insert_one(documento)
        return _doc_para_usuario(documento)
    except PyMongoError as e:
        raise ValueError(f"Erro ao inserir usuário no MongoDB: {e}")


def listar_usuarios(conexao):
    """Retorna todos os usuários ordenados por _id."""
    usuarios = conexao["usuarios"]
    cursor = usuarios.find().sort("_id", 1)
    return [_doc_para_usuario(doc) for doc in cursor]


def buscar_usuario(conexao, id_usuario):
    """Busca um usuário pelo _id."""
    try:
        id_int = int(id_usuario)
    except (ValueError, TypeError):
        return None
    doc = conexao["usuarios"].find_one({"_id": id_int})
    return _doc_para_usuario(doc) if doc else None


def atualizar_usuario(conexao, id_usuario, nome, email, cargo):
    """RF06 + RN01 + RN08 — atualiza campos atômicos via update_one sem alterar _id."""
    try:
        id_int = int(id_usuario)
    except (ValueError, TypeError):
        raise ValueError(f"ID de usuário inválido: {id_usuario}.")

    usuarios = conexao["usuarios"]
    atual = usuarios.find_one({"_id": id_int})
    if not atual:
        raise ValueError(f"Usuário ID {id_int} não encontrado.")

    campos_atualizar = {}
    if nome is not None and nome.strip():
        campos_atualizar["nome_usuario"] = nome.strip()
    if email is not None and email.strip():
        _validar_email(email.strip())
        duplicado = usuarios.find_one({"email_usuario": email.strip(), "_id": {"$ne": id_int}})
        if duplicado:
            raise ValueError(f"Já existe outro usuário com o e-mail '{email.strip()}'.")
        campos_atualizar["email_usuario"] = email.strip()
    if cargo is not None and cargo.strip():
        campos_atualizar["cargo_usuario"] = cargo.strip()

    try:
        if campos_atualizar:
            usuarios.update_one({"_id": id_int}, {"$set": campos_atualizar})
        return buscar_usuario(conexao, id_int)
    except PyMongoError as e:
        raise ValueError(f"Erro ao atualizar usuário no MongoDB: {e}")


def excluir_usuario(conexao, id_usuario, excluir_filhos=False):
    """RF05 — verifica integridade referencial em tarefas antes de excluir usuário."""
    try:
        id_int = int(id_usuario)
    except (ValueError, TypeError):
        raise ValueError(f"ID de usuário inválido: {id_usuario}.")

    usuarios = conexao["usuarios"]
    tarefas = conexao["tarefas"]

    if not _registro_existe(usuarios, id_int):
        raise ValueError(f"Usuário ID {id_int} não encontrado.")

    qtd = tarefas.count_documents({"id_usuario": id_int})
    if qtd > 0 and not excluir_filhos:
        raise ValueError(
            f"Usuário ID {id_int} possui {qtd} tarefa(s) vinculada(s). "
            "Exclua as tarefas primeiro ou confirme a exclusão em cascata."
        )

    try:
        if qtd > 0 and excluir_filhos:
            tarefas.delete_many({"id_usuario": id_int})
        usuarios.delete_one({"_id": id_int})
        return True
    except PyMongoError as e:
        raise ValueError(f"Erro ao excluir usuário no MongoDB: {e}")


# ==============================================================================
#  PROJETOS
# ==============================================================================

def inserir_projeto(conexao, nome, descricao, data_inicio_str, data_fim_str):
    """RF04 + RN06 — insere novo projeto com insert_one."""
    if not nome or not data_inicio_str:
        raise ValueError("Nome e data de início são obrigatórios.")

    data_inicio = _validar_data_str(data_inicio_str, "data de início")
    data_fim = _validar_data_str(data_fim_str, "data de término") if data_fim_str else None

    if data_fim and data_fim < data_inicio:
        raise ValueError("RN06: Data de término não pode ser anterior à data de início.")

    projetos = conexao["projetos"]
    try:
        novo_id = _proximo_id(projetos)
        documento = {
            "_id": novo_id,
            "nome_projeto": nome.strip(),
            "descricao_projeto": descricao.strip() if descricao else "",
            "data_inicio_projeto": data_inicio,
            "data_fim_projeto": data_fim,
        }
        projetos.insert_one(documento)
        return _doc_para_projeto(documento)
    except PyMongoError as e:
        raise ValueError(f"Erro ao inserir projeto no MongoDB: {e}")


def listar_projetos(conexao):
    """Retorna todos os projetos ordenados por _id."""
    projetos = conexao["projetos"]
    cursor = projetos.find().sort("_id", 1)
    return [_doc_para_projeto(doc) for doc in cursor]


def buscar_projeto(conexao, id_projeto):
    """Busca um projeto pelo _id."""
    try:
        id_int = int(id_projeto)
    except (ValueError, TypeError):
        return None
    doc = conexao["projetos"].find_one({"_id": id_int})
    return _doc_para_projeto(doc) if doc else None


def atualizar_projeto(conexao, id_projeto, nome, descricao, data_inicio_str, data_fim_str):
    """RF06 + RN06 + RN08 — atualiza campos atômicos via update_one sem alterar _id."""
    try:
        id_int = int(id_projeto)
    except (ValueError, TypeError):
        raise ValueError(f"ID de projeto inválido: {id_projeto}.")

    projetos = conexao["projetos"]
    atual = projetos.find_one({"_id": id_int})
    if not atual:
        raise ValueError(f"Projeto ID {id_int} não encontrado.")

    data_inicio = (
        _validar_data_str(data_inicio_str, "data de início")
        if data_inicio_str and data_inicio_str.strip()
        else atual.get("data_inicio_projeto")
    )
    data_fim = (
        _validar_data_str(data_fim_str, "data de término")
        if data_fim_str and data_fim_str.strip()
        else atual.get("data_fim_projeto")
    )

    if data_inicio and data_fim and data_fim < data_inicio:
        raise ValueError("RN06: Data de término não pode ser anterior à data de início.")

    campos_atualizar = {
        "data_inicio_projeto": data_inicio,
        "data_fim_projeto": data_fim,
    }
    if nome is not None and nome.strip():
        campos_atualizar["nome_projeto"] = nome.strip()
    if descricao is not None and descricao.strip():
        campos_atualizar["descricao_projeto"] = descricao.strip()

    try:
        projetos.update_one({"_id": id_int}, {"$set": campos_atualizar})
        return buscar_projeto(conexao, id_int)
    except PyMongoError as e:
        raise ValueError(f"Erro ao atualizar projeto no MongoDB: {e}")


def excluir_projeto(conexao, id_projeto, excluir_filhos=False):
    """RF05 — verifica integridade referencial em tarefas antes de excluir projeto."""
    try:
        id_int = int(id_projeto)
    except (ValueError, TypeError):
        raise ValueError(f"ID de projeto inválido: {id_projeto}.")

    projetos = conexao["projetos"]
    tarefas = conexao["tarefas"]

    if not _registro_existe(projetos, id_int):
        raise ValueError(f"Projeto ID {id_int} não encontrado.")

    qtd = tarefas.count_documents({"id_projeto": id_int})
    if qtd > 0 and not excluir_filhos:
        raise ValueError(
            f"Projeto ID {id_int} possui {qtd} tarefa(s) vinculada(s). "
            "Exclua as tarefas primeiro ou confirme a exclusão em cascata."
        )

    try:
        if qtd > 0 and excluir_filhos:
            tarefas.delete_many({"id_projeto": id_int})
        projetos.delete_one({"_id": id_int})
        return True
    except PyMongoError as e:
        raise ValueError(f"Erro ao excluir projeto no MongoDB: {e}")


# ==============================================================================
#  TAREFAS
# ==============================================================================

def inserir_tarefa(conexao, titulo, descricao, status, prioridade,
                   horas_gastas, data_criacao_str, data_conclusao_str,
                   id_projeto, id_usuario):
    """RF04 + RN02–RN07 — insere nova tarefa com insert_one após validar FKs."""
    if not titulo or not titulo.strip():
        raise ValueError("Título da tarefa é obrigatório.")

    status_norm = status.strip().upper() if status else ""
    prioridade_norm = prioridade.strip().upper() if prioridade else ""

    if status_norm not in _STATUS_VALIDOS:
        raise ValueError(f"RN03: Status inválido. Use: {', '.join(_STATUS_VALIDOS)}.")
    if prioridade_norm not in _PRIORIDADES_VALIDAS:
        raise ValueError(f"RN04: Prioridade inválida. Use: {', '.join(_PRIORIDADES_VALIDAS)}.")

    try:
        horas = float(horas_gastas)
    except (ValueError, TypeError):
        raise ValueError("Horas gastas devem ser um número.")
    if horas < 0:
        raise ValueError("RN05: Horas gastas não podem ser negativas.")

    data_criacao = _validar_data_str(data_criacao_str, "data de criação")
    data_conclusao = (
        _validar_data_str(data_conclusao_str, "data de conclusão")
        if data_conclusao_str and data_conclusao_str.strip()
        else None
    )

    if data_conclusao and status_norm != "CONCLUIDA":
        raise ValueError("RN07: Data de conclusão só pode ser preenchida quando status = CONCLUIDA.")
    if status_norm == "CONCLUIDA" and not data_conclusao:
        raise ValueError("RN07: Tarefa CONCLUIDA deve ter data de conclusão.")

    try:
        id_proj_int = int(id_projeto)
        id_user_int = int(id_usuario)
    except (ValueError, TypeError):
        raise ValueError("RN02: IDs de projeto e usuário devem ser números inteiros.")

    if not _registro_existe(conexao["projetos"], id_proj_int):
        raise ValueError(f"RN02: Projeto ID {id_proj_int} não existe.")
    if not _registro_existe(conexao["usuarios"], id_user_int):
        raise ValueError(f"RN02: Usuário ID {id_user_int} não existe.")

    tarefas = conexao["tarefas"]
    try:
        novo_id = _proximo_id(tarefas)
        documento = {
            "_id": novo_id,
            "titulo_tarefa": titulo.strip(),
            "descricao_tarefa": descricao.strip() if descricao else "",
            "status_tarefa": status_norm,
            "prioridade_tarefa": prioridade_norm,
            "horas_gastas_tarefa": horas,
            "data_criacao_tarefa": data_criacao,
            "data_conclusao_tarefa": data_conclusao,
            "id_projeto": id_proj_int,
            "id_usuario": id_user_int,
        }
        tarefas.insert_one(documento)
        return _doc_para_tarefa(documento)
    except PyMongoError as e:
        raise ValueError(f"Erro ao inserir tarefa no MongoDB: {e}")


def listar_tarefas(conexao):
    """Retorna todas as tarefas ordenadas por _id."""
    tarefas = conexao["tarefas"]
    cursor = tarefas.find().sort("_id", 1)
    return [_doc_para_tarefa(doc) for doc in cursor]


def buscar_tarefa(conexao, id_tarefa):
    """Busca uma tarefa pelo _id."""
    try:
        id_int = int(id_tarefa)
    except (ValueError, TypeError):
        return None
    doc = conexao["tarefas"].find_one({"_id": id_int})
    return _doc_para_tarefa(doc) if doc else None


def atualizar_tarefa(conexao, id_tarefa, titulo, descricao, status, prioridade,
                     horas_gastas, data_criacao_str, data_conclusao_str,
                     id_projeto, id_usuario):
    """RF06 + RN02–RN08 — atualiza campos atômicos via update_one sem alterar _id."""
    try:
        id_int = int(id_tarefa)
    except (ValueError, TypeError):
        raise ValueError(f"ID de tarefa inválido: {id_tarefa}.")

    tarefas = conexao["tarefas"]
    atual = tarefas.find_one({"_id": id_int})
    if not atual:
        raise ValueError(f"Tarefa ID {id_int} não encontrada.")

    status_norm = status.strip().upper() if status and status.strip() else atual.get("status_tarefa")
    prioridade_norm = prioridade.strip().upper() if prioridade and prioridade.strip() else atual.get("prioridade_tarefa")

    if status_norm not in _STATUS_VALIDOS:
        raise ValueError(f"RN03: Status inválido. Use: {', '.join(_STATUS_VALIDOS)}.")
    if prioridade_norm not in _PRIORIDADES_VALIDAS:
        raise ValueError(f"RN04: Prioridade inválida. Use: {', '.join(_PRIORIDADES_VALIDAS)}.")

    try:
        horas = float(horas_gastas) if horas_gastas is not None and str(horas_gastas).strip() != "" else float(atual.get("horas_gastas_tarefa", 0.0))
    except (ValueError, TypeError):
        raise ValueError("Horas gastas devem ser um número.")
    if horas < 0:
        raise ValueError("RN05: Horas gastas não podem ser negativas.")

    data_criacao = (
        _validar_data_str(data_criacao_str, "data de criação")
        if data_criacao_str and data_criacao_str.strip()
        else atual.get("data_criacao_tarefa")
    )
    data_conclusao = (
        _validar_data_str(data_conclusao_str, "data de conclusão")
        if data_conclusao_str and data_conclusao_str.strip()
        else atual.get("data_conclusao_tarefa")
    )

    if data_conclusao and status_norm != "CONCLUIDA":
        raise ValueError("RN07: Data de conclusão só permitida para status CONCLUIDA.")
    if status_norm == "CONCLUIDA" and not data_conclusao:
        raise ValueError("RN07: Tarefa CONCLUIDA deve ter data de conclusão.")

    try:
        id_proj_int = int(id_projeto) if id_projeto is not None and str(id_projeto).strip() != "" else atual.get("id_projeto")
        id_user_int = int(id_usuario) if id_usuario is not None and str(id_usuario).strip() != "" else atual.get("id_usuario")
    except (ValueError, TypeError):
        raise ValueError("RN02: IDs de projeto e usuário devem ser números inteiros.")

    if not _registro_existe(conexao["projetos"], id_proj_int):
        raise ValueError(f"RN02: Projeto ID {id_proj_int} não existe.")
    if not _registro_existe(conexao["usuarios"], id_user_int):
        raise ValueError(f"RN02: Usuário ID {id_user_int} não existe.")

    campos_atualizar = {
        "status_tarefa": status_norm,
        "prioridade_tarefa": prioridade_norm,
        "horas_gastas_tarefa": horas,
        "data_criacao_tarefa": data_criacao,
        "data_conclusao_tarefa": data_conclusao,
        "id_projeto": id_proj_int,
        "id_usuario": id_user_int,
    }
    if titulo is not None and titulo.strip():
        campos_atualizar["titulo_tarefa"] = titulo.strip()
    if descricao is not None and descricao.strip():
        campos_atualizar["descricao_tarefa"] = descricao.strip()

    try:
        tarefas.update_one({"_id": id_int}, {"$set": campos_atualizar})
        return buscar_tarefa(conexao, id_int)
    except PyMongoError as e:
        raise ValueError(f"Erro ao atualizar tarefa no MongoDB: {e}")


def excluir_tarefa(conexao, id_tarefa):
    """RF05 — exclui uma tarefa pelo _id via delete_one."""
    try:
        id_int = int(id_tarefa)
    except (ValueError, TypeError):
        raise ValueError(f"ID de tarefa inválido: {id_tarefa}.")

    tarefas = conexao["tarefas"]
    if not _registro_existe(tarefas, id_int):
        raise ValueError(f"Tarefa ID {id_int} não encontrada.")

    try:
        tarefas.delete_one({"_id": id_int})
        return True
    except PyMongoError as e:
        raise ValueError(f"Erro ao excluir tarefa no MongoDB: {e}")