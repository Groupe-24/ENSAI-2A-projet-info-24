from InquirerPy import inquirer
from service.utilisateur_service import UtilisateurService
from abstract_view.vue_abstraite import VueAbstraite
from dao.utilisateur_dao import UtilisateurDAO
from dao.tournoi_dao import TournoiDAO
from dao.statistique_dao import StatistiquesDAO
from dao.equipe_dao import EquipeDAO
from dao.joueur_dao import JoueursDAO
from dao.match_dao import MatchDAO
from service.pari_service import PariService
from dao.pari_dao import ParisDAO
from business_object.match import Match
from business_object.equipe import Equipe
from business_object.users.utilisateur import Utilisateur

from service.tournoi_service import TournoiService
from abc import *


class MenuGestionPariVue(VueAbstraite):
    """Menu Gestion de Tournoi"""

    def __init__(self, message="", utilisateur=None, match=None):
        super().__init__(message)
        self.utilisateur = utilisateur
        self.match_pari = match

    def choisir_menu(self):
        print("\n" + "-" * 25 + "\nVue administrateur\n" + "-" * 25 + "\n")

        # utilisateur = UtilisateurDAO().get_utilisateur_by_parameters(
        #     pseudo=self.pseudo_utilisateur
        # )[0]
        # user = Utilisateur(
        #     pseudo=self.pseudo_utilisateur,
        #     mail=utilisateur["email"],
        #     id=utilisateur["id_utilisateur"],
        #     ddn=utilisateur["date_de_naissance"],
        #     organisateur=utilisateur["organisateur"],
        #     administrateur=utilisateur["administrateur"],
        # )
        # match_reel_dict = MatchDAO().get_match_by_id(id_match=self.id_match)
        # match_pari = Match(
        #     id_match=self.id_match,
        #     id_tournoi=match_reel_dict["id_tournois"],
        #     date=match_reel_dict["date"],
        #     equipe_bleu=match_reel_dict["equipe_bleu"],
        #     equipe_orange=match_reel_dict["equipe_orange"],
        # )
        dict_cote = PariService(pari_dao=ParisDAO()).afficher_cote(self.match_pari)
        nom_tournoi = TournoiDAO().get_tournoi_by_id(self.match_pari.id_tournoi)["titre"]
        print(
            "Tournoi: "
            + nom_tournoi
            + "\n Match: \n equipe bleu: "
            + self.match_pari.equipe_bleu.nom
            + " VS "
            + "equipe orange: "
            + self.match_pari.equipe_orange.nom
            + "\n"
            + "cote: "
            + str(dict_cote["cote_equipe_bleu"])
            + "/"
            + str(dict_cote["cote_equipe_orange"])
        )

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Parier sur un match",
                "Quitter",
            ],
        ).execute()

        match choix:
            case "Quitter":
                pass

            case "Parier sur un match":
                choix = inquirer.select(
                    message="Sur quelle équipe voulez vous pariez ?",
                    choices=[
                        "Equipe Bleu",
                        "Equipe Orange",
                    ],
                ).execute()
                match choix:
                    case "Equipe Bleu":
                        equipe_parier = self.match_pari.equipe_bleu
                    case "Equipe Orange":
                        equipe_parier = self.match_pari.equipe_orange
                qte_parie = inquirer.text(message="Combien voulez-vous pariez ?").execute()
                gain = PariService(ParisDAO()).gain_potentiel(
                    mise=qte_parie, equipe=equipe_parier, match=self.match_pari
                )
                print("gain:" + str(gain))
                choix = inquirer.select(
                    message="Voulez-vous parier ?",
                    choices=[
                        "Oui",
                        "Non",
                    ],
                ).execute()
                match choix:
                    case "Oui":
                        PariService(ParisDAO()).parier(
                            match=self.match_pari,
                            equipe=equipe_parier,
                            utilisateur=self.utilisateur,
                            mise=qte_parie,
                            gain=gain,
                        )
                    case "Non":
                        return MenuGestionPariVue(
                            utilisateur=self.utilisateur, match=self.match_pari
                        )
