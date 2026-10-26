-- Sistema de Gerenciamento de Tarefas — MySQL 8.0.16+
-- (CHECK só é aplicado a partir da versão 8.0.16)

DROP DATABASE IF EXISTS gerenciamento_tarefas;
CREATE DATABASE gerenciamento_tarefas
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE gerenciamento_tarefas;

CREATE TABLE usuarios (
    id_usuario      INT AUTO_INCREMENT,
    nome_usuario    VARCHAR(100) NOT NULL,
    email_usuario   VARCHAR(120) NOT NULL,
    cargo_usuario   VARCHAR(60),
    CONSTRAINT pk_usuarios PRIMARY KEY (id_usuario),
    CONSTRAINT uk_usuarios_email UNIQUE (email_usuario)
);

CREATE TABLE projetos (
    id_projeto          INT AUTO_INCREMENT,
    nome_projeto        VARCHAR(100) NOT NULL,
    descricao_projeto   VARCHAR(255),
    data_inicio_projeto DATE NOT NULL,
    data_fim_projeto    DATE,
    CONSTRAINT pk_projetos PRIMARY KEY (id_projeto),
    CONSTRAINT ck_projetos_datas
        CHECK (data_fim_projeto IS NULL OR data_fim_projeto >= data_inicio_projeto)
);

CREATE TABLE tarefas (
    id_tarefa               INT AUTO_INCREMENT,
    titulo_tarefa           VARCHAR(120) NOT NULL,
    descricao_tarefa        VARCHAR(255),
    status_tarefa           VARCHAR(15)  NOT NULL DEFAULT 'PENDENTE',
    prioridade_tarefa       VARCHAR(10)  NOT NULL DEFAULT 'MEDIA',
    horas_gastas_tarefa     DECIMAL(6,2) NOT NULL DEFAULT 0,
    data_criacao_tarefa     DATE         NOT NULL,
    data_conclusao_tarefa   DATE,
    id_projeto              INT NOT NULL,
    id_usuario              INT NOT NULL,
    CONSTRAINT pk_tarefas PRIMARY KEY (id_tarefa),
    CONSTRAINT fk_tarefas_projetos FOREIGN KEY (id_projeto)
        REFERENCES projetos (id_projeto)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_tarefas_usuarios FOREIGN KEY (id_usuario)
        REFERENCES usuarios (id_usuario)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT ck_tarefas_status
        CHECK (status_tarefa IN ('PENDENTE', 'EM_ANDAMENTO', 'CONCLUIDA')),
    CONSTRAINT ck_tarefas_prioridade
        CHECK (prioridade_tarefa IN ('BAIXA', 'MEDIA', 'ALTA')),
    CONSTRAINT ck_tarefas_horas
        CHECK (horas_gastas_tarefa >= 0),
    CONSTRAINT ck_tarefas_conclusao
        CHECK (data_conclusao_tarefa IS NULL OR status_tarefa = 'CONCLUIDA')
);

CREATE INDEX idx_tarefas_projeto ON tarefas (id_projeto);
CREATE INDEX idx_tarefas_usuario ON tarefas (id_usuario);


INSERT INTO usuarios (nome_usuario, email_usuario, cargo_usuario) VALUES
    ('Murilo', 'murilo@exemplo.com', 'Analista'),
    ('Davi',   'davi@exemplo.com',   'Desenvolvedor'),
    ('George', 'george@exemplo.com', 'Desenvolvedor');

INSERT INTO projetos (nome_projeto, descricao_projeto, data_inicio_projeto, data_fim_projeto) VALUES
    ('Trabalho de Banco de Dados', 'CRUD com MySQL', '2026-10-01', '2026-10-30'),
    ('Site da Turma', 'Página institucional', '2026-10-05', NULL);

INSERT INTO tarefas
    (titulo_tarefa, descricao_tarefa, status_tarefa, prioridade_tarefa,
     horas_gastas_tarefa, data_criacao_tarefa, data_conclusao_tarefa, id_projeto, id_usuario) VALUES
    ('Modelar banco',       'Diagrama no Mermaid',  'CONCLUIDA',    'ALTA',  4.50, '2026-10-02', '2026-10-04', 1, 1),
    ('Criar script SQL',    'Tabelas e restrições', 'CONCLUIDA',    'ALTA',  3.00, '2026-10-04', '2026-10-05', 1, 1),
    ('Implementar CRUD',    'Inserir/atualizar',    'EM_ANDAMENTO', 'ALTA',  6.25, '2026-10-06', NULL,         1, 2),
    ('Criar menu e splash', 'Interface console',    'PENDENTE',     'MEDIA', 0.00, '2026-10-06', NULL,         1, 3),
    ('Definir layout',      'Wireframe',            'PENDENTE',     'BAIXA', 0.00, '2026-10-07', NULL,         2, 3);


-- Relatório 1 (GROUP BY): resumo por usuário
-- SELECT u.nome_usuario,
--        COUNT(t.id_tarefa) AS total_tarefas,
--        SUM(CASE WHEN t.status_tarefa = 'CONCLUIDA' THEN 1 ELSE 0 END) AS concluidas,
--        COALESCE(SUM(t.horas_gastas_tarefa), 0) AS horas_totais
-- FROM usuarios u
-- LEFT JOIN tarefas t ON t.id_usuario = u.id_usuario
-- GROUP BY u.id_usuario, u.nome_usuario
-- ORDER BY horas_totais DESC;

-- Relatório 2 (JOIN): tarefas com projeto e responsável
-- SELECT t.id_tarefa, t.titulo_tarefa, p.nome_projeto, u.nome_usuario,
--        t.status_tarefa, t.prioridade_tarefa, t.horas_gastas_tarefa
-- FROM tarefas t
-- INNER JOIN projetos p ON p.id_projeto = t.id_projeto
-- INNER JOIN usuarios u ON u.id_usuario = t.id_usuario
-- ORDER BY p.nome_projeto, t.id_tarefa;
