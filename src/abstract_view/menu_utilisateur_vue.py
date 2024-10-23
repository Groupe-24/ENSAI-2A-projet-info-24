from InquirerPy import inquirer

from abstract_view.vue_abstraite import VueAbstraite


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
                pass

            case "Consulter les statistiques":
                pass

            case "S'inscrire à un tournoi":
                pass

            case "Parier sur des matchs":
                pass
