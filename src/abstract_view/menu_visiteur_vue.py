from InquirerPy import inquirer


from abstract_view.vue_abstraite import VueAbstraite


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
                pass

            case "Consulter le Calendrier":
                pass

            case "Consulter les statistiques":
                pass
