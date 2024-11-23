from InquirerPy import inquirer
from service.match_service import MatchService
from dao.match_dao import MatchDAO
from abstract_view.vue_abstraite import VueAbstraite
from abstract_view.menu_statistique_vue import MenuStatistiqueVue
from abstract_view.accueil_vue import AccueilVue


class VisiteurVue(VueAbstraite):
    """Vue des visiteurs non authentifiés"""

    def choisir_menu(self):
        print("\n" + "-" * 25 + "\nVisiteurVue\n" + "-" * 25 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Consulter le Calendrier",
                "Consulter les statistiques",
                "Quitter",
            ],
        ).execute()

        match choix:
            case "Quitter":
                return AccueilVue(message="retour au menu Connexion")

            case "Consulter le Calendrier":
                MatchService(MatchDAO()).afficher_calendrier()

            case "Consulter les statistiques":
                return MenuStatistiqueVue()
