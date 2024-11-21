from dao.statistique_dao import StatistiquesDAO


class StatistiqueService:
    def __init__(self, statistiques_dao):
        self.dao = statistiques_dao

    def ajouter_statistique(
        self, id_statistique, joueur, match, equipe, but, score_de_match, consommation_boost
    ):
        if self.dao.exists_by_id(id_statistique):
            raise ValueError(f"La statistique avec l'ID {id_statistique} existe déjà.")
        self.dao.insert_statistique(
            id_statistique, joueur, match, equipe, but, score_de_match, consommation_boost
        )
        return f"Statistique ajoutée avec succès pour l'ID {id_statistique}."

    def obtenir_statistique(self, id_statistique):
        statistique = self.dao.get_statistique_by_id(id_statistique)
        if not statistique:
            raise ValueError(f"Aucune statistique trouvée avec l'ID {id_statistique}.")
        return statistique

    def mettre_a_jour_statistique(self, id_statistique, **kwargs):
        if not self.dao.exists_by_id(id_statistique):
            raise ValueError(f"Aucune statistique trouvée avec l'ID {id_statistique}.")
        self.dao.update_statistique(id_statistique, **kwargs)
        return f"Statistique avec l'ID {id_statistique} mise à jour avec succès."

    def supprimer_statistique(self, id_statistique):
        if not self.dao.exists_by_id(id_statistique):
            raise ValueError(f"Aucune statistique trouvée avec l'ID {id_statistique}.")
        self.dao.delete_statistique(id_statistique)
        return f"Statistique avec l'ID {id_statistique} supprimée avec succès."

    def lister_statistiques(self):
        statistiques = self.dao.list_statistiques()
        if not statistiques:
            return "Aucune statistique disponible."
        return statistiques

    def obtenir_statistiques_equipe(self, equipe):
        result = self.dao.statistique_equipe(equipe)
        if not result:
            return f"Aucune statistique trouvée pour l'équipe {equipe}."
        return {"equipe": result[0], "total_buts": result[1], "total_scores": result[2]}

    def obtenir_statistiques_match(self, match):
        result = self.dao.statistique_match(match)
        if not result:
            return f"Aucune statistique trouvée pour le match {match}."
        return [{"match": r[0], "total_buts": r[1], "total_scores": r[2]} for r in result]

    def obtenir_statistiques_joueur(self, joueur):
        result = self.dao.statistique_joueur(joueur)
        if not result:
            return f"Aucune statistique trouvée pour le joueur {joueur}."
        return {"joueur": result[0], "total_buts": result[1], "total_scores": result[2]}
