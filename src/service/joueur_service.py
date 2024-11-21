from business_object.users.joueur import Joueur


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

    def creer_joueur(self, id_joueur, pseudo, equipe, professionnel):
        """Créer un joueur

        Parameters
        ----------
        id_joueur: str
            ID du nouveau joueur
        pseudo: str
            Pseudo du joueur
        equipe: str
            Nom de l'équipe du joueur
        professionnel: bool
            True si le joueur est un professionnel, False sinon
        """
        if self.joueur_dao.exists_by_id(id_joueur):
            raise ValueError(f"Un joueur avec l'ID {id_joueur} existe déjà.")

        if self.joueur_dao.get_joueur_by_parameters(pseudo=pseudo):
            raise ValueError(f"Un joueur avec le pseudo '{pseudo}' existe déjà.")

        self.joueur_dao.insert_joueur(
            id_joueur=id_joueur, pseudo=pseudo, equipe=equipe, professionnel=professionnel
        )
        return f"Le joueur '{pseudo}' a été créé avec succès."

    def supprimer_joueur(self, id_joueur):
        """Supprimer un joueur

        Parameters
        ----------
        id_joueur: str
            ID du joueur à supprimer
        """
        if not self.joueur_dao.exists_by_id(id_joueur):
            raise ValueError(f"Le joueur avec l'ID {id_joueur} n'existe pas.")
        self.joueur_dao.delete_joueur(id_joueur)
        return f"Le joueur avec l'ID {id_joueur} a été supprimé avec succès."
