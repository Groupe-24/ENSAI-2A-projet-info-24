from business_object.users.utilisateur import Utilisateur


class UtilisateurService:
    def __init__(self, utilisateurDao):
        self.utilisateurDao = utilisateurDao

    def creer_compte(self, pseudo, nom, mail, ddn, mdp):
        utilisateur = Utilisateur(pseudo, nom, mail, ddn, mdp, False, False)
        self.utilisateurDao.insert_utilisateur(pseudo, nom, mail, ddn, mdp)
        return utilisateur

    def se_connecter_utilisateur(self, pseudo, mdp):
        utili = self.utilisateurDao.get_utilisateur_by_id(pseudo)
        if utili and utili == pseudo:
            return utili.mdp == mdp
        return False

    def supprimer_utilisateur(self, utilisateur):
        return self.utilisateurDao.delete_utilisateur(utilisateur.pseudo)

    def se_connecter_administrateur(self, pseudo, mdp):
        utili = self.utilisateurDao.get_utilisateur_by_id(pseudo)
        if utili and utili.administrateur:
            if utili.pseudo == pseudo:
                return utili.mdp == mdp
        return False

    def se_connecter_organisateur(self, pseudo, mdp):
        utili = self.utilisateurDao.get_utilisateur_by_id(pseudo)
        if utili.organisateur:
            if utili.pseudo == pseudo:
                return utili.mdp == mdp
        return False

    def connection_ok(self, pseudo, mdp):
        utili = self.utilisateurDao.get_utilisateur_by_id(pseudo)
        if utili is None:
            return False
        return (
            self.se_connecter_utilisateur(pseudo, mdp)
            or self.se_connecter_administrateur(pseudo, mdp)
            or self.se_connecter_organisateur(pseudo, mdp)
        )
