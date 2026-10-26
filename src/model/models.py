"""Classes de modelo para as entidades do sistema."""


class Usuario:
    """Representa um registro da tabela USUARIOS."""

    def __init__(self, id_usuario=None, nome_usuario="", email_usuario="", cargo_usuario=""):
        self.id_usuario = id_usuario
        self.nome_usuario = nome_usuario
        self.email_usuario = email_usuario
        self.cargo_usuario = cargo_usuario

    def __repr__(self):
        return (f"Usuario(id={self.id_usuario}, nome='{self.nome_usuario}', "
                f"email='{self.email_usuario}', cargo='{self.cargo_usuario}')")


class Projeto:
    """Representa um registro da tabela PROJETOS."""

    def __init__(self, id_projeto=None, nome_projeto="", descricao_projeto="",
                 data_inicio_projeto=None, data_fim_projeto=None):
        self.id_projeto = id_projeto
        self.nome_projeto = nome_projeto
        self.descricao_projeto = descricao_projeto
        self.data_inicio_projeto = data_inicio_projeto
        self.data_fim_projeto = data_fim_projeto

    def __repr__(self):
        return (f"Projeto(id={self.id_projeto}, nome='{self.nome_projeto}', "
                f"inicio='{self.data_inicio_projeto}', fim='{self.data_fim_projeto}')")


class Tarefa:
    """Representa um registro da tabela TAREFAS."""

    def __init__(self, id_tarefa=None, titulo_tarefa="", descricao_tarefa="",
                 status_tarefa="PENDENTE", prioridade_tarefa="MEDIA",
                 horas_gastas_tarefa=0.0, data_criacao_tarefa=None,
                 data_conclusao_tarefa=None, id_projeto=None, id_usuario=None):
        self.id_tarefa = id_tarefa
        self.titulo_tarefa = titulo_tarefa
        self.descricao_tarefa = descricao_tarefa
        self.status_tarefa = status_tarefa
        self.prioridade_tarefa = prioridade_tarefa
        self.horas_gastas_tarefa = horas_gastas_tarefa
        self.data_criacao_tarefa = data_criacao_tarefa
        self.data_conclusao_tarefa = data_conclusao_tarefa
        self.id_projeto = id_projeto
        self.id_usuario = id_usuario

    def __repr__(self):
        return (f"Tarefa(id={self.id_tarefa}, titulo='{self.titulo_tarefa}', "
                f"status='{self.status_tarefa}', prioridade='{self.prioridade_tarefa}')")
