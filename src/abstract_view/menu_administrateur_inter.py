from InquirerPy import inquirer
from abstract_view.vue_abstraite import VueAbstraite
from abstract_view.menu_administrateur_vue import MenuAdministrateurVue
from abstract_view.menu_organisateur_vue import MenuOrganisateurVue
from abstract_view.menu_utilisateur_vue import MenuUtilisateurVue

# from service.joueur_service import JoueurService


class ConnexionAdminVue(VueAbstraite):

    def __init__(self, message="", utilisateur=None):
        super().__init__(message)
        self.utilisateur = utilisateur

    def choisir_menu(self):
        choix = inquirer.select(
            message="Choisissez dabs quel menu vous voulez rentrer : ",
            choices=[
                "Utilisateur",
                "Administrateur",
                "Organisateur",
                "Quitter",
            ],
        ).execute()

        match choix:
            case "Utilisateur":
                return MenuUtilisateurVue(self.message, utilisateur=self.utilisateur)
            case "Administrateur":
                return MenuAdministrateurVue(message=self.message)
            case "Organisateur":
                return MenuOrganisateurVue()
            case "Quitter":
                pass