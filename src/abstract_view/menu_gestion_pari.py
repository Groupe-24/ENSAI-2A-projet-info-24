from InquirerPy import inquirer
from abstract_view.vue_abstraite import VueAbstraite
from dao.tournoi_dao import TournoiDAO
from service.pari_service import PariService
from dao.pari_dao import ParisDAO


class MenuGestionPariVue(VueAbstraite):
    """Menu Gestion de Pari"""

    def __init__(self, message="", utilisateur=None, match=None):
        super().__init__(message)
        self.utilisateur = utilisateur
        self.match_pari = match

    def choisir_menu(self):
        print("\n" + "-" * 25 + "\nMenu Gestion de Pari\n" + "-" * 25 + "\n")

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
                        return MenuGestionPariVue(
                            utilisateur=self.utilisateur, match=self.match_pari
                        )
                    case "Non":
                        return MenuGestionPariVue(
                            utilisateur=self.utilisateur, match=self.match_pari
                        )
