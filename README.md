# Sistema CRUD de Clientes

Sistema de registo e gestão de clientes com persistência de dados em SQLite e menu interativo no terminal. Este projeto foi desenvolvido para consolidar conceitos de classes, modelagem de dados e validações no curso de Análise e Desenvolvimento de Sistemas (FAESA).

##  Funcionalidades

O sistema segue a arquitetura de Modelo e Controladora, oferecendo as seguintes operações:

*   **Create (Inserção):** Cadastro de novos clientes garantindo que todos os campos (ID, Nome, E-mail) sejam preenchidos.
*   **Read (Leitura):** Listagem completa de todos os clientes registados na base de dados.
*   **Update (Atualização):** Alteração seletiva de nome e/ou e-mail de um cliente existente.
*   **Delete (Exclusão):** Remoção permanente de um registo da base de dados.

## Validações e Segurança

Para garantir a integridade dos dados, a Controladora implementa várias camadas de proteção:
*   **Formato de E-mail:** Utilização de Expressões Regulares (Regex) para impedir o cadastro de e-mails inválidos (ex: múltiplos `@`).
*   **Chave Primária (ID):** O banco de dados bloqueia automaticamente a tentativa de criar dois clientes com o mesmo ID (`UNIQUE constraint`).
*   **E-mail Único:** Proteção no SQLite para impedir que clientes diferentes partilhem o mesmo endereço de e-mail.
*   **Validação de Existência:** O sistema verifica se um ID existe antes de tentar atualizá-lo ou excluí-lo.

## Como Executar 

### Pré-requisitos
*   Ter o [Python 3](https://www.python.org/downloads/) instalado.
*   A biblioteca `sqlite3` já faz parte da biblioteca padrão do Python (não é necessário instalar pacotes externos).

### Passos
1. Abra a pasta do projeto no VS Code.
2. Abra o terminal integrado (`Ctrl` + `'` ou `Ctrl` + `~`).
3. Execute o script principal:
   ```bash
   python crud_clientes.py