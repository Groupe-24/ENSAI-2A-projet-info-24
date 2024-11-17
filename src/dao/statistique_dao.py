from db_connection import DBConnection
from contextlib import closing


# Classe pour la table Statistiques
class StatistiquesDAO:
    def __init__(self, db_connection):
        self.connection = db_connection

    def insert_statistique(
        self, id_statistique, joueur, match, equipe, but, score_de_match, consommation_boost
    ):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO Statistiques(Id_Statistique, Joueur, Match, Equipe, But, Score_De_Match, Consommation_Du_Boost) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s);",
                (id_statistique, joueur, match, equipe, but, score_de_match, consommation_boost),
            )
            self.connection.commit()

    def get_statistique_by_id(self, id_statistique):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "SELECT * FROM Statistiques WHERE Id_Statistique = %s;", (id_statistique,)
            )
            return cursor.fetchone()  # Retourne une seule statistique

    def update_statistique(
        self,
        id_statistique,
        joueur=None,
        match=None,
        equipe=None,
        but=None,
        score_de_match=None,
        consommation_boost=None,
    ):
        with closing(self.connection.cursor()) as cursor:
            updates = []
            params = []

            if joueur is not None:
                updates.append("Joueur = %s")
                params.append(joueur)
            if match is not None:
                updates.append("Match = %s")
                params.append(match)
            if equipe is not None:
                updates.append("Equipe = %s")
                params.append(equipe)
            if but is not None:
                updates.append("But = %s")
                params.append(but)
            if score_de_match is not None:
                updates.append("Score_De_Match = %s")
                params.append(score_de_match)
            if consommation_boost is not None:
                updates.append("Consommation_Du_Boost = %s")
                params.append(consommation_boost)

            params.append(id_statistique)  # Ajouter l'ID statistique à la fin des paramètres
            update_query = (
                "UPDATE Statistiques SET " + ", ".join(updates) + " WHERE Id_Statistique = %s;"
            )
            cursor.execute(update_query, params)
            self.connection.commit()

    def delete_statistique(self, id_statistique):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("DELETE FROM Statistiques WHERE Id_Statistique = %s;", (id_statistique,))
            self.connection.commit()

    def list_statistiques(self):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM Statistiques;")
            return cursor.fetchall()  # Récupérer toutes les statistiques

    def exists_by_id(self, id_statistique):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM Statistiques WHERE Id_Statistique = %s);",
                (id_statistique,),
            )
            return cursor.fetchone()[0]  # Renvoie True ou False

    def statistique_equipe(self, equipe):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "SELECT equipe,SUM(but),SUM(score_de_match) FROM Statistiques GROUP BY equipe WHERE equipe=%s"
            )
            return cursor.fetchone()

    def statistique_match(self, match):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "SELECT match,SUM(but),SUM(score_de_match) FROM Statistiques GROUP BY match WHERE match=%s"
            )
            return cursor.fetchall()

    def statistique_joueur(self, joueur):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "SELECT joueur,SUM(but),SUM(score_de_match) FROM Statistiques GROUP BY joueur WHERE joueur=%s"
            )
            return cursor.fetchone()
