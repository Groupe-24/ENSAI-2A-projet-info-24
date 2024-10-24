from dao.db_connection import DBConnection
from contextlib import closing
from uuid import uuid4


class UtilisateurDAO:

    def __init__(self):
        self.connection = DBConnection().connection

    def insert_utilisateur(
        self,
        pseudo,
        email,
        ddn,
        password,
        administrateur,
        organisateur,
        id_utilisateur=None,
        id_joueur=None,
    ):
        print("tu y es presque")
        if id_utilisateur is None:
            id_utilisateur = str(uuid4())
            print("aloooors")
            print(id_utilisateur)
        with closing(self.connection.cursor()) as cursor:
            print("maybe")
            cursor.execute(
                "INSERT INTO Utilisateurs(Id_Utilisateur, Pseudo, Email, Date_Naissance, Password,"
                " Id_Joueur, Administrateur, Organisateur) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                (
                    id_utilisateur,
                    pseudo,
                    email,
                    ddn,
                    password,
                    id_joueur,
                    administrateur,
                    organisateur,
                ),
            )
        print("alors là c'est bizarre")
        self.connection.commit()

    def get_utilisateur_by_id(self, id_utilisateur):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "SELECT * FROM Utilisateurs WHERE Id_Utilisateur = %s;", (id_utilisateur,)
            )
            return cursor.fetchone()  # Récupérer un seul utilisateur

    def update_utilisateur(
        self,
        id_utilisateur,
        pseudo=None,
        email=None,
        password=None,
        id_joueur=None,
        administrateur=None,
        organisateur=None,
    ):
        with closing(self.connection.cursor()) as cursor:
            # Créer la liste des colonnes à mettre à jour
            updates = []
            params = []
            if pseudo is not None:
                updates.append("Pseudo = %s")
                params.append(pseudo)
            if email is not None:
                updates.append("Email = %s")
                params.append(email)
            if password is not None:
                updates.append("Password = %s")
                params.append(password)
            if id_joueur is not None:
                updates.append("Id_Joueur = %s")
                params.append(id_joueur)
            if administrateur is not None:
                updates.append("Administrateur = %s")
                params.append(administrateur)
            if organisateur is not None:
                updates.append("Organisateur = %s")
                params.append(organisateur)

            params.append(id_utilisateur)  # Ajouter l'ID utilisateur à la fin des paramètres
            update_query = (
                "UPDATE Utilisateurs SET " + ", ".join(updates) + " WHERE Id_Utilisateur = %s;"
            )
            cursor.execute(update_query, params)
        self.connection.commit()

    def delete_utilisateur(self, id_utilisateur):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("DELETE FROM Utilisateurs WHERE Id_Utilisateur = %s;", (id_utilisateur,))
        self.connection.commit()

    def list_utilisateurs(self):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM Utilisateurs;")
            return cursor.fetchall()  # Récupérer tous les utilisateurs

    def get_utilisateur_by_parameters(
        self, pseudo=None, email=None, administrateur=None, id_joueur=None, organisateur=None
    ):
        query = "SELECT * FROM Utilisateurs WHERE 1=1"
        params = []

        # Construction dynamique de la requête
        if pseudo is not None:
            query += " AND Pseudo = %s"
            params.append(pseudo)

        if email is not None:
            query += " AND Email = %s"
            params.append(email)

        if administrateur is not None:
            query += " AND Administrateur = %s"
            params.append(administrateur)

        if organisateur is not None:
            query += " AND Organisateur = %s"
            params.append(organisateur)

        if id_joueur is not None:
            query += " AND Id_Joueur = %s"
            params.append(id_joueur)

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()  # Récupérer tous les utilisateurs correspondants

    def is_in_utilisateur(self, id_utilisateur):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM Utilisateurs WHERE Id_Utilisateur = %s);",
                (id_utilisateur,),
            )
            return cursor.fetchone()[0]  # Renvoie True ou False
