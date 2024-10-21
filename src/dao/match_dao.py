import psycopg2
import json

class MatchDAO:
    def _init_(self, db_connection):
        """
        Initialise le DAO avec une connexion à la base de données.
        """
        self.conn = db_connection

    def ajouter_match(self, match):
        """
        Ajoute un nouveau match dans la base de données.
        """
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    INSERT INTO matchs (id, evenement, date, equipe1, equipe2, buts1, buts2, tirs1, tirs2, score1, score2, assists1, assists2, arrets1, arrets2)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    match.id,
                    match.evenement,
                    match.date,
                    match.equipe1.id_equipe,  # On peut stocker l'ID des équipes
                    match.equipe2.id_equipe,
                    json.dumps(match.buts1),   # On stocke les statistiques en JSON
                    json.dumps(match.buts2),
                    json.dumps(match.tirs1),
                    json.dumps(match.tirs2),
                    json.dumps(match.score1),
                    json.dumps(match.score2),
                    json.dumps(match.assists1),
                    json.dumps(match.assists2),
                    json.dumps(match.arrets1),
                    json.dumps(match.arrets2)
                ))
                self.conn.commit()
        except Exception as e:
            print(f"Erreur lors de l'ajout du match : {e}")
            self.conn.rollback()


    # Méthode pour lister tous les matchs
    def lister_tous_les_matchs(self):
        """
        Retourne une liste de tous les matchs présents dans la base de données.
        """
        matchs = []
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM matchs"
                cursor.execute(sql)
                resultats = cursor.fetchall()

                equipe_dao = EquipeDAO(self.conn)  # Utiliser un DAO pour les équipes

                for result in resultats:
                    equipe1 = equipe_dao.obtenir_equipe(result[3])  # Récupérer l'équipe 1 par son ID
                    equipe2 = equipe_dao.obtenir_equipe(result[4])  # Récupérer l'équipe 2 par son ID
                    
                    match = Match(
                        id=result[0],
                        evenement=result[1],
                        date=result[2],
                        equipe1=equipe1,
                        equipe2=equipe2,
                        buts1=json.loads(result[5]),
                        buts2=json.loads(result[6]),
                        tirs1=json.loads(result[7]),
                        tirs2=json.loads(result[8]),
                        score1=json.loads(result[9]),
                        score2=json.loads(result[10]),
                        assists1=json.loads(result[11]),
                        assists2=json.loads(result[12]),
                        arrets1=json.loads(result[13]),
                        arrets2=json.loads(result[14])
                    )
                    matchs.append(match)
        except Exception as e:
            print(f"Erreur lors de la récupération des matchs : {e}")
            return []

        return matchs

    def obtenir_match(self, match_id):
        """
        Récupère un match à partir de son identifiant.
        """
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT * FROM matchs WHERE id = %s"
                cursor.execute(sql, (match_id,))
                result = cursor.fetchone()
                if result:
                    equipe_dao = EquipeDAO(self.conn)  # Utiliser un DAO pour les équipes
                    equipe1 = equipe_dao.obtenir_equipe(result[3])  # Récupérer les équipes par leur ID
                    equipe2 = equipe_dao.obtenir_equipe(result[4])
                    
                    return Match(
                        id=result[0],
                        evenement=result[1],
                        date=result[2],
                        equipe1=equipe1,
                        equipe2=equipe2,
                        buts1=json.loads(result[5]),  # Convertir le JSON en dictionnaire Python
                        buts2=json.loads(result[6]),
                        tirs1=json.loads(result[7]),
                        tirs2=json.loads(result[8]),
                        score1=json.loads(result[9]),
                        score2=json.loads(result[10]),
                        assists1=json.loads(result[11]),
                        assists2=json.loads(result[12]),
                        arrets1=json.loads(result[13]),
                        arrets2=json.loads(result[14])
                    )
        except Exception as e:
            print(f"Erreur lors de la récupération du match : {e}")
            return None

    def mettre_a_jour_match(self, match):
        """
        Met à jour les informations d'un match dans la base de données.
        """
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    UPDATE matchs
                    SET evenement = %s, date = %s, equipe1 = %s, equipe2 = %s, 
                        buts1 = %s, buts2 = %s, tirs1 = %s, tirs2 = %s,
                        score1 = %s, score2 = %s, assists1 = %s, assists2 = %s, 
                        arrets1 = %s, arrets2 = %s
                    WHERE id = %s
                """
                cursor.execute(sql, (
                    match.evenement,
                    match.date,
                    match.equipe1.id_equipe,  # Utiliser l'ID de l'équipe
                    match.equipe2.id_equipe,
                    json.dumps(match.buts1),   # Convertir les dictionnaires en JSON
                    json.dumps(match.buts2),
                    json.dumps(match.tirs1),
                    json.dumps(match.tirs2),
                    json.dumps(match.score1),
                    json.dumps(match.score2),
                    json.dumps(match.assists1),
                    json.dumps(match.assists2),
                    json.dumps(match.arrets1),
                    json.dumps(match.arrets2),
                    match.id
                ))
                self.conn.commit()
        except Exception as e:
            print(f"Erreur lors de la mise à jour du match : {e}")
            self.conn.rollback()

    def supprimer_match(self, match_id):
        """
        Supprime un match de la base de données.
        """
        try:
            with self.conn.cursor() as cursor:
                sql = "DELETE FROM matchs WHERE id = %s"
                cursor.execute(sql, (match_id,))
                self.conn.commit()
        except Exception as e:
            print(f"Erreur lors de la suppression du match : {e}")
            self.conn.rollback()