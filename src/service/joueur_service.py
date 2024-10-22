from dao.joueur_dao import JoueursDao
from business_oject.joueur import Joueur


class JoueurService:
    def __init__(self, joueur_dao):
        self.joueur_dao = joueur_dao

    def rechercher_joueur(self, pseudo):
        """Rechercher un joueur par son pseudo

        Parameters
        ----------
        pseudo : str
            Pseudo du joueur à chercher

        Return
        ------
        list[Joueur]
        """
        resultat = self.joueur_dao.get_joueur_by_parameters(pseudo=pseudo)
        liste_joueur = []
        if resultat:
            for un_joueur in resultat:
                joueur = Joueur(
                    id_joueur=un_joueur["id_joueurs"],
                    pseudo=un_joueur["pseudo"],
                    equipe=un_joueur["equipe"],
                    professionnel=un_joueur["professionnel"],
                )
                liste_joueur.append(joueur)
        return liste_joueur
