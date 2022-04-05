INSERT INTO settings (active, version, web, api)
VALUES (True, '1.0', '{ "visible": { "/categorias": false } }', '{}');

-- privilegios básicos, agnosticos ao fork
INSERT INTO privilegios (name, created_user, updated_user) VALUES
    ('Administrador', 0, 0), -- 1
    ('Moderador', 0, 0), -- 2
    ('Participante', 0, 0); -- 3


-- usuário admin, agnostico ao fork
--      query nao ta errada, se algum intellisense apontar erro é pq a IDE não entende o "OVERRIDING SYSTEM VALUE"
INSERT INTO usuarios (id, type, email, username, password, name, has_accepted_terms, created_user, updated_user)
OVERRIDING SYSTEM VALUE VALUES (0, 1, 'admin@email.com', 'admin', '12345', 'Administrador', False, 0, 0);

INSERT INTO categorias (id, name, created_user, updated_user)
OVERRIDING SYSTEM VALUE VALUES (0, 'Sem Categoria', 0, 0);

-- TESTING INSERTS
INSERT INTO categorias (name, created_date, created_user, updated_date, updated_user)
VALUES ('Orientações', '2022-03-02 10:08:40.420395', 0, '2022-03-02 10:08:40.420395', 0), -- 1
       ('Atividades', '2022-03-02 10:08:40.420395', 0, '2022-03-02 10:08:40.420395', 0), -- 2
       ('Interação Social', '2022-03-02 10:08:40.420395', 0, '2022-03-02 10:08:40.420395', 0), -- 3
       ('Sintomas Atípicos', '2022-03-02 10:08:40.420395', 0, '2022-03-02 10:08:40.420395', 0) -- 4
;

INSERT INTO categorias (name, created_date, created_user, updated_date, updated_user)
VALUES ('Categoria Teste', '2022-03-02 10:08:40.420395', 0, '2022-03-02 10:08:40.420395', 0); -- 5

INSERT INTO postagens (categoria, titulo, texto, selo, created_date, created_user, updated_date, updated_user)
VALUES (0, 'Post 1', 1, 'false', '2022-03-02 14:31:21.414159', 0, '2022-03-02 14:31:21.414159', 0); -- 1
INSERT INTO postagens (categoria, titulo, texto, selo, created_date, created_user, updated_date, updated_user)
VALUES (0, 'Post 2', 2, 'true', '2022-03-02 14:31:21.414159', 0, '2022-03-02 14:31:21.414159', 0); -- 2
INSERT INTO postagens (categoria, titulo, texto, selo, created_date, created_user, updated_date, updated_user)
VALUES (1, 'Post 3', 3, 'true', '2022-03-02 14:31:21.414159', 0, '2022-03-02 14:31:21.414159', 0); -- 3


SELECT * FROM settings;

SELECT * FROM usuarios;
SELECT * FROM privilegios;

SELECT * FROM categorias;
SELECT * FROM postagens ORDER BY created_date DESC;
SELECT * FROM comentarios;

UPDATE usuarios SET data = NULL WHERE id = 0