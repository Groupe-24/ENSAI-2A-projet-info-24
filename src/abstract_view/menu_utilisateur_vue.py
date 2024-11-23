from InquirerPy import inquirer
from dao.match_dao import MatchDAO
from service.match_service import MatchService
from abstract_view.vue_abstraite import VueAbstraite
from abstract_view.menu_statistique_vue import MenuStatistiqueVue
from abstract_view.menu_gestion_pari import MenuGestionPariVue
from business_object.match import Match
from InquirerPy.validator import EmptyInputValidator
from dao.equipe_dao import EquipeDAO
from dao.tournoi_dao import TournoiDAO
from business_object.equipe import Equipe
from abstract_view.menu_inscription_vue import MenuInscriptionVue
from abstract_view.accueil_vue import AccueilVue


class MenuUtilisateurVue(VueAbstraite):
    """Menu des utilisateurs authentifiés"""

    def __init__(self, message="", utilisateur=None):
        super().__init__(message)
        self.utilisateur = utilisateur

    def choisir_menu(self):
        print("\n" + "-" * 25 + "\nVue utilisateur\n" + "-" * 25 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Consulter le Calendrier",
                "Consulter les statistiques",
                "Inscription",
                "Parier sur des matchs",
                "Quitter",
            ],
        ).execute()

        match choix:
            case "Quitter":
                return AccueilVue(message="retour au menu Connexion")

            case "Consulter le Calendrier":
                MatchService(MatchDAO()).afficher_calendrier()
                return MenuUtilisateurVue(
                    message="retour au Menu Utilisateur", utilisateur=self.utilisateur
                )

            case "Consulter les statistiques":
                return MenuStatistiqueVue()

            case "Inscription":
                return MenuInscriptionVue(message="", utilisateur=self.utilisateur)

            case "Parier sur des matchs":
                equipe_orange = inquirer.text(
                    message="equipe orange ?",
                    validate=EmptyInputValidator(message="Veuillez rentrer une equipe"),
                ).execute()
                equipe_bleu = inquirer.text(
                    message="equipe bleu ?",
                    validate=EmptyInputValidator(message="Veuillez rentrer une equipe"),
                ).execute()
                tournoi = inquirer.text(
                    message="tournoi ?",
                    validate=EmptyInputValidator(message="Veuillez rentrer une equipe"),
                ).execute()

                match_reel_dict = MatchDAO().get_match_by_parameters(
                    id_tournoi=TournoiDAO().get_tournoi_by_titre(tournoi)[0]["id_tournois"],
                    equipe_bleu=EquipeDAO().get_equipe_by_nom(equipe_bleu)["id_equipe"],
                    equipe_orange=EquipeDAO().get_equipe_by_nom(equipe_orange)["id_equipe"],
                )[0]
                id_equipe_bleu = match_reel_dict["equipe_bleu"]
                equipe_bleu_pari = Equipe(
                    nom=EquipeDAO().get_equipe_by_id(id_equipe_bleu)["nom"],
                    id_equipe=id_equipe_bleu,
                )
                id_equipe_orange = match_reel_dict["equipe_orange"]
                equipe_orange_pari = Equipe(
                    nom=EquipeDAO().get_equipe_by_id(id_equipe_orange)["nom"],
                    id_equipe=id_equipe_orange,
                )
                match_pari = Match(
                    id_match=match_reel_dict["id_matches"],
                    id_tournoi=match_reel_dict["id_tournois"],
                    date=match_reel_dict["date"],
                    equipe_bleu=equipe_bleu_pari,
                    equipe_orange=equipe_orange_pari,
                )
                return MenuGestionPariVue(utilisateur=self.utilisateur, match=match_pari)
