DROP TABLE IF EXISTS fa;
CREATE TABLE IF NOT EXISTS fa (
    identifiant_fa SERIAL PRIMARY KEY,
    identifiant_pot INTEGER NOT NULL,
    identifiant_lot INTEGER NOT NULL,
    code_resultat CHAR(2) NOT NULL,
    date_importation DATE NOT NULL,
    date_dernier_traitement DATE NOT NULL,
    initial_numero VARCHAR(10),
    initial_voie VARCHAR(100),
    initial_code_postal VARCHAR(10),
    initial_ville VARCHAR(100),
    final_numero VARCHAR(10),
    final_voie VARCHAR(100),
    final_code_postal VARCHAR(10),
    final_ville VARCHAR(100),
    coordonnees_wgs84 float8[],
    champs_supplementaires TEXT[]
);

DROP SEQUENCE IF EXISTS identifiant_lot_seq;
CREATE SEQUENCE identifiant_lot_seq;

DROP TABLE IF EXISTS agents;
CREATE TABLE IF NOT EXISTS agents (
    identifiant_agent SERIAL PRIMARY KEY,
    est_superviseur BOOLEAN NOT NULL,
    quotite float8 NOT NULL,
    identifiant_superviseur INTEGER,
    identifiant_delegue INTEGER,
    nom_utilisateur VARCHAR(64) UNIQUE NOT NULL,
    mot_de_passe CHAR(128) NOT NULL,
    prenom VARCHAR(50) NOT NULL,
    nom VARCHAR(100) NOT NULL
);

DROP TABLE IF EXISTS modeles;
CREATE TABLE IF NOT EXISTS modeles (
    identifiant_modele SERIAL PRIMARY KEY,
    nom_modele VARCHAR(50) NOT NULL,
    regex_nom_fichier VARCHAR(255) NOT NULL,
    position_champ_numero SMALLINT[] NOT NULL,
    position_champ_voie SMALLINT[] NOT NULL,
    position_champ_code_postal SMALLINT[] NOT NULL,
    position_champ_ville SMALLINT[] NOT NULL,
    position_champs_supplementaires TEXT[][]
);

INSERT INTO modeles (nom_modele, regex_nom_fichier, position_champ_numero,
                     position_champ_voie, position_champ_code_postal, position_champ_ville)
VALUES ('Modèle par défaut','.*','{0}','{1}','{2}','{3}');