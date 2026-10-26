import sqlite3
import re

class Cliente:
    def __init__(self, id_cliente, nome, email):
        self.id_cliente = id_cliente
        self.nome = nome
        self.email = email

    def __repr__(self):
        return f"Cliente(id={self.id_cliente}, nome='{self.nome}', email='{self.email}')"

class ClienteController:
    def __init__(self, db_name="sistema_crud.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._criar_tabela()

    def _criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')
        self.conn.commit()

    def _validar_email(self, email):
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(padrao, email):
            raise ValueError(f"Erro: O e-mail '{email}' tem um formato inválido.")

    def criar_cliente(self, id_cliente, nome, email):
        if not id_cliente or not nome or not email:
            raise ValueError("Erro: Todos os campos são obrigatórios.")
        self._validar_email(email)
        try:
            self.cursor.execute('''
                INSERT INTO clientes (id_cliente, nome, email)
                VALUES (?, ?, ?)
            ''', (id_cliente, nome, email))
            self.conn.commit()
            print(f"Sucesso: {nome} cadastrado(a) na base de dados!")
            return Cliente(id_cliente, nome, email)
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Erro de validação: ID ou E-mail já existem no sistema.")

    def listar_clientes(self):
        self.cursor.execute('SELECT * FROM clientes')
        linhas = self.cursor.fetchall()
        return [Cliente(linha[0], linha[1], linha[2]) for linha in linhas]

    def buscar_cliente(self, id_cliente):
        self.cursor.execute('SELECT * FROM clientes WHERE id_cliente = ?', (id_cliente,))
        linha = self.cursor.fetchone()
        if linha:
            return Cliente(linha[0], linha[1], linha[2])
        return None

    def atualizar_cliente(self, id_cliente, novo_nome=None, novo_email=None):
        cliente_atual = self.buscar_cliente(id_cliente)
        if not cliente_atual:
            raise ValueError(f"Erro: Cliente com ID {id_cliente} não encontrado.")
        nome_final = novo_nome if novo_nome else cliente_atual.nome
        email_final = novo_email if novo_email else cliente_atual.email
        if novo_email:
            self._validar_email(novo_email)
        try:
            self.cursor.execute('''
                UPDATE clientes 
                SET nome = ?, email = ?
                WHERE id_cliente = ?
            ''', (nome_final, email_final, id_cliente))
            self.conn.commit()
            print(f"Sucesso: Registro {id_cliente} atualizado.")
            return Cliente(id_cliente, nome_final, email_final)
        except sqlite3.IntegrityError:
            raise ValueError("Erro: O novo e-mail fornecido já está em uso por outro cliente.")

    def excluir_cliente(self, id_cliente):
        if not self.buscar_cliente(id_cliente):
            raise ValueError(f"Erro: Não é possível excluir. O ID {id_cliente} não existe.")
        self.cursor.execute('DELETE FROM clientes WHERE id_cliente = ?', (id_cliente,))
        self.conn.commit()
        print(f"Sucesso: Registro {id_cliente} excluído da base de dados permanentemente.")
        return True

if __name__ == "__main__":
    controller = ClienteController()
    
    while True:
        print("\n" + "="*40)
        print("          SISTEMA CRUD CLIENTES")
        print("="*40)
        print("1 - Cadastrar novo cliente")
        print("2 - Listar todos os clientes")
        print("3 - Atualizar um cliente")
        print("4 - Excluir um cliente")
        print("0 - Sair do sistema")
        print("="*40)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            print("\n--- CADASTRAR CLIENTE ---")
            try:
                id_cliente = int(input("Digite o ID (número): "))
                nome = input("Digite o Nome: ")
                email = input("Digite o E-mail: ")
                controller.criar_cliente(id_cliente, nome, email)
            except ValueError as e:
                # Trata erros caso o usuário digite texto no lugar de número no ID
                print(f"Erro de validação: {e}")
                
        elif opcao == '2':
            print("\n--- LISTA DE CLIENTES ---")
            clientes = controller.listar_clientes()
            if not clientes:
                print("Nenhum cliente cadastrado no banco de dados.")
            else:
                for c in clientes:
                    print(f"ID: {c.id_cliente} | Nome: {c.nome} | E-mail: {c.email}")
            
            # Adicione esta linha para pausar o ecrã!
            input("\nPressione Enter para voltar ao menu...")
                    
        elif opcao == '3':
            print("\n--- ATUALIZAR CLIENTE ---")
            try:
                id_cliente = int(input("Digite o ID do cliente que deseja atualizar: "))
                print("(Deixe em branco e aperte Enter se não quiser alterar o campo)")
                
                novo_nome = input("Novo Nome: ")
                novo_email = input("Novo E-mail: ")
                
                # Prepara os dados (se estiver vazio, envia None para não alterar)
                nome_final = novo_nome if novo_nome.strip() != "" else None
                email_final = novo_email if novo_email.strip() != "" else None
                
                # Faz a atualização e guarda o retorno para mostrar na tela
                cliente_atualizado = controller.atualizar_cliente(id_cliente, nome_final, email_final)
                
                print("\n>>> RESULTADO DA ATUALIZAÇÃO <<<")
                print(f"ID: {cliente_atualizado.id_cliente} | Nome: {cliente_atualizado.nome} | E-mail: {cliente_atualizado.email}")
            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == '4':
            print("\n--- EXCLUIR CLIENTE ---")
            try:
                id_cliente = int(input("Digite o ID do cliente que deseja excluir: "))
                confirmacao = input(f"Tem certeza que deseja excluir o ID {id_cliente}? (S/N): ").upper()
                if confirmacao == 'S':
                    controller.excluir_cliente(id_cliente)
                else:
                    print("Operação de exclusão cancelada.")
            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == '0':
            print("\nSaindo do sistema... Até logo!")
            break
            
        else:
            print("\nOpção inválida! Digite um número de 0 a 4.")