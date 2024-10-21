<<<<<<< HEAD
import psycopg2

class UtilisateurDAO:
    def _init_(self, db_connection):
        """
        Initialise le DAO avec une connexion à la base de données.
        """
        self.conn = db_connection

    def ajouter_utilisateur(self, utilisateur):
        """
        Ajoute un nouvel utilisateur dans la base de données.
        """
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    INSERT INTO utilisateurs (id_utilisateur, nom, mail, date_de_naissance, mdp, administrateur, organisateur)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    utilisateur.id_utilisateur, utilisateur.nom, utilisateur.mail,
                    utilisateur.date_de_naissance, utilisateur.mdp, utilisateur.administrateur,
                    utilisateur.organisateur
                ))
                self.conn.commit()
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'utilisateur : {e}")
            self.conn.rollback()

    def obtenir_utilisateur(self, id_utilisateur):
        """
        Récupère un utilisateur à partir de son identifiant.
        """
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM utilisateurs WHERE id_utilisateur = %s"
                cursor.execute(sql, (id_utilisateur,))
                result = cursor.fetchone()
                if result:
                    return Utilisateur(
                        id=result[0],
                        nom=result[1],
                        mail=result[2],
                        ddn=result[3],
                        mdp=result[4],
                        administrateur=result[5],
                        organisateur=result[6]
                    )
        except Exception as e:
            print(f"Erreur lors de la récupération de l'utilisateur : {e}")
            return None

    def mettre_a_jour_utilisateur(self, utilisateur):
        """
        Met à jour les informations d'un utilisateur dans la base de données.
        """
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    UPDATE utilisateurs
                    SET nom = %s, mail = %s, date_de_naissance = %s, mdp = %s, administrateur = %s, organisateur = %s
                    WHERE id_utilisateur = %s
                """
                cursor.execute(sql, (
                    utilisateur.nom, utilisateur.mail, utilisateur.date_de_naissance,
                    utilisateur.mdp, utilisateur.administrateur, utilisateur.organisateur,
                    utilisateur.id_utilisateur
                ))
                self.conn.commit()
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'utilisateur : {e}")
            self.conn.rollback()

    def supprimer_utilisateur(self, id_utilisateur):
        """
        Supprime un utilisateur de la base de données.
        """
        try:
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM utilisateurs WHERE id_utilisateur = %s"
                cursor.execute(sql, (id_utilisateur,))
                self.conn.commit()
        except Exception as e:
            print(f"Erreur lors de la suppression de l'utilisateur : {e}")
            self.conn.rollback()
=======
from db_connection import DBConnection
from contextlib import closing


class UtilisateurDAO:

    def __init__(self, db_connection):
        self.connection = DBConnection().connection

    def insert_utilisateur(
        self, id_utilisateur, pseudo, email, password, id_joueur, administrateur
    ):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO Utilisateurs (Id_Utilisateur, Pseudo, Email, Password, Id_Joueur, Administrateur) "
                "VALUES (%s, %s, %s, %s, %s, %s);",
                (id_utilisateur, pseudo, email, password, id_joueur, administrateur),
            )
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
        self, pseudo=None, email=None, administrateur=None, id_joueur=None
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
>>>>>>> 43d75505600556759e994fca74866c5d585967f4
