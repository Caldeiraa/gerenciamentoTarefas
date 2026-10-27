"""Módulo SQL — consultas montadas por concatenação de texto (sem ORM).

Cada função retorna uma tupla (sql_string, parametros) pronta para
cursor.execute(sql, parametros).
O edital exige SQL por concatenação; os parâmetros são passados via
placeholders %s do mysql-connector para evitar SQL Injection.
"""

#  USUÁRIOS

def sql_inserir_usuario(nome, email, cargo):
    sql = ("INSERT INTO usuarios (nome_usuario, email_usuario, cargo_usuario) "
           "VALUES (%s, %s, %s)")
    return sql, (nome, email, cargo)


def sql_listar_usuarios():
    sql = "SELECT id_usuario, nome_usuario, email_usuario, cargo_usuario FROM usuarios ORDER BY id_usuario"
    return sql, ()


def sql_buscar_usuario(id_usuario):
    sql = "SELECT id_usuario, nome_usuario, email_usuario, cargo_usuario FROM usuarios WHERE id_usuario = %s"
    return sql, (id_usuario,)


def sql_atualizar_usuario(id_usuario, nome, email, cargo):
    sql = ("UPDATE usuarios SET nome_usuario = %s, email_usuario = %s, cargo_usuario = %s "
           "WHERE id_usuario = %s")
    return sql, (nome, email, cargo, id_usuario)


def sql_excluir_usuario(id_usuario):
    sql = "DELETE FROM usuarios WHERE id_usuario = %s"
    return sql, (id_usuario,)


def sql_usuario_possui_tarefas(id_usuario):
    sql = "SELECT COUNT(1) FROM tarefas WHERE id_usuario = %s"
    return sql, (id_usuario,)


def sql_excluir_tarefas_usuario(id_usuario):
    sql = "DELETE FROM tarefas WHERE id_usuario = %s"
    return sql, (id_usuario,)


def sql_usuario_existe(id_usuario):
    sql = "SELECT COUNT(1) FROM usuarios WHERE id_usuario = %s"
    return sql, (id_usuario,)


#  PROJETOS

def sql_inserir_projeto(nome, descricao, data_inicio, data_fim):
    sql = ("INSERT INTO projetos (nome_projeto, descricao_projeto, "
           "data_inicio_projeto, data_fim_projeto) VALUES (%s, %s, %s, %s)")
    return sql, (nome, descricao, data_inicio, data_fim)


def sql_listar_projetos():
    sql = ("SELECT id_projeto, nome_projeto, descricao_projeto, "
           "data_inicio_projeto, data_fim_projeto FROM projetos ORDER BY id_projeto")
    return sql, ()


def sql_buscar_projeto(id_projeto):
    sql = ("SELECT id_projeto, nome_projeto, descricao_projeto, "
           "data_inicio_projeto, data_fim_projeto FROM projetos WHERE id_projeto = %s")
    return sql, (id_projeto,)


def sql_atualizar_projeto(id_projeto, nome, descricao, data_inicio, data_fim):
    sql = ("UPDATE projetos SET nome_projeto = %s, descricao_projeto = %s, "
           "data_inicio_projeto = %s, data_fim_projeto = %s WHERE id_projeto = %s")
    return sql, (nome, descricao, data_inicio, data_fim, id_projeto)


def sql_excluir_projeto(id_projeto):
    sql = "DELETE FROM projetos WHERE id_projeto = %s"
    return sql, (id_projeto,)


def sql_projeto_possui_tarefas(id_projeto):
    sql = "SELECT COUNT(1) FROM tarefas WHERE id_projeto = %s"
    return sql, (id_projeto,)


def sql_excluir_tarefas_projeto(id_projeto):
    sql = "DELETE FROM tarefas WHERE id_projeto = %s"
    return sql, (id_projeto,)


def sql_projeto_existe(id_projeto):
    sql = "SELECT COUNT(1) FROM projetos WHERE id_projeto = %s"
    return sql, (id_projeto,)


#  TAREFAS

def sql_inserir_tarefa(titulo, descricao, status, prioridade,
                       horas_gastas, data_criacao, data_conclusao,
                       id_projeto, id_usuario):
    sql = ("INSERT INTO tarefas (titulo_tarefa, descricao_tarefa, status_tarefa, "
           "prioridade_tarefa, horas_gastas_tarefa, data_criacao_tarefa, "
           "data_conclusao_tarefa, id_projeto, id_usuario) "
           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
    return sql, (titulo, descricao, status, prioridade, horas_gastas,
                 data_criacao, data_conclusao, id_projeto, id_usuario)


def sql_listar_tarefas():
    sql = ("SELECT id_tarefa, titulo_tarefa, descricao_tarefa, status_tarefa, "
           "prioridade_tarefa, horas_gastas_tarefa, data_criacao_tarefa, "
           "data_conclusao_tarefa, id_projeto, id_usuario "
           "FROM tarefas ORDER BY id_tarefa")
    return sql, ()


def sql_buscar_tarefa(id_tarefa):
    sql = ("SELECT id_tarefa, titulo_tarefa, descricao_tarefa, status_tarefa, "
           "prioridade_tarefa, horas_gastas_tarefa, data_criacao_tarefa, "
           "data_conclusao_tarefa, id_projeto, id_usuario "
           "FROM tarefas WHERE id_tarefa = %s")
    return sql, (id_tarefa,)


def sql_atualizar_tarefa(id_tarefa, titulo, descricao, status, prioridade,
                         horas_gastas, data_criacao, data_conclusao,
                         id_projeto, id_usuario):
    sql = ("UPDATE tarefas SET titulo_tarefa = %s, descricao_tarefa = %s, "
           "status_tarefa = %s, prioridade_tarefa = %s, "
           "horas_gastas_tarefa = %s, data_criacao_tarefa = %s, "
           "data_conclusao_tarefa = %s, id_projeto = %s, id_usuario = %s "
           "WHERE id_tarefa = %s")
    return sql, (titulo, descricao, status, prioridade, horas_gastas,
                 data_criacao, data_conclusao, id_projeto, id_usuario, id_tarefa)


def sql_excluir_tarefa(id_tarefa):
    sql = "DELETE FROM tarefas WHERE id_tarefa = %s"
    return sql, (id_tarefa,)


def sql_tarefa_existe(id_tarefa):
    sql = "SELECT COUNT(1) FROM tarefas WHERE id_tarefa = %s"
    return sql, (id_tarefa,)


#  CONTAGEM

def sql_contar_tabela(nome_tabela):
    """Retorna SQL de contagem. O nome da tabela é embutido na string
    (nunca vem do usuário — apenas de TABELAS em config.py)."""
    sql = "SELECT COUNT(1) AS total_" + nome_tabela + " FROM " + nome_tabela
    return sql, ()
