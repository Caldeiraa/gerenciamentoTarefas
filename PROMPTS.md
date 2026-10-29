# PROMPTS.md — Registro de Uso de Inteligência Artificial

Em conformidade com as diretrizes do edital (**RNF05**), este documento registra o histórico de consultas realizadas a ferramentas de Inteligência Artificial Generativa durante o desenvolvimento do **Sistema de Gerenciamento de Tarefas**.

O uso de IA pelo grupo teve caráter estritamente consultivo, atuando como suporte para:
1. Discussão de arquitetura de software sem ORM (**RNF04**);
2. Refinamento de consultas SQL avançadas com agregações condicionais (**RF03**);
3. Validação de integridade referencial e tratamento de erros no banco (**RF05** / **RN08**);
4. Boas práticas de interface CLI e formatação no terminal (**RF01** / **RF02**);
5. Configuração e portabilidade do ambiente para a Máquina Virtual Linux (**RNF01**).

A modelagem conceitual, o script DDL, as regras de negócio e a implementação final do código foram integralmente conduzidas, validadas e testadas pelos integrantes da equipe.

---

## 📌 Registro Cronológico de Prompts

---

### Prompt 1 — Arquitetura modular sem ORM e separação de responsabilidades (RNF04)

- **Contexto:** Definição da estrutura de diretórios do projeto para atender a exigência de separação em camadas (`model`, `controller`, `conexion`, `sql`, `reports`, `utils`, `principal`), sem utilização de frameworks ou ORM.
- **Integrante:** George (Integração e Interface) / Davi (Controladores)
- **Ferramenta:** Google Gemini (Antigravity IDE)

**Prompt submetido:**
> "Estamos desenvolvendo um sistema em Python 3 para uma disciplina de Banco de Dados. O projeto deve persistir em MySQL 8.0 puro, sem nenhum ORM. Uma das exigências é organizar o projeto em pacotes: model, controller, conexion, sql, reports, utils e principal. 
> Como podemos estruturar a passagem de parâmetros e da conexão ativa entre essas camadas de forma limpa, garantindo que o módulo `sql` apenas monte as strings e parâmetros parametrizados (evitando SQL Injection), enquanto o `controller` gerencia transações e regras de negócio?"

**Retorno da IA:**
- A IA sugeriu que o módulo `sql` contivesse funções puras retornando tuplas `(query_string, parametros)`, utilizando placeholders `%s` do conector nativo.
- Sugeriu que o `controller` recebesse a instância da conexão, controlasse abertura de cursores, `commit()`, `rollback()` e validações, retornando objetos do `model`.
- Apresentou uma árvore de diretórios padrão alinhada ao padrão de camadas.

**Análise crítica e aplicação pelo grupo:**
- O grupo aprovou a abordagem de tuplas `(sql, params)` para desacoplar a construção da query da sua execução física, o que garantiu total conformidade com o **RNF02** (SQL por concatenação) e prevenção contra SQL Injection.
- O grupo optou por encapsular a inicialização em `python -m src.principal`, garantindo resolução consistente de módulos em ambientes Windows e Linux.

---

### Prompt 2 — Otimização de consulta com agregação e soma condicional (RF03.1)

- **Contexto:** Elaboração do relatório de produtividade de usuários com `GROUP BY`, total de tarefas, tarefas concluídas e horas gastas.
- **Integrante:** Murilo (Banco de Dados e Modelagem)
- **Ferramenta:** Google Gemini

**Prompt submetido:**
> "No MySQL 8, tenho as tabelas `usuarios (id_usuario, nome_usuario, ...)` e `tarefas (id_tarefa, id_usuario, status_tarefa, horas_gastas_tarefa, ...)`.
> Preciso de uma consulta agregada que retorne para cada usuário: total de tarefas, total de tarefas concluídas (status = 'CONCLUIDA') e a soma das horas gastas. 
> Importante: usuários que ainda não possuem tarefas cadastradas devem aparecer na listagem com 0 tarefas e 0 horas, e não serem omitidos. Qual a melhor forma de estruturar essa query com LEFT JOIN e agregação condicional?"

**Retorno da IA:**
- A IA apresentou a sugestão de utilizar `LEFT JOIN`, agrupando por `u.id_usuario, u.nome_usuario`.
- Para as tarefas concluídas, sugeriu o uso de `SUM(CASE WHEN t.status_tarefa = 'CONCLUIDA' THEN 1 ELSE 0 END)`.
- Para a soma de horas, sugeriu `COALESCE(SUM(t.horas_gastas_tarefa), 0)`.
- Alertou para a necessidade de usar `COUNT(t.id_tarefa)` em vez de `COUNT(*)`, pois `COUNT(*)` retornaria 1 para usuários sem tarefas devido à linha nula gerada pelo `LEFT JOIN`.

**Análise crítica e aplicação pelo grupo:**
- A observação sobre a diferença entre `COUNT(*)` e `COUNT(t.id_tarefa)` no `LEFT JOIN` foi validada nos testes no MySQL Workbench e evitou uma inconsistência de dados.
- A consulta foi integrada no módulo `src/reports/reports.py` na constante `_SQL_RELATORIO_USUARIO`, adicionando ordenação decrescente por horas totais (`ORDER BY horas_totais DESC`).

---

### Prompt 3 — Tratamento de integridade referencial na exclusão com opção em cascata (RF05 / RN08)

- **Contexto:** Atendimento ao requisito **RF05**, que prevê que ao tentar excluir um registro pai com dependências (como um usuário ou projeto que possui tarefas), o sistema deve alertar o operador e oferecer a exclusão em cascata das tarefas vinculadas.
- **Integrante:** Davi (Regras de Negócio e Controladores)
- **Ferramenta:** Google Gemini

**Prompt submetido:**
> "Em uma aplicação Python com MySQL Connector (sem ORM), como implementar uma exclusão segura de entidade pai (ex: Usuario) que tem relação 1:N com Tarefas? 
> O requisito exige: antes de deletar, verificar se há tarefas filhas. Se houver, alertar a quantidade e perguntar ao usuário se deseja cancelar ou excluir tudo em cascata. Caso confirme a cascata, como garantir que a exclusão dos filhos e do pai ocorra de forma atômica?"

**Retorno da IA:**
- Recomendou a realização de um `SELECT COUNT(1)` prévio para checar a existência de dependentes antes de tentar o `DELETE`.
- Sugeriu centralizar a lógica no `controller`, recebendo um parâmetro booleano `excluir_filhos=False`.
- Enfatizou o uso explícito de bloco `try/except` com `conexao.rollback()` em caso de falha durante a sequência de `cursor.execute()` de remoção dos filhos e do pai, chamando `conexao.commit()` apenas ao final de ambas as operações.

**Análise crítica e aplicação pelo grupo:**
- O grupo implementou esse padrão nas funções `excluir_usuario` e `excluir_projeto` em `src/controller/controller.py`.
- Adicionou-se mensagens amigáveis na camada visual (`src/principal.py`) para confirmar a ação explicitamente com o usuário (`[S/N]`), impedindo exclusões acidentais.

---

### Prompt 4 — Validações de domínio e consistência temporal (RN01, RN05, RN06, RN07)

- **Contexto:** Implementação de validações robustas no Python antes de enviar comandos de inserção ou atualização ao banco de dados.
- **Integrante:** Davi (Controladores e Regras de Negócio)
- **Ferramenta:** Google Gemini

**Prompt submetido:**
> "Preciso criar funções de validação em Python puro para aplicar regras de negócio antes de persistir dados no MySQL:
> 1. Validar e-mail com regex simples e eficiente;
> 2. Converter e validar datas no formato AAAA-MM-DD;
> 3. Garantir que a data de término de um projeto não seja anterior à data de início;
> 4. Garantir que horas gastas não sejam negativas.
> Qual a forma idiomática em Python de disparar exceções de validação para que a camada de apresentação capture e informe o usuário sem quebrar o programa?"

**Retorno da IA:**
- Forneceu a expressão regular `r'^[\w\.\-]+@[\w\.\-]+\.\w+$'` para validação do e-mail.
- Demonstrou a conversão de strings para objetos `datetime.date` para possibilitar a comparação direta `data_fim < data_inicio`.
- Sugeriu o lançamento de `ValueError` com mensagens claras e descritivas, permitindo captura unificada no menu interativo via `except ValueError as e`.

**Análise crítica e aplicação pelo grupo:**
- O grupo incorporou os validadores auxiliares `_validar_email`, `_parse_data` e as checagens de datas em `src/controller/controller.py`.
- No menu principal (`src/principal.py`), foram criados blocos de captura para exibir `[AVISO] <mensagem>` e permitir nova tentativa de digitação pelo usuário.

---

### Prompt 5 — Splash Screen dinâmica e formatação de tabela no console (RF01 / RF02)

- **Contexto:** Construção da tela inicial obrigatória exibindo a contagem dinâmica de registros de todas as tabelas (`usuarios`, `projetos`, `tarefas`), dados dos integrantes e menu interativo resiliente.
- **Integrante:** George (Interface e Apresentação)
- **Ferramenta:** Google Gemini

**Prompt submetido:**
> "Para a entrega de um trabalho acadêmico de Banco de Dados, preciso construir uma Splash Screen em console (terminal) em Python. 
> Ela precisa fazer uma contagem dinâmica (`SELECT COUNT(1) FROM tabela`) de cada uma das 3 tabelas do sistema, imprimir os nomes dos integrantes, professor e disciplina em um quadro formatado com caracteres ASCII/Unicode. 
> Além disso, como estruturar o loop do menu principal para que continue rodando após cada operação até que o usuário digite a opção de sair?"

**Retorno da IA:**
- Demonstrou a função de consulta dinâmica iterando sobre uma lista de tabelas definidas em arquivo de configuração.
- Sugeriu o uso de f-strings com alinhamento (`:<`, `:>`) para criar caixas de texto padronizadas no terminal sem depender de bibliotecas externas como `tabulate` ou `rich`.
- Exemplificou a estrutura de loop `while True` com tratamento de exceções e pausa com `input("Pressione Enter para continuar...")`.

**Análise crítica e aplicação pelo grupo:**
- O layout gerado foi customizado para incluir a paleta visual e os dados da disciplina em `src/utils/config.py` e `src/utils/splash_screen.py`.
- O grupo optou por não usar dependências externas para garantir execução imediata em qualquer ambiente Linux/Windows sem conflitos de pacotes.

---

### Prompt 6 — Portabilidade de execução e ambiente na VM Linux (RNF01)

- **Contexto:** Garantir que o projeto rode perfeitamente tanto no ambiente de desenvolvimento (Windows) quanto na Máquina Virtual de avaliação do professor (Linux Debian/Ubuntu).
- **Integrante:** George (Documentação e Integração) / Murilo (Banco de Dados)
- **Ferramenta:** Google Gemini

**Prompt submetido:**
> "Temos um projeto em Python com conexão ao MySQL via `mysql-connector-python`. Ele foi desenvolvido no Windows e agora precisa rodar na VM Linux da disciplina. 
> Quais são os comandos essenciais para instalar o conector no Ubuntu/Debian via apt e pip, e qual o comando recomendado para executar o script principal garantindo que os imports relativos da pasta `src` sejam localizados sem erro de `ModuleNotFoundError`?"

**Retorno da IA:**
- Recomendou a instalação de `python3`, `python3-pip` e o pacote `mysql-connector-python`.
- Explicou a importância de rodar a aplicação a partir do diretório raiz utilizando a flag de módulo: `python3 -m src.principal`, o que adiciona automaticamente o diretório corrente ao `sys.path`.

**Análise crítica e aplicação pelo grupo:**
- O grupo testou os passos na VM Linux, validando a execução do script SQL via terminal e o arranque da aplicação.
- As instruções detalhadas foram documentadas na seção 4 do `README.md`.

---

## 📊 Síntese da Participação dos Integrantes

| Integrante | Área Principal | Atividades Desenvolvidas pelo Aluno | Papel da IA no Apoio |
|---|---|---|---|
| **Murilo** | Banco de Dados & SQL | Modelagem ER, elaboração do `script_criacao.sql`, constraints de FK, definição de índices e elaboração das queries dos relatórios | Consulta sobre agregação condicional com `CASE WHEN` e `COALESCE` no `GROUP BY`. |
| **Davi** | Controladores & CRUD | Implementação dos fluxos de Inserção, Atualização e Exclusão; regras de negócio RN01 a RN08; controle transacional (`commit`/`rollback`) | Esclarecimento de padrão para transações atômicas com exclusão em cascata e regex de validação. |
| **George** | Interface & Integração | Estruturação dos submenus, montagem da Splash Screen (RF01), orquestração do loop principal (RF02), documentação do `README.md` e gravação do vídeo | Boas práticas de formatação de console e comando de execução de módulos em Linux. |

---

## Conclusão

O uso de Inteligência Artificial ao longo do projeto foi pautado pela ética acadêmica e pelo aprendizado prático. Em todas as etapas, os membros da equipe mantiveram a autoria das decisões de projeto, utilizando a ferramenta como acelerador de pesquisa técnica e guia de boas práticas de engenharia de software e banco de dados.
