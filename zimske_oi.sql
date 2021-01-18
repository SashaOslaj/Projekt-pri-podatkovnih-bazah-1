--
-- File generated with SQLiteStudio v3.2.1 on Mon Jan 18 12:03:33 2021
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: disciplina
CREATE TABLE disciplina (
    id  INTEGER  PRIMARY KEY AUTOINCREMENT,
    ime TEXT     UNIQUE NOT NULL
);

-- Table: drzava
CREATE TABLE drzava (
    kratica VARCHAR(3)  PRIMARY KEY,
    ime     TEXT
);

-- Table: licenca
CREATE TABLE licenca (
  id TEXT PRIMARY KEY
);

-- Table: olimpijskeIgre
CREATE TABLE olimpijskeIgre (
    leto   INT         PRIMARY KEY,
    drzava VARCHAR(3)  REFERENCES drzava(kratica) 
);

-- Table: poddisciplina
CREATE TABLE poddisciplina (
    id         INTEGER    PRIMARY KEY AUTOINCREMENT,
    ime        TEXT       NOT NULL,
    disciplina INT        REFERENCES disciplina(id)
);

-- Table: popravi
CREATE TABLE popravi (
    uporabnik  TEXT REFERENCES uporabnik (uporabniskoIme),
    tekmovalec INT REFERENCES tekmovalec (id),
    kajNaredi  TEXT NOT NULL,
    razlog     TEXT NOT NULL
);

-- Table: rezultat
CREATE TABLE rezultat (
    id         INTEGER    PRIMARY KEY AUTOINCREMENT,
    leto       INT        NOT NULL REFERENCES olimpijskeIgre(leto),
    disciplina INT        NOT NULL REFERENCES poddisciplina(id),
    tekmovalec INT        NOT NULL REFERENCES tekmovalec(id),
    drzava     VARCHAR(3) REFERENCES drzava(kratica),
    mesto      INT,
    rezultat   TEXT
);

-- Table: tekmovalec
CREATE TABLE tekmovalec (
    id     INTEGER     PRIMARY KEY AUTOINCREMENT,
    ime    TEXT        NOT NULL,
    rojen  DATE,
    drzava VARCHAR(3)  REFERENCES drzava(kratica)
);

-- Table: uporabnik
CREATE TABLE uporabnik (
    uporabniskoIme TEXT PRIMARY KEY,
    geslo          TEXT,
    licenca        TEXT REFERENCES licenca(id)
);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
