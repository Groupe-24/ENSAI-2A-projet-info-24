print("a")
from InquirerPy import inquirer

print("b")
from abstract_view.vue_abstraite import VueAbstraite

print("c")


class VisiteurVue(VueAbstraite):
    """Vue des visiteurs non authentifiés"""

    print("12")

    def choix_visiteur(self):
        print("\n" + "-" * 50 + "\VisiteurVue\n" + "-" * 50 + "\n")

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
