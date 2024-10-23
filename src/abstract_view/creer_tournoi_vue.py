from InquirerPy import inquirer


from abstract_view.vue_abstraite import VueAbstraite


class CreationTournoiVue(VueAbstraite):
    """Menu de la création des tournois"""

    def choisir_menu(self):
        print("\n" + "-" * 25 + "\nVue création tournoi\n" + "-" * 25 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Ajouter une équipe",
                "Définir le calendrier",
                "Quitter",
            ],
        ).execute()

        match choix:
            case "Quitter":
                pass

            case "Ajouter une équipe":
                pass

            case "Définir le calendrier":
                pass
