from InquirerPy import inquirer
from service.match_service import MatchService
from abstract_view.vue_abstraite import VueAbstraite
from dao.match_dao import MatchDAO
from abstract_view.menu_gestion_tournoi_vu import MenuGestionTournoiVue


class MenuOrganisateurVue(VueAbstraite):
    """Menu des organisateurs"""

    def choisir_menu(self):
        print("\n" + "-" * 25 + "\nVue organisateur\n" + "-" * 25 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Modifier les informations d'un match",
                "Créer un tournoi",
                "Gestion d'un tournoi",
                "Quitter",
            ],
        ).execute()

        match choix:
            case "Quitter":
                pass

            case "Modifier les informations d'un match":
                print("Voici le calendrier des matchs")
                MatchService(MatchDAO()).afficher_calendrier()

                match = inquirer.text(message="Saisir l'id du match à modifier : ").execute()

                choix1 = inquirer.select(
                    message="Que voulez vous modifier : ",
                    choices=[
                        "Date",
                        "Id_tournoi",
                        "Nom équipe orange",
                        "Nom équipe bleu",
                        "Retour",
                    ],
                ).execute()

                match choix1:
                    case "Date":
                        Date = inquirer.text(
                            message="Saisir la nouvelle date du match : "
                        ).execute()
                        MatchService(MatchDAO()).modifier_match(id_match=match, date=Date)
                        return MenuOrganisateurVue("Retour au Menu Organisateur")

                    case "Id_tournoi":
                        Id_tournoi = inquirer.text(
                            message="Saisir le nouveau id du tournoi : "
                        ).execute()
                        MatchService(MatchDAO()).modifier_match(
                            id_match=match, id_tournoi=Id_tournoi
                        )
                        return MenuOrganisateurVue("Retour au Menu Organisateur")

                    case "Nom équipe orange":
                        Nom_orange = inquirer.text(
                            message="Saisir le nom de l'équipe orange : "
                        ).execute()
                        MatchService(MatchDAO()).modifier_match(
                            id_match=match, equipe_orange=Nom_orange
                        )
                        return MenuOrganisateurVue("Retour au Menu Organisateur")

                    case "Nom équipe bleu":
                        Nom_bleu = inquirer.text(
                            message="Saisir le nom de l'équipe bleu : "
                        ).execute()
                        MatchService(MatchDAO()).modifier_match(
                            id_match=match, equipe_bleu=Nom_bleu
                        )
                        return MenuOrganisateurVue("Retour au Menu Organisateur")

                    case "Retour":
                        return MenuOrganisateurVue("Retour au Menu Organisateur")

            case "Créer un tournoi":
                from abstract_view.creer_tournoi_vue import CreationTournoiVue

                return CreationTournoiVue("Création de tournoi")

            case "Gestion d'un tournoi":
                pseudo_tournoi = inquirer.text(message="Saisir le nom du tournoi : ").execute()
                return MenuGestionTournoiVue(message="aaaaah", pseudo_tournoi=pseudo_tournoi)
