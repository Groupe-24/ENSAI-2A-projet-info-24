import requests
from dao.db_connection import DBConnection

# Le fichier sert à créer les différentes tables et les drops si elles existent déjà, il faut créer son .env

create_match_request = """
DROP TABLE IF EXISTS Matches CASCADE;
CREATE TABLE IF NOT EXISTS Matches (
    Id_Matches VARCHAR(255) PRIMARY KEY,
    Date DATE,
    Id_Tournois VARCHAR(255),
    Equipe_Orange VARCHAR(255),
    Equipe_Bleu VARCHAR(255)
);
"""

create_tournois_request = """ 
DROP TABLE IF EXISTS Tournois CASCADE;
CREATE TABLE IF NOT EXISTS Tournois (
    Id_Tournois VARCHAR(255) PRIMARY KEY,
    Titre VARCHAR(255),
    Description TEXT,
    Date_Debut DATE,
    Date_Fin DATE,
    Id_Organisateur VARCHAR(255),
    Id_Equipe VARCHAR(255)
);
"""

create_paris_request = """ 
DROP TABLE IF EXISTS Paris CASCADE;
CREATE TABLE IF NOT EXISTS Paris (
    Id_Paris VARCHAR(255) PRIMARY KEY,
    Id_Matches VARCHAR(255),
    Id_Equipe VARCHAR(255),
    Id_Utilisateur VARCHAR(255),
    Mise DECIMAL(10, 2),
    Gain DECIMAL(10, 2)
);
"""

create_utilisateurs_request = """ 
DROP TABLE IF EXISTS Utilisateurs CASCADE;
CREATE TABLE IF NOT EXISTS Utilisateurs (
    Id_Utilisateur VARCHAR(255) PRIMARY KEY,
    Pseudo VARCHAR(255),
    Email VARCHAR(255),
    Password VARCHAR(255),
    Id_Joueur VARCHAR(255),
    Administrateur BOOLEAN
);
"""

create_joueurs_request = """
DROP TABLE IF EXISTS Joueurs CASCADE;
CREATE TABLE IF NOT EXISTS Joueurs (
    Id_Joueurs VARCHAR(255) PRIMARY KEY,
    Pseudo VARCHAR(255),
    Equipe VARCHAR(255),
    Professionnel BOOLEAN
);
"""

create_statistiques_request = """
DROP TABLE IF EXISTS Statistiques CASCADE;
CREATE TABLE IF NOT EXISTS Statistiques (
    Id_Statistique VARCHAR(255) PRIMARY KEY,
    Joueur VARCHAR(255),
    Match VARCHAR(255),
    Equipe VARCHAR(255),
    But INT,
    Score_De_Match DECIMAL(10, 2),
    Consommation_Du_Boost DECIMAL(10, 2)
);
"""

create_equipe_request = """ 
DROP TABLE IF EXISTS Equipe CASCADE;
CREATE TABLE IF NOT EXISTS Equipe (
    Id_Equipe VARCHAR(255) PRIMARY KEY,
    Nom VARCHAR(255)
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
