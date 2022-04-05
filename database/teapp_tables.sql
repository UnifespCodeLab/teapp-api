--
-- CREATION/UPDATE FIELDS TEMPLATE
--
--     -- creation/update
--     created_date TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     created_user INTEGER NOT NULL,
--     updated_date TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     updated_user INTEGER NOT NULL,
--
--     FOREIGN KEY (created_user) REFERENCES usuarios (id),
--     FOREIGN KEY (updated_user) REFERENCES usuarios (id)
--     -- creation/update

DROP TABLE IF EXISTS settings;
DROP TABLE IF EXISTS comentarios;
DROP TABLE IF EXISTS postagens;
DROP TABLE IF EXISTS categorias;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS privilegios;

--
-- USUARIOS
--

CREATE TABLE privilegios (
    id INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name CHARACTER VARYING(80) NOT NULL,

    -- creation/update
    created_date TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_user INTEGER NOT NULL,
    updated_date TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_user INTEGER NOT NULL
    -- creation/update
);

CREATE TABLE usuarios (
    id INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    type INTEGER NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    -- ou o usuário tem um email e/ou um nome de usuario
    email CHARACTER VARYING(120),
    username CHARACTER VARYING(80),
    password CHARACTER VARYING(80) NOT NULL,
    name CHARACTER VARYING(180) NOT NULL,
    has_accepted_terms BOOLEAN NOT NULL DEFAULT FALSE,
    -- dados necessarios pro fork local? não vejo mt a necessidade de criar uma tabela pra isso se as vantagens do
    --      banco relacional não vão ser relevantes
    --      um problema seria a falta de um "schema" pra isso, e talvez a necessidade de salvar um schema também?
    --      esse schema ficaria onde, em uma tabela "config" com coisas do fork?
    --      no exemplo do campo "bairro" pro ibeapp, seria um id dentro de dados ou uma string com o nome do bairro?
    --      se fosse um id, onde ficaria a relação de id_bairro -> nome do bairro? talvez uma tabela geral chamada
    --      "metadados", com colunas como o tipo de dado, id e nome? talvez ficasse "fixa" no código?
    --      se esse campo "bairro" nunca for utilizado como WHERE/JOIN em query, ele não precisa ser "relacional" em
    --      nenhum sentido
    --      formulario socioeconomico estaria dentro disso também?
    --      notificacoes_conf também?
    data JSON DEFAULT NULL,

    -- creation/update
    created_date TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_user INTEGER NOT NULL,
    updated_date TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_user INTEGER NOT NULL
    -- creation/update
);

--
-- POSTAGENS
--

CREATE TABLE categorias (
    id INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    name CHARACTER VARYING(80) NOT NULL,

    -- creation/update
    created_date TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_user INTEGER NOT NULL,
    updated_date TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_user INTEGER NOT NULL,

    FOREIGN KEY (created_user) REFERENCES usuarios (id),
    FOREIGN KEY (updated_user) REFERENCES usuarios (id)
    -- creation/update
);

CREATE TABLE postagens (
    id INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    categoria INTEGER NOT NULL,

    titulo CHARACTER VARYING(400) NOT NULL,
    texto CHARACTER VARYING(400) NOT NULL,
    selo BOOLEAN NOT NULL DEFAULT FALSE,

    FOREIGN KEY (categoria) REFERENCES categorias (id),

    -- creation/update
    created_date TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_user INTEGER NOT NULL,
    updated_date TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_user INTEGER NOT NULL,

    FOREIGN KEY (created_user) REFERENCES usuarios (id),
    FOREIGN KEY (updated_user) REFERENCES usuarios (id)
    -- creation/update
);

CREATE TABLE comentarios (
    id INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    texto CHARACTER VARYING(400) NOT NULL,
    postagem INTEGER NOT NULL,
    resposta INTEGER,

    FOREIGN KEY (postagem) REFERENCES postagens (id),

    -- creation/update
    created_date TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_user INTEGER NOT NULL,
    updated_date TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_user INTEGER NOT NULL,

    FOREIGN KEY (created_user) REFERENCES usuarios (id),
    FOREIGN KEY (updated_user) REFERENCES usuarios (id)
    -- creation/update
);

--
-- SETTINGS
--

CREATE TABLE settings (
    id INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    active BOOLEAN DEFAULT FALSE NOT NULL,

    version VARCHAR(10) NOT NULL,

    web JSON DEFAULT NULL,
    api JSON DEFAULT NULL
);
