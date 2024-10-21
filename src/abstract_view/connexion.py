from InquirerPy import inquirer
from service.utilisateur_service import UtilisateurService
from abstract_view.vue_abstraite import VueAbstraite
from view.session import Session

from service.joueur_service import JoueurService


class ConnexionVue(VueAbstraite):
    """Vue de Connexion (saisie de pseudo et mdp)"""

    def choisir_menu(self):
        # Demande à l'utilisateur de saisir pseudo et mot de passe
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()
        mdp = inquirer.secret(message="Entrez votre mot de passe :").execute()

        # Appel du service pour trouver le joueur
        utilisateur = UtilisateurService().se_connecter(pseudo, mdp)

        # Si le joueur a été trouvé à partir des ses identifiants de connexion
        if joueur:
            message = f"Vous êtes connecté sous le pseudo {joueur.pseudo}"

            from abstract_view.menu_utilisateur_vue import MenuUtilisateurVue

            return MenuUtilisateurVue(message)

        message = "Erreur de connexion (pseudo ou mot de passe invalide)"
        from abstract_view.accueil_vue import AccueilVue

        return AccueilVue(message)
