from db_connection import DBConnection
from contextlib import closing


# Classe pour la table Joueurs
class JoueursDAO:
    def __init__(self, db_connection):
        self.connection = db_connection

    def insert_joueur(self, id_joueur=None, pseudo=None, equipe=None, professionnel=None):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO Joueurs(Id_Joueurs, Pseudo, Equipe, Professionnel)"
                "VALUES (%s, %s, %s, %s);",
                (id_joueur, pseudo, equipe, professionnel),
            )
            self.connection.commit()

    def get_joueur_by_id(self, id_joueur):
        with closing(self.connection.cursor()) as cursor:  # Correction ici
            cursor.execute(
                "SELECT * FROM Joueurs WHERE Id_Joueurs = %s;", (id_joueur,)
            )  # Correction du nom de colonne
            return cursor.fetchone()  # Retourne un seul joueur

    def update_joueur(self, id_joueur, pseudo=None, equipe=None, professionnel=None):
        with closing(self.connection.cursor()) as cursor:
            # Créer la liste des colonnes à mettre à jour
            updates = []
            params = []
            if pseudo is not None:
                updates.append("Pseudo = %s")
                params.append(pseudo)
            if equipe is not None:
                updates.append("Equipe = %s")
                params.append(equipe)
            if professionnel is not None:
                updates.append("Professionnel = %s")
                params.append(professionnel)

            params.append(id_joueur)  # Ajouter l'ID joueur à la fin des paramètres
            update_query = (
                "UPDATE Joueurs SET " + ", ".join(updates) + " WHERE Id_Joueurs = %s;"
            )  # Correction ici
            cursor.execute(update_query, params)
            self.connection.commit()

    def delete_joueur(self, id_joueur):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "DELETE FROM Joueurs WHERE Id_Joueurs = %s;", (id_joueur,)
            )  # Correction ici
            self.connection.commit()

    def list_joueurs(self):  # Correction du nom de la méthode
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM Joueurs;")  # Correction ici
            return cursor.fetchall()  # Récupérer tous les joueurs

    def get_joueur_by_parameters(
        self, id_joueur=None, pseudo=None, equipe=None, professionnel=None
    ):
        query = "SELECT * FROM Joueurs WHERE 1=1"
        params = []

        # Construction dynamique de la requête
        if pseudo is not None:
            query += " AND Pseudo = %s"
            params.append(pseudo)

        if equipe is not None:
            query += " AND Equipe = %s"
            params.append(equipe)

        if professionnel is not None:
            query += " AND Professionnel = %s"
            params.append(professionnel)

        if id_joueur is not None:
            query += " AND Id_Joueur = %s"
            params.append(id_joueur)

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()  # Récupérer tous les utilisateurs correspondants

    def is_in_joueur(self, id_joueur):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM Joueurs WHERE Id_Joueurs = %s);", (id_joueur,)
            )
            return cursor.fetchone()[0]  # Renvoie True ou False
