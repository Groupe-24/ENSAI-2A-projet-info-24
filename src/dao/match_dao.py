from db_connection import DBConnection
from contextlib import closing
from uuid import uuid4


# Classe pour la table Match
class MatchDAO:
    def __init__(self):
        self.connection = DBConnection().connection

    def insert_match(
        self, id_match=None, date=None, id_tournoi=None, equipe_orange=None, equipe_bleu=None
    ):
        if id_match is None:
            id_match = str(uuid4())
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO Matches(Id_Matches, Date, Id_Tournois, Equipe_Orange, Equipe_Bleu) VALUES (%s, %s, %s, %s, %s);",
                (id_match, date, id_tournoi, equipe_orange, equipe_bleu),
            )
            self.connection.commit()

    def get_match_by_id(self, id_match):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM Matches WHERE Id_Matches = %s;", (id_match,))
            return cursor.fetchone()  # Retourne un seul match

    def update_match(
        self, id_match, date=None, id_tournoi=None, equipe_orange=None, equipe_bleu=None
    ):
        with closing(self.connection.cursor()) as cursor:
            updates = []
            params = []
            if date is not None:
                updates.append("Date = %s")
                params.append(date)
            if id_tournoi is not None:
                updates.append("Id_Tournois = %s")
                params.append(id_tournoi)
            if equipe_orange is not None:
                updates.append("Equipe_Orange = %s")
                params.append(equipe_orange)
            if equipe_bleu is not None:
                updates.append("Equipe_Bleu = %s")
                params.append(equipe_bleu)

            params.append(id_match)  # Ajouter l'ID match à la fin des paramètres
            update_query = "UPDATE Matches SET " + ", ".join(updates) + " WHERE Id_Matches = %s;"
            cursor.execute(update_query, params)
            self.connection.commit()

    def delete_match(self, id_match):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("DELETE FROM Matches WHERE Id_Matches = %s;", (id_match,))
            self.connection.commit()

    def list_matches(self):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM Matches;")
            return cursor.fetchall()  # Récupérer tous les matchs

    def is_in_match(self, id_match):
        # with closing(self.connection.cursor()) as cursor:
        #     cursor.execute(
        #         "SELECT EXISTS(SELECT 1 FROM Matches WHERE Id_Matches = %s);", (id_match,)
        #     )
        #     return cursor.fetchone()[0]  # Renvoie True ou False
        a = self.get_match_by_id(id_match=id_match)
        if a is None:
            return False
        else:
            return True

    def calendrier(self, Date, id_tournois=None):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM Matches WHERE Date > %s ORDER BY Date);", (Date,))
            return cursor.fetchall()
