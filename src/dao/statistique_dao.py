from dao.db_connection import DBConnection
from contextlib import closing
from uuid import uuid4


class StatistiquesDAO:
    def __init__(self):
        self.connection = DBConnection().connection

    def insert_statistique(
        self,
        id_statistique=None,
        joueur=None,
        match=None,
        equipe=None,
        goals=None,
        assists=None,
        saves=None,
        shots=None,
        score=None,
    ):
        if id_statistique is None:
            id_statistique = str(uuid4())
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO Statistiques(Id_Statistique, Joueur, Match, Equipe, Goals, Assists, Saves, Shots, Score) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
                (id_statistique, joueur, match, equipe, goals, assists, saves, shots, score),
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
        goals=None,
        shots=None,
        assists=None,
        saves=None,
        score=None,
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
            if goals is not None:
                updates.append("Goals = %s")
                params.append(goals)
            if saves is not None:
                updates.append("Saves = %s")
                params.append(saves)
            if assists is not None:
                updates.append("Assists = %s")
                params.append(assists)
            if score is not None:
                updates.append("Score = %s")
                params.append(score)
            if shots is not None:
                updates.append("Shots = %s")
                params.append(shots)

            params.append(id_statistique)  # Ajouter l'ID statistique à la fin des paramètres
            update_query = (
                "UPDATE Statistiques SET " + ", ".join(updates) + " WHERE Id_Statistique = %s;"
            )
            cursor.execute(update_query, params)
            self.connection.commit()

    def delete_statistique(self, id_statistique):
        try:
            with closing(self.connection.cursor()) as cursor:
                cursor.execute(
                    "DELETE FROM Statistiques WHERE Id_Statistique = %s;", (id_statistique,)
                )
                if cursor.rowcount == 0:  # Vérifie si une ligne a été affectée
                    raise ValueError("Statistique non trouvée")
                self.connection.commit()
        except ValueError as ve:
            print(f"Erreur : {ve}")
        except Exception as e:
            print(f"Erreur inattendue : {e}")

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
                "SELECT Equipe, SUM(Goals), SUM(Score),SUM(assists),SUM(Saves),SUM(Saves),SUM(Shots)"
                "FROM Statistiques WHERE Equipe = %s GROUP BY Equipe;",
                (equipe,),
            )
            return cursor.fetchone()

    def statistique_match(self, match):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "SELECT Match,SUM(Goals), SUM(Score),SUM(assists),SUM(Saves),SUM(Saves),SUM(Shots)"
                "FROM Statistiques WHERE Match = %s GROUP BY Match;",
                (match,),
            )
            return cursor.fetchall()

    def statistique_joueur(self, joueur):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "SELECT Joueur,SUM(Goals), SUM(Score),SUM(assists),SUM(Saves),SUM(Saves),SUM(Shots)"
                "FROM Statistiques WHERE Joueur = %s GROUP BY Joueur;",
                (joueur,),
            )
            return cursor.fetchone()

    def get_statistique_by_parameters(
        self,
        id_statistique=None,
        joueur=None,
        match=None,
        equipe=None,
        goals=None,
        shots=None,
        assists=None,
        saves=None,
        score=None,
    ):
        query = "SELECT * FROM Statistiques WHERE 1=1"
        params = []

        # Construction dynamique de la requête
        if id_statistique is not None:
            query += " AND Id_Statistique = %s"
            params.append(id_statistique)

        if joueur is not None:
            query += " AND Joueur = %s"
            params.append(joueur)

        if match is not None:
            query += " AND Match = %s"
            params.append(match)

        if equipe is not None:
            query += " AND Equipe = %s"
            params.append(equipe)

        if goals is not None:
            query += " AND Goals = %s"
            params.append(goals)

        if shots is not None:
            query += " AND Shots = %s"
            params.append(shots)

        if assists is not None:
            query += " AND Assists = %s"
            params.append(assists)

        if saves is not None:
            query += " AND Saves = %s"
            params.append(saves)

        if score is not None:
            query += " AND Score = %s"
            params.append(score)

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()  # Récupérer tous les utilisateurs correspondants
