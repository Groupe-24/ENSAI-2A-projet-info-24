from InquirerPy import inquirer
from service.utilisateur_service import UtilisateurService
from abstract_view.vue_abstraite import VueAbstraite
from dao.utilisateur_dao import UtilisateurDAO


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
                pass
