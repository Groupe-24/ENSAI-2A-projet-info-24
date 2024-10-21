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