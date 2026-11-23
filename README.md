# Sistema de Gerenciamento de Tarefas

## 1. Apresentação

O Sistema de Gerenciamento de Tarefas é uma aplicação desenvolvida em Python para cadastrar e gerenciar usuários, projetos e tarefas. O projeto foi desenvolvido para a disciplina de Banco de Dados, sob orientação do professor Howard Roatti, no semestre 2026/2.

Nesta versão, a persistência dos dados é realizada por meio do MongoDB, utilizando a biblioteca PyMongo.

## 2. Integrantes e responsabilidades

| Integrante | Responsabilidade |
|---|---|
| Murilo Caldeira Sousa | Banco de dados e modelagem |
| Davi Mendes Barcelos | Operações CRUD, regras de negócio e controladores |
| George Pinheiro Ramos | Interface, integração, menus, fluxo de execução, tela inicial e documentação |

## 3. Tecnologias utilizadas

- Python 3.10 ou superior.
- MongoDB Community Server.
- PyMongo.
- Git e GitHub para controle de versão.

## 4. Pré-requisitos

Antes de executar o sistema, é necessário instalar:

1. Python 3.10 ou superior.
2. MongoDB Community Server.
3. Biblioteca PyMongo.

A instalação do MongoDB pode ser realizada pelos links oficiais:

- Windows: https://www.mongodb.com/try/download/community
- Ubuntu: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/
- Debian: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-debian/

Para visualizar e administrar os dados, também é possível utilizar o MongoDB Compass:

https://www.mongodb.com/products/tools/compass

## 5. Obtenção do projeto

Clone o repositório:

```bash
git clone https://github.com/Caldeiraa/gerenciamentoTarefas.git
```

Acesse a pasta do projeto:

```bash
cd gerenciamentoTarefas
```

## 6. Configuração do ambiente

Recomenda-se utilizar um ambiente virtual Python.

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Ubuntu/Debian:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Com o ambiente virtual ativado, instale a biblioteca PyMongo:

```bash
python -m pip install pymongo
```

## 7. Configuração do banco de dados

A aplicação utiliza o MongoDB com as seguintes configurações padrão:

| Parâmetro | Valor |
|---|---|
| Endereço de conexão | mongodb://localhost:27017/ |
| Banco de dados | gerenciamento_tarefas |
| Coleções | usuarios, projetos e tarefas |

A configuração da conexão está implementada no arquivo `src/conexion/mongo_connection.py`.

O sistema permite definir o endereço de conexão e o nome do banco por meio das variáveis de ambiente `MONGO_URI` e `MONGO_DB_NAME`.

Quando essas variáveis não são configuradas, são utilizados os valores padrão apresentados na tabela.

O banco de dados e as coleções são criados pelo MongoDB conforme a aplicação realiza as primeiras gravações. Portanto, não é necessário executar um script SQL para criar as tabelas.

## 8. Execução do sistema

Antes de executar a aplicação, certifique-se de que o serviço MongoDB esteja iniciado.

Na pasta principal do projeto, com o ambiente virtual ativado, execute:

**Windows:**

```powershell
python -m src.principal
```

**Ubuntu/Debian:**

```bash
python3 -m src.principal
```

Após a execução, será apresentada a tela inicial do sistema e, em seguida, o menu principal.

## 9. Criação das coleções

O projeto disponibiliza o script `script_criacao_mongo.py`, localizado na pasta principal, para criar as coleções necessárias no MongoDB.

Para executar o script, utilize:

```bash
python script_criacao_mongo.py
```

O script verifica a existência das coleções `usuarios`, `projetos` e `tarefas`, criando apenas aquelas que ainda não existem. Os registros já armazenados são preservados.

## 10. Funcionalidades

O sistema disponibiliza as seguintes funcionalidades:

- **Tela inicial:** apresenta informações do projeto e a quantidade de registros armazenados.
- **Menu principal:** permite acessar as operações disponíveis.
- **Inserção:** cadastro de usuários, projetos e tarefas.
- **Consulta e relatórios:** apresentação de informações armazenadas no banco de dados, utilizando operações de agregação do MongoDB.
- **Atualização:** alteração dos dados cadastrados.
- **Remoção:** exclusão de registros, considerando os relacionamentos entre usuários, projetos e tarefas.
- **Validações:** aplicação de regras de negócio relacionadas aos dados cadastrados.

## 11. Estrutura do projeto

```text
gerenciamentoTarefas/
│
├── src/
│   ├── conexion/
│   │   ├── mongo_connection.py
│   │   └── db_connection.py
│   │
│   ├── controller/
│   │   └── controller.py
│   │
│   ├── model/
│   │   └── models.py
│   │
│   ├── reports/
│   │   └── reports.py
│   │
│   ├── utils/
│   │   ├── config.py
│   │   └── splash_screen.py
│   │
│   └── principal.py
│
├── modelo_relacional.md
├── modeloRelacional.png
├── PROMPTS.md
└── README.md
```

## 12. Modelagem de dados

O projeto contempla três entidades principais: usuários, projetos e tarefas.

Os relacionamentos estabelecidos são:

- Um usuário pode ser responsável por várias tarefas.
- Um projeto pode possuir várias tarefas.
- Cada tarefa está associada a um usuário responsável e a um projeto.

O arquivo `modelo_relacional.md` apresenta a modelagem e os relacionamentos entre as entidades.

## 13. Vídeo demonstrativo

O vídeo demonstrativo do projeto está disponível no YouTube:

https://youtu.be/wwb_LKxzltk

**Observação:** a demonstração em vídeo deverá corresponder à versão atual do sistema, que utiliza MongoDB.

## 14. Repositório

O código-fonte e o histórico de desenvolvimento estão disponíveis no GitHub:

https://github.com/Caldeiraa/gerenciamentoTarefas

## 15. Testes e validação dos relatórios

Em 22/11/2026, foram realizados testes funcionais dos três relatórios do sistema Gerenciador de Tarefas, utilizando o banco de dados MongoDB.

### RF03.1 — Resumo por usuário (AGGREGATE)
- Usuário testado: Jack.
- Total de tarefas: 1.
- Tarefas concluídas: 0.
- Total de horas: 2,00.
- **Resultado:** aprovado.

### RF03.2 — Tarefas detalhadas (LOOKUP)
- Tarefa: Teste dos relatórios C3.
- Projeto: Projeto Demonstração C3.
- Responsável: Jack.
- Status: PENDENTE.
- Prioridade: MEDIA.
- Horas: 2,00.
- **Resultado:** aprovado.

### RF03.3 — Tarefas por projeto e status (AGGREGATE)
- Projeto: Projeto Demonstração C3.
- Status: PENDENTE.
- Quantidade de tarefas: 1.
- **Resultado:** aprovado.

### Conclusão dos testes

Os três relatórios apresentaram os resultados esperados durante os testes realizados. Foram verificadas as consultas, agregações e associações entre as coleções `usuarios`, `projetos` e `tarefas` do MongoDB.

Não foi necessária alteração no módulo `src/reports/reports.py`, pois as funcionalidades testadas apresentaram o comportamento esperado.
