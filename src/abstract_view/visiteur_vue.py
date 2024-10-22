print("a")
from InquirerPy import inquirer

print("b")
from abstract_view.vue_abstraite import VueAbstraite

print("c")


class VisiteurVue(VueAbstraite):
    """Vue des visiteurs non authentifiés"""

    print("12")

    def choisir_menu(self):
        print("\n" + "-" * 25 + "\VisiteurVue\n" + "-" * 25 + "\n")

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

        from abstract_view.accueil_vue import AccueilVue

        return AccueilVue(message)
