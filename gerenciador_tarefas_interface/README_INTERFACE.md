# Interface do Gerenciador de Tarefas

Esta entrega contém somente o menu principal e a tela inicial, conforme divisão de tarefas do grupo.

## Executar no Linux

Na raiz do projeto:

```bash
python3 -m src.principal
```

## Integrar com os módulos do grupo

No ponto de entrada do sistema completo, importe `executar` de `src.principal` e passe a conexão DB-API e um dicionário com as funções dos módulos:

```python
from src.principal import executar

# Exemplo: conexão e funções serão implementadas pelos demais integrantes.
# executar(conexao, {"1": relatorios, "2": inserir, "3": remover, "4": atualizar})
```

Cada função receberá `conexao` como argumento. Se o grupo adotar assinaturas diferentes, crie adaptadores.

Edite `src/utils/config.py` para informar os nomes completos dos integrantes e os nomes reais das tabelas. A contagem só funciona com uma conexão ativa e as tabelas criadas. Sem conexão, a interface informa que a contagem está indisponível, sem inventar valores.

Este pacote não implementa CRUD, relatórios ou conexão com banco de dados.

## Uso de IA

O edital solicita que o grupo registre no `PROMPTS.md` o prompt utilizado, sua fonte e o uso da resposta. Inclua a solicitação desta interface e descreva as adaptações feitas pelo grupo.
