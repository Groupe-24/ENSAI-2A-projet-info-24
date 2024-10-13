from db_connection import DBConnection


# Classe pour la table Joueurs
class JoueursDAO:
    def __init__(self, db_connection):
        self.connection = db_connection

    def insert_joueur(self, id_joueur, pseudo, equipe, professionnel):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO Joueurs (Id_Joueurs, Pseudo, Equipe, Professionnel) VALUES (?, ?, ?, ?);",
                (id_joueur, pseudo, equipe, professionnel),
            )
            self.connection.commit()
