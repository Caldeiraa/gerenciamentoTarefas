"""Classes de modelo para as entidades do sistema."""


class Usuario:
    """Representa um documento da coleção usuarios."""

    def __init__(self, id_usuario=None, nome_usuario="", email_usuario="", cargo_usuario=""):
        self.id_usuario = id_usuario
        self.nome_usuario = nome_usuario
        self.email_usuario = email_usuario
        self.cargo_usuario = cargo_usuario

    def get_id_usuario(self):
        return self.id_usuario

    def get_nome_usuario(self):
        return self.nome_usuario

    def get_email_usuario(self):
        return self.email_usuario

    def get_cargo_usuario(self):
        return self.cargo_usuario

    def set_id_usuario(self, id_usuario):
        self.id_usuario = id_usuario

    def set_nome_usuario(self, nome_usuario):
        self.nome_usuario = nome_usuario

    def set_email_usuario(self, email_usuario):
        self.email_usuario = email_usuario

    def set_cargo_usuario(self, cargo_usuario):
        self.cargo_usuario = cargo_usuario

    def to_string(self):
        return (f"ID: {self.id_usuario} | Nome: {self.nome_usuario} | "
                f"E-mail: {self.email_usuario} | Cargo: {self.cargo_usuario}")

    def __repr__(self):
        return (f"Usuario(id={self.id_usuario}, nome='{self.nome_usuario}', "
                f"email='{self.email_usuario}', cargo='{self.cargo_usuario}')")


class Projeto:
    """Representa um documento da coleção projetos."""

    def __init__(self, id_projeto=None, nome_projeto="", descricao_projeto="",
                 data_inicio_projeto=None, data_fim_projeto=None):
        self.id_projeto = id_projeto
        self.nome_projeto = nome_projeto
        self.descricao_projeto = descricao_projeto
        self.data_inicio_projeto = data_inicio_projeto
        self.data_fim_projeto = data_fim_projeto

    def get_id_projeto(self):
        return self.id_projeto

    def get_nome_projeto(self):
        return self.nome_projeto

    def get_descricao_projeto(self):
        return self.descricao_projeto

    def get_data_inicio_projeto(self):
        return self.data_inicio_projeto

    def get_data_fim_projeto(self):
        return self.data_fim_projeto

    def set_id_projeto(self, id_projeto):
        self.id_projeto = id_projeto

    def set_nome_projeto(self, nome_projeto):
        self.nome_projeto = nome_projeto

    def set_descricao_projeto(self, descricao_projeto):
        self.descricao_projeto = descricao_projeto

    def set_data_inicio_projeto(self, data_inicio_projeto):
        self.data_inicio_projeto = data_inicio_projeto

    def set_data_fim_projeto(self, data_fim_projeto):
        self.data_fim_projeto = data_fim_projeto

    def to_string(self):
        return (f"ID: {self.id_projeto} | Projeto: {self.nome_projeto} | "
                f"Descrição: {self.descricao_projeto} | "
                f"Início: {self.data_inicio_projeto} | Fim: {self.data_fim_projeto}")

    def __repr__(self):
        return (f"Projeto(id={self.id_projeto}, nome='{self.nome_projeto}', "
                f"inicio='{self.data_inicio_projeto}', fim='{self.data_fim_projeto}')")


class Tarefa:
    """Representa um documento da coleção tarefas."""

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

    def get_id_tarefa(self):
        return self.id_tarefa

    def get_titulo_tarefa(self):
        return self.titulo_tarefa

    def get_descricao_tarefa(self):
        return self.descricao_tarefa

    def get_status_tarefa(self):
        return self.status_tarefa

    def get_prioridade_tarefa(self):
        return self.prioridade_tarefa

    def get_horas_gastas_tarefa(self):
        return self.horas_gastas_tarefa

    def get_data_criacao_tarefa(self):
        return self.data_criacao_tarefa

    def get_data_conclusao_tarefa(self):
        return self.data_conclusao_tarefa

    def get_id_projeto(self):
        return self.id_projeto

    def get_id_usuario(self):
        return self.id_usuario

    def set_id_tarefa(self, id_tarefa):
        self.id_tarefa = id_tarefa

    def set_titulo_tarefa(self, titulo_tarefa):
        self.titulo_tarefa = titulo_tarefa

    def set_descricao_tarefa(self, descricao_tarefa):
        self.descricao_tarefa = descricao_tarefa

    def set_status_tarefa(self, status_tarefa):
        self.status_tarefa = status_tarefa

    def set_prioridade_tarefa(self, prioridade_tarefa):
        self.prioridade_tarefa = prioridade_tarefa

    def set_horas_gastas_tarefa(self, horas_gastas_tarefa):
        self.horas_gastas_tarefa = horas_gastas_tarefa

    def set_data_criacao_tarefa(self, data_criacao_tarefa):
        self.data_criacao_tarefa = data_criacao_tarefa

    def set_data_conclusao_tarefa(self, data_conclusao_tarefa):
        self.data_conclusao_tarefa = data_conclusao_tarefa

    def set_id_projeto(self, id_projeto):
        self.id_projeto = id_projeto

    def set_id_usuario(self, id_usuario):
        self.id_usuario = id_usuario

    def to_string(self):
        return (f"ID: {self.id_tarefa} | Título: {self.titulo_tarefa} | "
                f"Status: {self.status_tarefa} | Prioridade: {self.prioridade_tarefa} | "
                f"Horas: {self.horas_gastas_tarefa}h | Criação: {self.data_criacao_tarefa} | "
                f"Conclusão: {self.data_conclusao_tarefa} | "
                f"Projeto ID: {self.id_projeto} | Usuário ID: {self.id_usuario}")

    def __repr__(self):
        return (f"Tarefa(id={self.id_tarefa}, titulo='{self.titulo_tarefa}', "
                f"status='{self.status_tarefa}', prioridade='{self.prioridade_tarefa}')")