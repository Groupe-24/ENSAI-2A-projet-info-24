from InquirerPy import inquirer

from abstract_view.vue_abstraite import VueAbstraite


class AccueilVue(VueAbstraite):
    """Vue d'accueil de l'application"""

    def choisir_menu(self):
        """Choix du menu suivant

        Return
        ------
        view
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nAccueil\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Se connecter",
                "Créer un compte",
                "Consulter le calendrier et les statistiques",
                "Quitter",
            ],
        ).execute()
        match choix:
            case "Quitter":
                pass

            case "Se connecter":
                from abstract_view.connexion import ConnexionVue

                return ConnexionVue("Connexion à l'application")

            case "Créer un compte":
                from abstract_view.inscription import InscriptionVue

                return InscriptionVue("Inscription à l'application")

            case "Consulter le calendrier et les statistiques":
                from abstract_view.menu_visiteur_vue import VisiteurVue

                return VisiteurVue("Que souhaitez vous faire ?")
