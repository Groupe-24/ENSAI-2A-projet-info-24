from InquirerPy import inquirer
from InquirerPy.validator import PasswordValidator, EmptyInputValidator
from dao.match_dao import MatchDAO
from service.match_service import MatchService
from abstract_view.vue_abstraite import VueAbstraite
from dao.statistique_dao import StatistiquesDAO
from service.statistique_service import StatistiqueService


class MenuStatistiqueVue(VueAbstraite):
    """Menu des utilisateurs authentifiés"""

    def choisir_menu(self):
        print("\n" + "-" * 25 + "\nVue utilisateur\n" + "-" * 25 + "\n")

        choix = inquirer.select(
            message="choisissez les statistiques qui vous intéresse : ",
            choices=[
                "Statistique d'un Joueur",
                "Statistique d'un Match",
                "Statistique d'une Equipe",
                "Quitter",
            ],
        ).execute()

        match choix:
            case "Quitter":
                pass

            case "Statistique d'un Joueur":
                joueur = inquirer.text(
                    message="Quel Joueur vous voulez regarder les statistiques ?",
                    validate=EmptyInputValidator(message="Veuillez rentrer un joueur"),
                ).execute()
                print(StatistiqueService(StatistiquesDAO()).obtenir_list_stat(joueur=joueur))

            case "Statistique d'un Match":
                print("Choisissez les deux équipes des matches que vous souhaitez")
                equipe_orange = inquirer.text(
                    message="equipe orange ?",
                    validate=EmptyInputValidator(message="Veuillez rentrer une equipe"),
                ).execute()
                equipe_bleu = inquirer.text(
                    message="equipe bleu ?",
                    validate=EmptyInputValidator(message="Veuillez rentrer une equipe"),
                ).execute()
                print(
                    StatistiqueService(StatistiquesDAO()).obtenir_list_stat(
                        equipe1=equipe_orange, equipe2=equipe_bleu
                    )
                )

            case "Statistique d'une Equipe":
                equipe_orange = inquirer.text(
                    message="Quelle equipe ?",
                    validate=EmptyInputValidator(message="Veuillez rentrer une equipe"),
                ).execute()
                print(
                    StatistiqueService(StatistiquesDAO()).obtenir_list_stat(equipe1=equipe_orange)
                )
