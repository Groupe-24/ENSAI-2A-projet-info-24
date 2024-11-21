from business_object.users.utilisateur import Utilisateur


class UtilisateurService:

    def __init__(self, utilisateurDao):
        self.utilisateurDao = utilisateurDao

    def creer_compte(self, pseudo, id, mail, ddn, mdp, administrateur, organisateur):
        utilisateur = Utilisateur(pseudo, id, mail, ddn, mdp, administrateur, organisateur)
        self.utilisateurDao.insert_utilisateur(
            id_utilisateur=id,
            pseudo=pseudo,
            email=mail,
            password=mdp,
            id_joueur=None,
            administrateur=administrateur,
            organisateur=organisateur,
            date_de_naissance=ddn,
        )
        return utilisateur

    def se_connecter_utilisateur(self, pseudo, mdp):

        utili = self.utilisateurDao.get_utilisateur_by_parameters(pseudo=pseudo)
        if utili is not None and len(utili) > 0 and utili[0]["pseudo"] == pseudo:
            return utili[0]["password"] == mdp

        return False

    def supprimer_utilisateur(self, utilisateur):
        return self.utilisateurDao.delete_utilisateur(utilisateur.pseudo)

    def supprimer_utilisateur_by_pseudo(self, pseudo):
        return self.utilisateurDao.delete_utilisateur(pseudo)

    def se_connecter_administrateur(self, pseudo, mdp):
        utili = self.utilisateurDao.get_utilisateur_by_parameters(pseudo=pseudo)
        if utili[0]["administrateur"]:
            if utili[0]["pseudo"] == pseudo:
                return utili[0]["password"] == mdp
        return False

    def se_connecter_organisateur(self, pseudo, mdp):
        utili = self.utilisateurDao.get_utilisateur_by_parameters(pseudo=pseudo)
        if utili[0]["organisateur"]:
            if utili[0]["pseudo"] == pseudo:
                return utili[0]["password"] == mdp
        return False

    def connection_ok(self, pseudo, mdp):
        utili = self.utilisateurDao.get_utilisateur_by_parameters(pseudo=pseudo)
        if utili == []:
            return False
        return (
            self.se_connecter_utilisateur(pseudo, mdp)
            or self.se_connecter_administrateur(pseudo, mdp)
            or self.se_connecter_organisateur(pseudo, mdp)
        )

    def pseudo_exist(self, pseudo):
        return self.utilisateurDao.get_utilisateur_by_parameters(pseudo=pseudo) != []

    def return_utilisateur(self, pseudo):
        return self.utilisateurDao.get_utilisateur_by_parameters(pseudo=pseudo)
