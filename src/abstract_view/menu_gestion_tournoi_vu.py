from InquirerPy import inquirer
from service.utilisateur_service import UtilisateurService
from abstract_view.vue_abstraite import VueAbstraite
from dao.utilisateur_dao import UtilisateurDAO
from dao.tournoi_dao import TournoiDAO
from dao.statistique_dao import StatistiquesDAO
from dao.equipe_dao import EquipeDAO
from dao.joueur_dao import JoueursDAO
from dao.match_dao import MatchDAO

from service.tournoi_service import TournoiService
from abc import *


class MenuGestionTournoiVue(VueAbstraite):
    """Menu Gestion de Tournoi"""

    def __init__(self, message="", pseudo_tournoi=None):
        super().__init__(message)
        self.pseudo_tournoi = pseudo_tournoi

    def choisir_menu(self):
        print("\n" + "-" * 25 + "\nVue administrateur\n" + "-" * 25 + "\n")

        id_tournoi = TournoiDAO().get_tournoi_by_titre(titre=self.pseudo_tournoi)[0]["id_tournois"]
        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Rajouter une Statistique",
                "Rajouter un Match associé au Tournoi",
                "Modifier les informations d'un Tournoi",
                "Quitter",
            ],
        ).execute()

        match choix:
            case "Quitter":
                pass

            case "Rajouter une Statistique":

                nom_equipe_orange = inquirer.text(
                    message="Entrez l'équipe orange du match"
                ).execute()
                id_equipe_orange = EquipeDAO().get_equipe_by_nom(nom_equipe_orange)["id_equipe"]

                nom_equipe_bleu = inquirer.text(message="Entrez l'équipe bleu du match").execute()
                id_equipe_bleu = EquipeDAO().get_equipe_by_nom(nom_equipe_bleu)["id_equipe"]
                # faire attention au message d'erreur si le match n'est pas encore créer
                pseudo_joueur = inquirer.text(message="Entrez le pseudo du joueur").execute()
                id_joueur = JoueursDAO().get_joueur_by_pseudo(pseudo_joueur)["id_joueurs"]
                # faire attention si le joueur est bien dans une des 2 equipes

                choix = inquirer.select(
                    message="Equipe du Joueur: ",
                    choices=[
                        "Bleu",
                        "Orange",
                    ],
                ).execute()
                match choix:
                    case "Bleu":
                        id_equipe = id_equipe_bleu
                    case "Orange":
                        id_equipe = id_equipe_orange

                goals = inquirer.text(message="Entrez le nombre de but du joueur").execute()

                shots = inquirer.text(message="Entrez le nombre de tire du joueur").execute()

                save = inquirer.text(message="Entrez le nombre de save du joueur").execute()

                assists = inquirer.text(message="Entrez le nombre d'assist du joueur").execute()

                score = inquirer.text(message="Entrez le score du joueur").execute()

                match_id = MatchDAO().get_match_by_parameters(
                    id_tournoi=id_tournoi,
                    equipe_bleu=id_equipe_bleu,
                    equipe_orange=id_equipe_orange,
                )[0]["id_matches"]
                StatistiquesDAO().insert_statistique(
                    equipe=id_equipe,
                    joueur=id_joueur,
                    match=match_id,
                    assists=assists,
                    saves=save,
                    score=score,
                    shots=shots,
                    goals=goals,
                )
                return MenuGestionTournoiVue(pseudo_tournoi=self.pseudo_tournoi)

            case "Rajouter un Match associé au Tournoi":
                nom_equipe_orange = inquirer.text(
                    message="Entrez l'équipe orange du match"
                ).execute()
                id_equipe_orange = EquipeDAO().get_equipe_by_nom(nom_equipe_orange)["id_equipe"]

                nom_equipe_bleu = inquirer.text(message="Entrez l'équipe bleu du match").execute()
                id_equipe_bleu = EquipeDAO().get_equipe_by_nom(nom_equipe_bleu)["id_equipe"]
                date = inquirer.text(message="Entrez la date du match (JJ/MM/AAAA)").execute()

                MatchDAO().insert_match(
                    id_tournoi=id_tournoi,
                    equipe_orange=id_equipe_orange,
                    equipe_bleu=id_equipe_bleu,
                    date=date,
                )
                return MenuGestionTournoiVue(pseudo_tournoi=self.pseudo_tournoi)

            case "Modifier les informations d'un Tournoi":
                pass
