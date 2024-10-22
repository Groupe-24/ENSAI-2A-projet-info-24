from InquirerPy import inquirer


from abstract_view.vue_abstraite import VueAbstraite


class MenuAdministrateurVue(VueAbstraite):
    """Menu des administrateurs"""

    def choisir_menu(self):
        print("\n" + "-" * 25 + "\Vue administrateur\n" + "-" * 25 + "\n")

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
                pass

            case "Supprimer un tournoi":
                pass
