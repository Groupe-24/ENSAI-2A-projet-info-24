import requests
from dao.db_connection import DBConnection

# Le fichier sert à créer les différentes tables et les drops si elles existent déjà, il faut créer son .env

create_match_request = """
DROP TABLE IF EXISTS Matches CASCADE;
CREATE TABLE IF NOT EXISTS Matches (
    Id_Matches VARCHAR PRIMARY KEY,
    Date DATE,
    Id_Tournois VARCHAR,
    Equipe_Orange VARCHAR,
    Equipe_Bleu VARCHAR
);
"""

create_tournois_request = """ 
DROP TABLE IF EXISTS Tournois CASCADE;
CREATE TABLE IF NOT EXISTS Tournois (
    Id_Tournois VARCHAR PRIMARY KEY,
    Titre VARCHAR,
    Description TEXT,
    Date_Debut DATE,
    Date_Fin DATE,
    Id_Organisateur VARCHAR,
    Id_Equipe VARCHAR
);
"""

create_paris_request = """ 
DROP TABLE IF EXISTS Paris CASCADE;
CREATE TABLE IF NOT EXISTS Paris (
    Id_Paris VARCHAR PRIMARY KEY,
    Id_Matches VARCHAR,
    Id_Equipe VARCHAR,
    Id_Utilisateur VARCHAR,
    Mise DECIMAL(10, 2),
    Gain DECIMAL(10, 2)
);
"""

create_utilisateurs_request = """ 
DROP TABLE IF EXISTS Utilisateurs CASCADE;
CREATE TABLE IF NOT EXISTS Utilisateurs (
    Id_Utilisateur VARCHAR PRIMARY KEY,
    Pseudo VARCHAR,
    Email VARCHAR,
    Password VARCHAR,
    Id_Joueur VARCHAR,
    Administrateur BOOLEAN,
    Date_de_naissance DATE
);
"""

create_joueurs_request = """
DROP TABLE IF EXISTS Joueurs CASCADE;
CREATE TABLE IF NOT EXISTS Joueurs (
    Id_Joueurs VARCHAR PRIMARY KEY,
    Pseudo VARCHAR,
    Equipe VARCHAR,
    Professionnel BOOLEAN
);
"""

create_statistiques_request = """
DROP TABLE IF EXISTS Statistiques CASCADE;
CREATE TABLE IF NOT EXISTS Statistiques (
    Id_Statistique VARCHAR PRIMARY KEY,
    Joueur VARCHAR,
    Match VARCHAR,
    Equipe VARCHAR,
    Goals INT,
    Shots INT,
    Assits INT,
    Saves INT
);
"""

create_equipe_request = """ 
DROP TABLE IF EXISTS Equipe CASCADE;
CREATE TABLE IF NOT EXISTS Equipe (
    Id_Equipe VARCHAR PRIMARY KEY,
    Nom VARCHAR
);
"""

# Connexion à la base de données
connection = DBConnection().connection
cursor = connection.cursor()

# Exécution des requêtes SQL sans clés étrangères
cursor.execute(
    create_match_request
    + create_equipe_request
    + create_joueurs_request
    + create_statistiques_request
    + create_paris_request
    + create_utilisateurs_request
    + create_tournois_request
)

# Validation des changements
connection.commit()

# Ajout des clés étrangères après la création des tables
alter_statements = [
    """
    ALTER TABLE Matches
    ADD CONSTRAINT fk_tournois FOREIGN KEY (Id_Tournois) REFERENCES Tournois(Id_Tournois),
    ADD CONSTRAINT fk_equipe_orange FOREIGN KEY (Equipe_Orange) REFERENCES Equipe(Id_Equipe),
    ADD CONSTRAINT fk_equipe_bleu FOREIGN KEY (Equipe_Bleu) REFERENCES Equipe(Id_Equipe);
    """,
    """
    ALTER TABLE Tournois
    ADD CONSTRAINT fk_organisateur FOREIGN KEY (Id_Organisateur) REFERENCES Utilisateurs(Id_Utilisateur),
    ADD CONSTRAINT fk_equipe FOREIGN KEY (Id_Equipe) REFERENCES Equipe(Id_Equipe);
    """,
    """
    ALTER TABLE Paris
    ADD CONSTRAINT fk_matches FOREIGN KEY (Id_Matches) REFERENCES Matches(Id_Matches),
    ADD CONSTRAINT fk_equipe FOREIGN KEY (Id_Equipe) REFERENCES Equipe(Id_Equipe),
    ADD CONSTRAINT fk_utilisateur FOREIGN KEY (Id_Utilisateur) REFERENCES Utilisateurs(Id_Utilisateur);
    """,
    """
    ALTER TABLE Utilisateurs
    ADD CONSTRAINT fk_joueur FOREIGN KEY (Id_Joueur) REFERENCES Joueurs(Id_Joueurs);
    """,
    """
    ALTER TABLE Statistiques
    ADD CONSTRAINT fk_joueur FOREIGN KEY (Joueur) REFERENCES Joueurs(Id_Joueurs),
    ADD CONSTRAINT fk_match FOREIGN KEY (Match) REFERENCES Matches(Id_Matches),
    ADD CONSTRAINT fk_equipe FOREIGN KEY (Equipe) REFERENCES Equipe(Id_Equipe);
    """,
]

# Exécution des requêtes d'ALTER TABLE pour ajouter les clés étrangères
for statement in alter_statements:
    cursor.execute(statement)

# Validation des changements
connection.commit()
