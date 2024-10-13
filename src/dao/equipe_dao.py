from db_connection import DBConnection
from contextlib import closing


# Classe pour la table Équipe
class EquipeDAO:
    def __init__(self, db_connection):
        self.connection = db_connection

    def insert_equipe(self, id_equipe=None, nom=None):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO Equipe(Id_Equipe, Nom) VALUES (%s, %s);",
                (id_equipe, nom),
            )
            self.connection.commit()

    def get_equipe_by_id(self, id_equipe):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM Equipe WHERE Id_Equipe = %s;", (id_equipe,))
            return cursor.fetchone()  # Retourne une seule équipe

    def update_equipe(self, id_equipe, nom=None):
        with closing(self.connection.cursor()) as cursor:
            updates = []
            params = []
            if nom is not None:
                updates.append("Nom = %s")
                params.append(nom)

            params.append(id_equipe)  # Ajouter l'ID équipe à la fin des paramètres
            update_query = "UPDATE Equipe SET " + ", ".join(updates) + " WHERE Id_Equipe = %s;"
            cursor.execute(update_query, params)
            self.connection.commit()

    def delete_equipe(self, id_equipe):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("DELETE FROM Equipe WHERE Id_Equipe = %s;", (id_equipe,))
            self.connection.commit()

    def list_equipes(self):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM Equipe;")
            return cursor.fetchall()  # Récupérer toutes les équipes

    def is_in_equipe(self, id_equipe):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM Equipe WHERE Id_Equipe = %s);", (id_equipe,)
            )
            return cursor.fetchone()[0]  # Renvoie True ou False
