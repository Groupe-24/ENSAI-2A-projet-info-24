from InquirerPy import inquirer
from dao.match_dao import MatchDAO
from service.match_service import MatchService
from abstract_view.vue_abstraite import VueAbstraite
from dao.statistique_dao import StatistiquesDAO
from service.statistique_service import StatistiqueService
from abstract_view.menu_statistique_vue import MenuStatistiqueVue


class MenuUtilisateurVue(VueAbstraite):
    """Menu des utilisateurs authentifiés"""

    def choisir_menu(self):
        print("\n" + "-" * 25 + "\nVue utilisateur\n" + "-" * 25 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Consulter le Calendrier",
                "Consulter les statistiques",
                "S'inscrire à un tournoi",
                "Parier sur des matchs",
                "Quitter",
            ],
        ).execute()

        match choix:
            case "Quitter":
                pass

            case "Consulter le Calendrier":
                MatchService(MatchDAO()).afficher_calendrier()

            case "Consulter les statistiques":
                return MenuStatistiqueVue()

            case "S'inscrire à un tournoi":
                pass

            case "Parier sur des matchs":
                pass
