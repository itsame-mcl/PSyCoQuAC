DROP TABLE IF EXISTS fa;
CREATE TABLE IF NOT EXISTS fa (
    identifiant_fa INTEGER PRIMARY KEY AUTOINCREMENT,
    identifiant_pot INTEGER NOT NULL,
    identifiant_lot INTEGER NOT NULL,
    code_resultat TEXT NOT NULL,
    date_importation TEXT NOT NULL,
    date_dernier_traitement TEXT NOT NULL,
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
    est_superviseur INTEGER NOT NULL,
    quotite NUMERIC NOT NULL,
    identifiant_superviseur INTEGER,
    identifiant_delegue INTEGER,
    nom_utilisateur TEXT UNIQUE NOT NULL,
    mot_de_passe TEXT NOT NULL,
    prenom TEXT NOT NULL,
    nom TEXT NOT NULL
);

DROP TABLE IF EXISTS modeles;
CREATE TABLE IF NOT EXISTS modeles (
    identifiant_modele INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_modele TEXT NOT NULL,
    regex_nom_fichier TEXT NOT NULL,
    position_champ_numero TEXT NOT NULL,
    position_champ_voie TEXT NOT NULL,
    position_champ_code_postal TEXT NOT NULL,
    position_champ_ville TEXT NOT NULL,
    position_champs_supplementaires TEXT
);

INSERT INTO sqlite_sequence(name, seq)
VALUES
    ('fa',0),
    ('agents',0),
    ('modeles',0),
    ('lots',0);

INSERT INTO modeles(nom_modele, regex_nom_fichier, position_champ_numero,
                    position_champ_voie, position_champ_code_postal,
                    position_champ_ville,position_champs_supplementaires)
VALUES ('Modèle par défaut','.*','(0)','(1)','(2)','(3)','{}');
