from InquirerPy import inquirer

from service.utilisateur_service import UtilisateurService
from abstract_view.vue_abstraite import VueAbstraite
from dao.utilisateur_dao import UtilisateurDAO
from abstract_view.menu_organisateur_vue import MenuOrganisateurVue
from abstract_view.menu_utilisateur_vue import MenuUtilisateurVue
from business_object.users.utilisateur import Utilisateur
from utils.function import generer_hash
from abstract_view.menu_administrateur_inter import ConnexionAdminVue


class ConnexionVue(VueAbstraite):
    """Vue de Connexion (saisie de pseudo et mdp)"""

    def choisir_menu(self):
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()
        mdp = generer_hash(inquirer.secret(message="Entrez votre mot de passe :").execute())

        if UtilisateurService(UtilisateurDAO()).connection_ok(pseudo, mdp):
            message = f"Vous êtes connecté sous le pseudo {pseudo}"

            utilisateur = UtilisateurDAO().get_utilisateur_by_parameters(pseudo=pseudo)[0]
            user = Utilisateur(
                pseudo=pseudo,
                mail=utilisateur["email"],
                id=utilisateur["id_utilisateur"],
                ddn=utilisateur["date_de_naissance"],
                organisateur=utilisateur["organisateur"],
                administrateur=utilisateur["administrateur"],
            )
            if UtilisateurService(UtilisateurDAO()).se_connecter_administrateur(pseudo, mdp):

                return ConnexionAdminVue(message=message, utilisateur=user)

            if UtilisateurService(UtilisateurDAO()).se_connecter_organisateur(pseudo, mdp):

                return MenuOrganisateurVue(message)

            return MenuUtilisateurVue(message, utilisateur=user)

        message = "Erreur de connexion (pseudo ou mot de passe invalide)"
        from abstract_view.accueil_vue import AccueilVue

        return AccueilVue(message)
