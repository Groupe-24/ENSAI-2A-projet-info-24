from db_connection import DBConnection
from contextlib import closing


# Classe pour la table Joueurs
class JoueursDAO:
    def __init__(self):
        self.connection = DBConnection().connection

    def insert_joueur(self, id_joueur=None, pseudo=None, equipe=None, professionnel=None):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO Joueurs(Id_Joueurs, Pseudo, Equipe, Professionnel)"
                "VALUES (%s, %s, %s, %s);",
                (id_joueur, pseudo, equipe, professionnel),
            )
            self.connection.commit()

    def get_joueur_by_id(self, id_joueur):
        with closing(self.connection.cursor()) as cursor:  # Correction ici
            cursor.execute(
                "SELECT * FROM Joueurs WHERE Id_Joueurs = %s;", (id_joueur,)
            )  # Correction du nom de colonne
            return cursor.fetchone()  # Retourne un seul joueur

    def update_joueur(self, id_joueur, pseudo=None, equipe=None, professionnel=None):
        with closing(self.connection.cursor()) as cursor:
            # Créer la liste des colonnes à mettre à jour
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

            params.append(id_joueur)  # Ajouter l'ID joueur à la fin des paramètres
            update_query = (
                "UPDATE Joueurs SET " + ", ".join(updates) + " WHERE Id_Joueurs = %s;"
            )  # Correction ici
            cursor.execute(update_query, params)
            self.connection.commit()

    def delete_joueur(self, id_joueur):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(
                "DELETE FROM Joueurs WHERE Id_Joueurs = %s;", (id_joueur,)
            )  # Correction ici
            self.connection.commit()

    def list_joueurs(self):  # Correction du nom de la méthode
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM Joueurs;")  # Correction ici
            return cursor.fetchall()  # Récupérer tous les joueurs

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
            query += " AND Id_Joueurs = %s"
            params.append(id_joueur)

        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()  # Récupérer tous les utilisateurs correspondants

    def is_in_joueur(self, id_joueur):
        with closing(self.connection.cursor()) as cursor:
            try:
                # Vérifier si la table est vide
                cursor.execute("SELECT COUNT(*) FROM Joueurs;")
                count_result = cursor.fetchone()

                # Afficher le résultat pour le débogage
                print(f"Résultat du COUNT: {count_result}")

                # Vérifiez si count_result est bien une liste ou un tuple
                if count_result is None or len(count_result) == 0:
                    return True  # La table est vide, renvoyer True

                # Vérifier si la table est vide
                if count_result[0] == 0:
                    return True  # La table est vide, renvoyer True

                # Vérifier si le joueur existe
                cursor.execute(
                    "SELECT EXISTS(SELECT 1 FROM Joueurs WHERE Id_Joueur = %s);", (id_joueur,)
                )
                result = cursor.fetchone()

                # Assurez-vous que result n'est pas None
                return (
                    result[0] if result else False
                )  # Renvoie True si le joueur existe, sinon False

            except Exception as e:
                print(f"Erreur lors de l'exécution de la requête: {e}")
                return False  # Renvoie False en cas d'erreur
