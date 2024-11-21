from InquirerPy import inquirer
from service.utilisateur_service import UtilisateurService
from abstract_view.vue_abstraite import VueAbstraite
from dao.utilisateur_dao import UtilisateurDAO
from dao.tournoi_dao import TournoiDAO
from service.tournoi_service import TournoiService


class MenuAdministrateurVue(VueAbstraite):
    """Menu des administrateurs"""

    def choisir_menu(self):
        print("\n" + "-" * 25 + "\nVue administrateur\n" + "-" * 25 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Supprimer un utilisateur",
                "Supprimer un tournoi",
                "Quitter",
            ],
        ).execute()

        match choix:
            case "Quitter":
                pass

            case "Supprimer un utilisateur":

                pseudo = inquirer.text(
                    message="Entrez le pseudo du joueur à supprimer : "
                ).execute()

                if UtilisateurService(UtilisateurDAO()).pseudo_exist(pseudo):
                    UtilisateurService(UtilisateurDAO()).supprimer_utilisateur_by_pseudo(pseudo)

                    message = "L'utilisateur à été supprimé avec succès"

                    return MenuAdministrateurVue(message)
                else:
                    message = "L'utilisateur que vous voulez supprimer n'existe pas"

                    return MenuAdministrateurVue(message)

            case "Supprimer un tournoi":
                titre = inquirer.text(message="Entrez le titre du tournoi à supprimer : ").execute()

                print(TournoiService(TournoiDAO()).rechercher_tournoi_titre(nom=titre))

                id = inquirer.text(
                    message="Entrez l'identifiant du tournoi (voir ci dessus) : "
                ).execute()

                TournoiService(TournoiDAO()).supprimer_tournoi(id=id)

                return MenuAdministrateurVue(message)
