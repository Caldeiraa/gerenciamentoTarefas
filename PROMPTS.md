# PROMPTS.md — Registro de Uso de Inteligência Artificial

Conforme solicitado no edital (RNF05), este arquivo documenta os prompts utilizados com auxílio de IA durante o desenvolvimento do projeto.

---

## Prompt 1 — Estrutura do projeto e integração dos módulos

**Fonte:** Google Gemini (Antigravity IDE)

**Prompt utilizado:**
> "Fiquei responsável pela parte de menu principal e tela inicial, integração dos módulos, README, vídeo e revisão final. Preciso que você faça a minha parte seguindo o edital e o que já tem no projeto."

**Uso da resposta:**
A IA gerou a estrutura completa do projeto conforme RNF04 (model, controller, conexion, sql, reports, utils, principal), incluindo:
- Módulo `principal.py` com menu principal (RF02), splash screen (RF01) e integração de todos os submenus
- Módulo de conexão MySQL (`conexion/db_connection.py`)
- Módulo SQL com queries por concatenação de texto (`sql/queries.py`) conforme RNF02
- Controller com validações de todas as regras de negócio (RN01–RN08)
- Módulo de relatórios com RF03.1 (GROUP BY), RF03.2 (JOIN) e RF03.3
- Models para as 3 entidades
- README.md completo

**Adaptações feitas pelo grupo:**
- Ajuste das credenciais de conexão para o ambiente da VM Linux
- Inclusão dos nomes completos dos integrantes em `config.py`
- Testes de integração com o banco de dados criado pelo script SQL

---
