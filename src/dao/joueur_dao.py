from dao.db_connection import DBConnection
from contextlib import closing
from uuid import uuid4


class JoueursDAO:
    def __init__(self):
        self.connection = DBConnection().connection

    def insert_joueur(self, id_joueur=None, pseudo=None, equipe=None, professionnel=None):
        if id_joueur is None:
            id_joueur = str(uuid4())
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO Joueurs(Id_Joueurs, Pseudo, Equipe, Professionnel)"
                "VALUES (%s, %s, %s, %s);",
                (id_joueur, pseudo, equipe, professionnel),
            )
            self.connection.commit()

    def get_joueur_by_id(self, id_joueur):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM Joueurs WHERE Id_Joueurs = %s;", (id_joueur,))
            return cursor.fetchone()

    def get_joueur_by_pseudo(self, pseudo):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM Joueurs WHERE Pseudo = %s;", (pseudo,))
            return cursor.fetchone()

    def update_joueur(self, id_joueur, pseudo=None, equipe=None, professionnel=None):
        with closing(self.connection.cursor()) as cursor:
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

            params.append(id_joueur)
            update_query = "UPDATE Joueurs SET " + ", ".join(updates) + " WHERE Id_Joueurs = %s;"
            cursor.execute(update_query, params)
            self.connection.commit()

    def delete_joueur(self, id_joueur):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("DELETE FROM Joueurs WHERE Id_Joueurs = %s;", (id_joueur,))
            self.connection.commit()

    def list_joueurs(self):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM Joueurs;")
            return cursor.fetchall()

    def get_joueur_by_parameters(
        self, id_joueur=None, pseudo=None, equipe=None, professionnel=None
    ):
        query = "SELECT * FROM Joueurs WHERE 1=1"
        params = []

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
            query += " AND Id_Joueurs = %s"
            params.append(id_joueur)

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def is_in_joueur(self, id_joueur):
        a = self.get_joueur_by_id(id_joueur=id_joueur)
        if a is None:
            False
        else:
            True

    def is_in_joueur_by_pseudo(self, pseudo):
        a = self.get_joueur_by_pseudo(pseudo)
        if a is None:
            False
        else:
            True
