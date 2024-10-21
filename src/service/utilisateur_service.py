from business_object.users.utilisateur import Utilisateur
from dao.utilisateur_dao import UtilisateurDAO


class UtilisateurService:

    def creer_compte(self, id, nom, mail, ddn, mdp):
        utilisateur = Utilisateur(id, nom, mail, ddn, mdp, False, False)
        UtilisateurDAO.ajouter_utilisateur(id)
        return utilisateur

    def se_connecter_utilisateur(self, id, mdp):
        utili = UtilisateurDAO.obtenir_utilisateur(id)
        if utili.id == id:
            return utili.mdp == mdp
        return False
