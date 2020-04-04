PRAGMA foreign_keys = ON;

CREATE TABLE utilizadores (
    id            INTEGER PRIMARY KEY,
    nome          TEXT,
    username      TEXT,
    password      TEXT
);

CREATE TABLE albuns (
    id            INTEGER PRIMARY KEY,
    id_banda      INTEGER,
    nome          TEXT,
    ano_album     INTEGER,
    FOREIGN KEY(id_banda) REFERENCES bandas(id)
);

CREATE TABLE bandas (
    id            INTEGER PRIMARY KEY,
    nome          TEXT,
    ano           INTEGER,
    genero        TEXT
);

CREATE TABLE rates (
    id            INTEGER PRIMARY KEY,
    designacao    TEXT,
    sigla         TEXT
);

CREATE TABLE listas_albuns (
    id_user       INTEGER,
    id_album      INTEGER,
    id_rate       INTEGER,
    PRIMARY KEY (id_user, id_album),
    FOREIGN KEY(id_user) REFERENCES utilizadores(id),
    FOREIGN KEY(id_album) REFERENCES albuns(id)
    FOREIGN KEY(id_rate) REFERENCES rates(id)
);

INSERT INTO rates (id, designacao, sigla) VALUES
    (1, "Mau", "M"),
    (2, "Mais ou menos", "MM"),
    (3, "Suficiente", "S"),
    (4, "Bom", "B"),
    (5, "Muito bom", "MB")
;
