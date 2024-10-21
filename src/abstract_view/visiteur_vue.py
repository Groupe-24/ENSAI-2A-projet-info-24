from InquirerPy import inquirer
from abstract_view.vue_abstraite import VueAbstraite


class VisiteurVue(VueAbstraite):
    """ """

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
