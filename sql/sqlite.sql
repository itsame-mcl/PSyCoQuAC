DROP TABLE IF EXISTS fa;
CREATE TABLE IF NOT EXISTS fa (
    identifiant_fa INTEGER PRIMARY KEY AUTOINCREMENT,
    identifiant_pot INTEGER,
    identifiant_lot INTEGER,
    code_resultat TEXT,
    date_importation TEXT,
    date_dernier_traitement TEXT,
    initial_numero TEXT,
    initial_voie TEXT,
    initial_code_postal TEXT,
    initial_ville TEXT,
    final_numero TEXT,
    final_voie TEXT,
    final_code_postal TEXT,
    final_ville TEXT,
    coordonnees_wgs84 TEXT,
    champs_supplementaires TEXT
);

DROP TABLE IF EXISTS agents;
CREATE TABLE IF NOT EXISTS agents (
    identifiant_agent INTEGER PRIMARY KEY AUTOINCREMENT,
    est_superviseur INTEGER,
    quotite NUMERIC,
    identifiant_superviseur INTEGER,
    nom_utilisateur TEXT,
    mot_de_passe TEXT,
    prenom TEXT,
    nom TEXT
);

DROP TABLE IF EXISTS modeles;
CREATE TABLE IF NOT EXISTS modeles (
    identifiant_modele INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_modele TEXT,
    regex_nom_fichier TEXT,
    position_champ_numero INTEGER,
    position_champ_voie INTEGER,
    position_champ_code_postal INTEGER,
    position_champ_ville INTEGER,
    position_champs_supplementaires TEXT
);

INSERT INTO sqlite_sequence(name, seq)
VALUES
    ("fa",0),
    ("agents",0),
    ("modeles",0),
    ("lots",0);