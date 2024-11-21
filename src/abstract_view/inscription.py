from InquirerPy import inquirer

from InquirerPy.validator import PasswordValidator, EmptyInputValidator

from abstract_view.vue_abstraite import VueAbstraite

from service.utilisateur_service import UtilisateurService

from dao.utilisateur_dao import UtilisateurDAO


class InscriptionVue(VueAbstraite):

    def choisir_menu(self):
        # Demande à l'utilisateur de saisir pseudo, mot de passe...
        pseudo = inquirer.text(
            message="Entrez votre pseudo : ",
            validate=EmptyInputValidator(message="Veuillez rentrer un pseudo"),
        ).execute()
        if UtilisateurService(UtilisateurDAO()).pseudo_exist(pseudo=pseudo):
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

        mail = inquirer.text(
            message="Quel est votre mail ?",
            validate=EmptyInputValidator(message="Veuillez rentrer un mail"),
        ).execute()

        date_naissance = inquirer.text(
            message="Quel est votre date de naissance ?",
            validate=EmptyInputValidator(message="Veuillez rentrer une date de naissance"),
        ).execute()

        admin = inquirer.confirm(
            message="Êtes vous un administrateur ? : ",
            confirm_letter="o",
            reject_letter="n",
        ).execute()

        orga = inquirer.confirm(
            message="Êtes vous un organisateur ? : ",
            confirm_letter="o",
            reject_letter="n",
        ).execute()

        # Appel du service pour créer l'utilisateur
        utilisateur = UtilisateurService(UtilisateurDAO()).creer_compte(
            pseudo=pseudo,
            id=None,
            mail=mail,
            ddn=date_naissance,
            mdp=mdp,
            administrateur=admin,
            organisateur=orga,
        )

        # Si l'Utilisateur a été créé
        if UtilisateurService(UtilisateurDAO()).pseudo_exist(pseudo=pseudo):
            message = f"Votre compte {utilisateur.pseudo} a été créé. Vous pouvez maintenant vous connecter."
        else:
            message = "Erreur de connexion (pseudo ou mot de passe invalide)"

        from abstract_view.accueil_vue import AccueilVue

        return AccueilVue(message)
