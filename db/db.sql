CREATE TABLE IF NOT EXISTS users (
    id_user INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(50),
    prenom VARCHAR(50),
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100),
    salt VARCHAR(32),
    hash VARCHAR(128),
    etablissements_list TEXT 
);


CREATE TABLE IF NOT EXISTS violations (
    id_poursuite INTEGER PRIMARY KEY,
    buisness_id INTEGER,
    date DATE,
    description TEXT,
    adresse VARCHAR(255),
    date_jugement DATE,
    etablissement VARCHAR(100),
    montant INTEGER,
    proprietaire VARCHAR(100),
    ville VARCHAR(50),
    statut VARCHAR(100),
    date_statut DATE,
    categorie VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS demandes_inspection (
    id_demande INTEGER PRIMARY KEY,
    etablissement VARCHAR(100),
    adresse VARCHAR(255),
    ville VARCHAR(50),
    date_demande DATE,
    nom_client VARCHAR(100),
    description_demande TEXT
);

-- seed

INSERT INTO users (nom, prenom, username, email, salt, hash, etablissements_list) 
VALUES ('Butler', 'Gerard', 'prof', 'gerard.butler@uqam.ca', '472d20e06c14477b8c2bc343d9e48a15', 'f37bfea807ccee4a9d95e6bbbe98fbfcce29002fc04f3a828dbcbb55c2ce203c82877e2bce3b2ac3be053564f4f1b5e1e5815dc41d3fbae75202e449982ee065', 'Restaurant UQAM, Café Robert');


