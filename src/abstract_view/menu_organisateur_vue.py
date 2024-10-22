from InquirerPy import inquirer


from abstract_view.vue_abstraite import VueAbstraite


class MenuOrganisateurVue(VueAbstraite):
    """Menu des organisateurs"""

    def choisir_menu(self):
        print("\n" + "-" * 25 + "\Vue organisateur\n" + "-" * 25 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Ajouter des informations à un match",
                "Modifier les informations d'un match",
                "Créer un tournoi",
                "Quitter",
            ],
        ).execute()

        match choix:
            case "Quitter":
                pass

            case "Ajouter des informations à un match":
                pass

            case "Modifier les informations d'un match":
                pass

            case "Créer un tournoi":
                from abstract_view.creer_tournoi_vue import CreationTournoiVue

                return CreationTournoiVue("Création de tournoi")
