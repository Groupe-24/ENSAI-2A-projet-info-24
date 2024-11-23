class StatistiqueService:
    def __init__(self, statistiques_dao):
        self.dao = statistiques_dao

    def ajouter_statistique(
        self, id_statistique, joueur, match, equipe, goals, assists, saves, shots, score
    ):
        # Vérification de l'existence de l'ID statistique
        if self.dao.exists_by_id(id_statistique):
            raise ValueError(f"La statistique avec l'ID {id_statistique} existe déjà.")

        # Insertion de la nouvelle statistique dans la base de données
        self.dao.insert_statistique(
            id_statistique, joueur, match, equipe, goals, assists, saves, shots, score
        )
        return f"Statistique ajoutée avec succès pour l'ID {id_statistique}."

    def obtenir_statistique(self, id_statistique):
        # Obtention d'une statistique par son ID
        statistique = self.dao.get_statistique_by_id(id_statistique)
        if not statistique:
            raise ValueError(f"Aucune statistique trouvée avec l'ID {id_statistique}.")
        return statistique

    def mettre_a_jour_statistique(self, id_statistique, **kwargs):
        # Vérification si l'ID existe avant de mettre à jour
        if not self.dao.exists_by_id(id_statistique):
            raise ValueError(f"Aucune statistique trouvée avec l'ID {id_statistique}.")

        # Mise à jour de la statistique
        self.dao.update_statistique(id_statistique, **kwargs)
        return f"Statistique avec l'ID {id_statistique} mise à jour avec succès."

    def supprimer_statistique(self, id_statistique):
        # Vérification de l'existence de l'ID avant suppression
        if not self.dao.exists_by_id(id_statistique):
            raise ValueError(f"Aucune statistique trouvée avec l'ID {id_statistique}.")

        # Suppression de la statistique
        self.dao.delete_statistique(id_statistique)
        return f"Statistique avec l'ID {id_statistique} supprimée avec succès."

    def lister_statistiques(self):
        # Récupération de toutes les statistiques
        statistiques = self.dao.list_statistiques()
        if not statistiques:
            return "Aucune statistique disponible."
        return statistiques

    def obtenir_statistiques_equipe(self, equipe):
        # Récupération des statistiques d'une équipe
        result = self.dao.statistique_equipe(equipe)
        if not result:
            return f"Aucune statistique trouvée pour l'équipe {equipe}."
        return {
            "equipe": result[0],
            "total_goals": result[1],
            "total_score": result[2],
            "total_assists": result[3],
            "total_saves": result[4],
            "total_shots": result[5],
        }

    def obtenir_statistiques_match(self, match):
        # Récupération des statistiques d'un match
        result = self.dao.statistique_match(match)
        if not result:
            return f"Aucune statistique trouvée pour le match {match}."
        return [
            {
                "match": r[0],
                "total_goals": r[1],
                "total_score": r[2],
                "total_assists": r[3],
                "total_saves": r[4],
                "total_shots": r[5],
            }
            for r in result
        ]

    def obtenir_statistiques_joueur(self, joueur):
        # Récupération des statistiques d'un joueur
        result = self.dao.statistique_joueur(joueur)
        if not result:
            return f"Aucune statistique trouvée pour le joueur {joueur}."
        return {
            "joueur": result[0],
            "total_goals": result[1],
            "total_score": result[2],
            "total_assists": result[3],
            "total_saves": result[4],
            "total_shots": result[5],
        }


from dao.statistique_dao import StatistiquesDAO

print(StatistiqueService(StatistiquesDAO()).lister_statistiques())
