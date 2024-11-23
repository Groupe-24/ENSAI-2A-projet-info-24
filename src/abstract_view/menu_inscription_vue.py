from InquirerPy import inquirer
from service.match_service import MatchService
from abstract_view.vue_abstraite import VueAbstraite
from dao.match_dao import MatchDAO
from abstract_view.menu_gestion_tournoi_vu import MenuGestionTournoiVue
from dao.joueur_dao import JoueursDAO
from dao.equipe_dao import EquipeDAO
from service.joueur_service import JoueurService
from business_object.users.joueur import Joueur
from business_object.users.utilisateur import Utilisateur
from dao.utilisateur_dao import UtilisateurDAO
from uuid import uuid4
from service.tournoi_service import TournoiService
from dao.tournoi_dao import TournoiDAO


class MenuInscriptionVue(VueAbstraite):
    """Menu des organisateurs"""

    def __init__(self, message="", utilisateur=None):
        super().__init__(message)
        self.utilisateur = utilisateur

    def choisir_menu(self):
        print("\n" + "-" * 25 + "\nVue organisateur\n" + "-" * 25 + "\n")

        choix = inquirer.select(
            message="Que voulez vous faire ?",
            choices=[
                "Inscrire mon équipe à un tournoi",
                "Créer une équipe",
                "Consulter les tournois",
                "Quitter",
            ],
        ).execute()

        match choix:
            case "Quitter":
                pass

            case "Inscrire mon équipe à un tournoi":
                id_joueur = UtilisateurDAO().get_utilisateur_by_id(self.utilisateur.id)["id_joueur"]
                if id_joueur is None:
                    print("Vous devez d'abord créer une équipe")
                    return MenuInscriptionVue(message=self.message, utilisateur=self.utilisateur)
                else:
                    Joueur
                    tournoi_pseudo = inquirer.text(
                        message="Saisir le nom du tournoi au quel vous voulez vous inscrire:"
                    ).execute()
                    nom_equipe = EquipeDAO().get_equipe_by_id(
                        JoueursDAO().get_joueur_by_id(id_joueur=id_joueur)["equipe"]
                    )["nom"]
                    TournoiService(TournoiDAO()).ajout_equipe(
                        tournoi_titre=tournoi_pseudo, nom_equipe=nom_equipe
                    )
                    print("vous êtes bien inscrit")
                    return MenuInscriptionVue(message=self.message, utilisateur=self.utilisateur)

            case "Créer une équipe":
                id_joueur = UtilisateurDAO().get_utilisateur_by_id(self.utilisateur.id)["id_joueur"]
                if id_joueur is None:
                    id_joueur = str(uuid4())
                    JoueursDAO().insert_joueur(id_joueur=id_joueur, pseudo=self.utilisateur.pseudo)
                    UtilisateurDAO().update_utilisateur(
                        id_utilisateur=self.utilisateur.id, id_joueur=id_joueur
                    )
                nom_equipe = inquirer.text(
                    message="Saisir le nom de votre nouvelle équipe"
                ).execute()
                if EquipeDAO().is_in_equipe_by_name(nom_equipe):
                    print("nom déjà prit choisissez en un autre")
                    while EquipeDAO().is_in_equipe_by_name(nom_equipe):
                        nom_equipe = inquirer.text(
                            message="Saisir le nom de votre nouvelle équipe"
                        ).execute()
                EquipeDAO().insert_equipe(nom=nom_equipe)
                id_equipe = EquipeDAO().get_equipe_by_nom(nom_equipe)["id_equipe"]
                JoueursDAO().update_joueur(id_joueur=id_joueur, equipe=id_equipe)
                print("equipe bien ajoutée")
                return MenuInscriptionVue(message=self.message, utilisateur=self.utilisateur)

            case "Consulter les tournois":
                print(TournoiService(TournoiDAO()).lister_tournois)
                return MenuInscriptionVue(message=self.message, utilisateur=self.utilisateur)
