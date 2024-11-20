from InquirerPy import inquirer
from service.tournoi_service import TournoiService
from abstract_view.vue_abstraite import VueAbstraite
from dao.tournoi_dao import TournoiDAO
from dao.utilisateur_dao import UtilisateurDAO
from service.utilisateur_service import UtilisateurService


class CreationTournoiVue(VueAbstraite):
    """Menu de la création des tournois"""

    def choisir_menu(self):
        print("\n" + "-" * 25 + "\nVue création tournoi\n" + "-" * 25 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Créer un tournoi",
                "Voir les tournois",
                "Chercher un tournoi par nom",
                "Quitter",
            ],
        ).execute()

        match choix:
            case "Quitter":
                pass

            case "Créer un tournoi":
                Pseudo_orga = inquirer.text(message="Veuillez saisir votre pseudo").execute()
                Titre = inquirer.text(message="Saisir le titre du tournoi : ").execute()
                Description = inquirer.text(message="Saisir la description du tournoi : ").execute()
                Date_debut = inquirer.text(
                    message="Saisir la date de début du tournoi : "
                ).execute()
                Date_fin = inquirer.text(message="Saisir la date de fin du tournoi : ").execute()
                Organisateur = UtilisateurService(UtilisateurDAO()).return_utilisateur(
                    pseudo=Pseudo_orga
                )
                print(Organisateur)
                TournoiService(TournoiDAO()).creer_tournoi(
                    titre=Titre,
                    description=Description,
                    date_debut=Date_debut,
                    date_fin=Date_fin,
                    organisateur=Organisateur[0],
                )

            case "Voir les tournois":
                pass

            case "Chercher un tournoi par nom":
                pass
