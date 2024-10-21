from business_object.users.utilisateur import Utilisateur
from dao.utilisateur_dao import UtilisateurDAO


class UtilisateurService:

    def creer_compte(self, pseudo, nom, mail, ddn, mdp):
        utilisateur = Utilisateur(pseudo, nom, mail, ddn, mdp, False, False)
        UtilisateurDAO.insert_utilisateur(pseudo, nom, mail, ddn, mdp)
        return utilisateur

    def se_connecter_utilisateur(self, pseudo, mdp):
        utili = UtilisateurDAO.get_utilisateur_by_id(pseudo)
        if utili.pseudo == pseudo:
            return utili.mdp == mdp
        return False

    def supprimer_utilisateur(self, utilisateur):
        return self.UtilisateurDAO.delete_utilisateur(utilisateur.pseudo)

    def se_connecter_administrateur(self, pseudo, mdp):
        utili = UtilisateurDAO.get_utilisateur_by_id(pseudo)
        if utili.administrateur:
            if utili.pseudo == pseudo:
                return utili.mdp == mdp
        return False

    def se_connecter_organisateur(self, pseudo, mdp):
        utili = UtilisateurDAO.get_utilisateur_by_id(pseudo)
        if utili.organisateur:
            if utili.pseudo == pseudo:
                return utili.mdp == mdp
        return False
