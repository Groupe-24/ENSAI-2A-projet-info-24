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
                "Quitter",
            ],
        ).execute()
        match choix:
            case "Quitter":
                pass

            case "Se connecter":
                from view.accueil.connexion_vue import ConnexionVue

                return ConnexionVue("Connexion à l'application")
