from dao.db_connection import DBConnection
from contextlib import closing
from uuid import uuid4


class ParisDAO:
    def __init__(self):
        self.connection = DBConnection().connection

    def insert_pari(
        self, id_pari=None, id_match=None, id_equipe=None, id_utilisateur=None, mise=None, gain=None
    ):
        if id_pari is None:
            id_pari = str(uuid4())
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO Paris(Id_Paris, Id_Matches, Id_Equipe, Id_Utilisateur, Mise, Gain) "
                "VALUES (%s, %s, %s, %s, %s, %s);",
                (id_pari, id_match, id_equipe, id_utilisateur, mise, gain),
            )
            self.connection.commit()

    def get_pari_by_id(self, id_pari):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM Paris WHERE Id_Paris = %s;", (id_pari,))
            return cursor.fetchone()

    def update_pari(
        self, id_pari, id_match=None, id_equipe=None, id_utilisateur=None, mise=None, gain=None
    ):
        with closing(self.connection.cursor()) as cursor:
            updates = []
            params = []

            if id_match is not None:
                updates.append("Id_Matches = %s")
                params.append(id_match)
            if id_equipe is not None:
                updates.append("Id_Equipe = %s")
                params.append(id_equipe)
            if id_utilisateur is not None:
                updates.append("Id_Utilisateur = %s")
                params.append(id_utilisateur)
            if mise is not None:
                updates.append("Mise = %s")
                params.append(mise)
            if gain is not None:
                updates.append("Gain = %s")
                params.append(gain)

            params.append(id_pari)
            update_query = "UPDATE Paris SET " + ", ".join(updates) + " WHERE Id_Paris = %s;"
            cursor.execute(update_query, params)
            self.connection.commit()

    def delete_pari(self, id_pari):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("DELETE FROM Paris WHERE Id_Paris = %s;", (id_pari,))
            self.connection.commit()

    def list_paris(self):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM Paris;")
            return cursor.fetchall()

    def exists_by_id(self, id_pari):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT EXISTS(SELECT 1 FROM Paris WHERE Id_Paris = %s);", (id_pari,))
            return cursor.fetchone()[0]

    def list_pari_match(self, id_match):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM Paris WHERE Id_Matches = %s;", (id_match,))
            return cursor.fetchall()
