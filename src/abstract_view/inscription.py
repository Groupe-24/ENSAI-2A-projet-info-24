from InquirerPy import inquirer

from InquirerPy.validator import PasswordValidator, EmptyInputValidator

from prompt_toolkit.validation import ValidationError, Validator

from abstract_view.vue_abstraite import VueAbstraite


class InscriptionVue(VueAbstraite):

    def choisir_menu(self):
        # Demande à l'utilisateur de saisir pseudo, mot de passe...
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()
        if JoueurService().pseudo_deja_utilise(pseudo):
            from abstract_view.accueil_vue import AccueilVue

            return AccueilVue(f"Le pseudo {pseudo} est déjà utilisé.")

        mdp = inquirer.secret(
            message="Entrez votre mot de passe : ",
            validate=PasswordValidator(
                length=8,
                cap=True,
                number=True,
                message="Au moins 8 caractères, incluant une majuscule et un chiffre",
            ),
        ).execute()

        equipe = inquirer.text(message="De quelle équipe faites vous partie ?")

        professionnel = inquirer.confirm(
            message="Êtes vous un joueur professionnel ? : ",
            confirm_letter="o",
            reject_letter="n",
        ).execute()

        # Appel du service pour créer le joueur
        joueur = JoueurService().creer(pseudo, mdp, equipe, professionnel)

        # Si le joueur a été créé
        if joueur:
            message = (
                f"Votre compte {joueur.pseudo} a été créé. Vous pouvez maintenant vous connecter."
            )
        else:
            message = "Erreur de connexion (pseudo ou mot de passe invalide)"

        from abstract_view.accueil_vue import AccueilVue

        return AccueilVue(message)
