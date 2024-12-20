from dao.db_connection import DBConnection
from contextlib import closing
from uuid import uuid4


class TournoiDAO:
    def __init__(self):
        self.connection = DBConnection().connection

    def insert_tournoi(
        self,
        id_tournoi=None,
        titre=None,
        description=None,
        date_debut=None,
        date_fin=None,
        id_organisateur=None,
        id_equipe=None,
    ):
        if id_tournoi is None:
            id_tournoi = str(uuid4())
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO Tournois(Id_Tournois, Titre, Description, Date_Debut, Date_Fin, "
                "Id_Organisateur, Id_Equipe) VALUES (%s, %s, %s, %s, %s, %s, %s);",
                (id_tournoi, titre, description, date_debut, date_fin, id_organisateur, id_equipe),
            )
            self.connection.commit()

    def get_tournoi_by_id(self, id_tournoi):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM Tournois WHERE Id_Tournois = %s;", (id_tournoi,))
            return cursor.fetchone()

    def get_tournoi_by_titre(self, titre):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM Tournois WHERE Titre = %s;", (titre,))
            return cursor.fetchall()

    def update_tournoi(
        self,
        id_tournoi,
        titre=None,
        description=None,
        date_debut=None,
        date_fin=None,
        id_organisateur=None,
        id_equipe=None,
    ):
        with closing(self.connection.cursor()) as cursor:
            updates = []
            params = []
            if titre is not None:
                updates.append("Titre = %s")
                params.append(titre)
            if description is not None:
                updates.append("Description = %s")
                params.append(description)
            if date_debut is not None:
                updates.append("Date_Debut = %s")
                params.append(date_debut)
            if date_fin is not None:
                updates.append("Date_Fin = %s")
                params.append(date_fin)
            if id_organisateur is not None:
                updates.append("Id_Organisateur = %s")
                params.append(id_organisateur)
            if id_equipe is not None:
                updates.append("Id_Equipe = %s")
                params.append(id_equipe)

            params.append(id_tournoi)
            update_query = "UPDATE Tournois SET " + ", ".join(updates) + " WHERE Id_Tournois = %s;"
            cursor.execute(update_query, params)
            self.connection.commit()

    def delete_tournoi(self, id_tournoi):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("DELETE FROM Tournois WHERE Id_Tournois = %s;", (id_tournoi,))
            self.connection.commit()

    def list_tournois(self):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM Tournois;")
            return cursor.fetchall()

    def is_in_tournoi(self, id_tournoi):
        table = self.get_tournoi_by_id(id_tournoi=id_tournoi)
        if table is None:
            return False
        else:
            return True

    def rajout_equipe(self, id_tournoi, id_equipe):
        if self.is_in_tournoi(id_tournoi):
            table = self.get_tournoi_by_id(id_tournoi=id_tournoi)
            liste_equipe_sans_modif = table["id_equipe"]
            if liste_equipe_sans_modif is None:
                self.update_tournoi(id_tournoi=id_tournoi, id_equipe=id_equipe)
            elif not (id_equipe in liste_equipe_sans_modif):
                list_equipe = liste_equipe_sans_modif + ", " + id_equipe
                self.update_tournoi(id_tournoi=id_tournoi, id_equipe=list_equipe)
