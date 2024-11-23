from dao.joueur_dao import JoueursDAO
from dao.equipe_dao import EquipeDAO
from dao.match_dao import MatchDAO
from dao.statistique_dao import StatistiquesDAO
from dao.joueur_dao import JoueursDAO


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
            "equipe": result["equipe"],
            "total_goals": result["goals"],
            "total_score": result["score"],
            "total_assists": result["assists"],
            "total_saves": result["saves"],
            "total_shots": result["shots"],
        }

    def obtenir_statistiques_match(self, match):
        # Récupération des statistiques d'un match
        result = self.dao.statistique_match(match)
        if not result:
            return f"Aucune statistique trouvée pour le match {match}."
        return [
            {
                "match": r["match"],
                "total_goals": r["goals"],
                "total_score": r["score"],
                "total_assists": r["assists"],
                "total_saves": r["saves"],
                "total_shots": r["shots"],
            }
            for r in result
        ]

    def obtenir_statistiques_joueur(self, joueur):
        # Récupération des statistiques d'un joueur
        result = self.dao.statistique_joueur(joueur)
        if not result:
            return f"Aucune statistique trouvée pour le joueur {joueur}."
        return {
            "joueur": result["joueur"],
            "total_goals": result["goals"],
            "total_score": result["score"],
            "total_assists": result["assists"],
            "total_saves": result["saves"],
            "total_shots": result["shots"],
        }

    def obtenir_list_stat(self, joueur=None, equipe1=None, equipe2=None):
        if not (joueur is None):
            id_joueur = JoueursDAO().get_joueur_by_pseudo(joueur)["id_joueurs"]
            return self.dao.get_statistique_by_parameters(joueur=id_joueur)
        if (not (equipe1 is None)) and (equipe2 is None):
            id_equipe = EquipeDAO().get_equipe_by_nom(equipe1)["id_equipe"]
            return self.dao.get_statistique_by_parameters(equipe=id_equipe)
        if equipe2 is not None:
            id_equipe1 = EquipeDAO().get_equipe_by_nom(equipe1)["id_equipe"]
            id_equipe2 = EquipeDAO().get_equipe_by_nom(equipe2)["id_equipe"]
            id_matches = MatchDAO().get_match_by_parameters(
                equipe_bleu=id_equipe1, equipe_orange=id_equipe2
            )
            id_matches2 = MatchDAO().get_match_by_parameters(
                equipe_bleu=id_equipe2, equipe_orange=id_equipe1
            )
            list_matches = id_matches + id_matches2
            if bool(list_matches):
                statistiques_des_matches = []
                for match in list_matches:
                    statistiques_des_matches.append(
                        self.dao.get_statistique_by_parameters(match=match["id_matches"])
                    )
                return statistiques_des_matches
        else:
            return None

    def statistique_de_joueur(self, joueur=None):
        list_de_stat = self.obtenir_list_stat(joueur=joueur)
        sum_shots = 0
        sum_score = 0
        sum_goals = 0
        sum_assists = 0
        n = len(list_de_stat)
        nom_equipe = EquipeDAO().get_equipe_by_id(list_de_stat[0]["equipe"])["nom"]
        for stat in list_de_stat:
            sum_score += stat["score"]
            sum_assists += stat["assists"]
            sum_goals += stat["goals"]
            sum_shots += stat["shots"]
        dict_reponse = {
            "joueur": joueur,
            "equipe": nom_equipe,
            "moyenne du score": sum_score / n,
            "moyenne du nombre d'assists": sum_assists / n,
            "moyenne du nombre de shots": sum_shots / n,
            "nombre de but": sum_goals,
            "moyenne du nombre de but": sum_goals / n,
            "nombre de match joué": n,
        }
        return dict_reponse

    def statistique_equipe(self, equipe):
        list_stat = self.obtenir_list_stat(equipe1=equipe)
        sum_shots = 0
        sum_score = 0
        sum_goals = 0
        sum_assists = 0
        n = len(list_stat)
        for stat in list_stat:
            sum_score += stat["score"]
            sum_assists += stat["assists"]
            sum_goals += stat["goals"]
            sum_shots += stat["shots"]
        dict_reponse = {
            "equipe": equipe,
            "moyenne du score": sum_score / n,
            "moyenne du nombre d'assists": sum_assists / n,
            "moyenne du nombre de shots": sum_shots / n,
            "nombre de but": sum_goals,
            "moyenne du nombre de but": sum_goals / n,
            "nombre de match joué": n,
        }
        return dict_reponse

    def statistique_match(self, equipe1, equipe2):
        list_stat = self.obtenir_list_stat(equipe1=equipe1, equipe2=equipe2)
        list_stat = list_stat[0]
        list_match = [list_stat[0]["match"]]
        list_reponse = []
        l = []
        sum_goals_1 = 0
        sum_goals_2 = 0
        for stat in list_stat:
            if not stat["match"] in list_match:
                l.append({"score" + equipe1: sum_goals_1, "score" + equipe2: sum_goals_2})
                list_reponse.append(l)
                l = []
                sum_goals_1 = 0
                sum_goals_2 = 0
            dict_rep = {
                "joueur": JoueursDAO().get_joueur_by_id(stat["joueur"])["pseudo"],
                "equipe": EquipeDAO().get_equipe_by_id(stat["equipe"])["nom"],
                "score": stat["score"],
                "shots": stat["shots"],
                "goals": stat["goals"],
                "saves": stat["saves"],
            }
            l.append(dict_rep)
            if dict_rep["equipe"] == equipe1:
                sum_goals_1 += sum_goals_1 + dict_rep["goals"]
            else:
                sum_goals_2 += sum_goals_2 + dict_rep["goals"]
        l.append({"score " + equipe1: sum_goals_1, "score " + equipe2: sum_goals_2})
        list_reponse.append(l)
        l = []
        sum_goals_1 = 0
        sum_goals_2 = 0
        list_reponse.append({"nombre de rencontre": len(list_reponse)})
        return list_reponse
