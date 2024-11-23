from business_object.users.utilisateur import Utilisateur


class UtilisateurService:
    def __init__(self, utilisateurDao):
        self.utilisateurDao = utilisateurDao

    def creer_compte(self, pseudo, id, mail, ddn, mdp, administrateur, organisateur):
        """Créer un compte utilisateur

        Parameters
        ----------
        pseudo: str
            Pseudo de l'utilisateur
        id: str
            ID de l'utilisateur
        mail: str
            Adresse mail de l'utilisateur
        administrateur: bool
            True si l'utilisateur est un administrateur, False sinon
        Organisateur: bool
            True si l'utilisateur est un organisateur, False sinon

        Return
        ------
        Utilisateur
        """
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
        """Connecter un utilisateur

        Parameters
        ----------
        pseudo: str
            Pseudo de l'utilisateur qui souhaite se connecter
        mdp: str
            Mot de passe de l'utilisateur qui souhaite se connecter

        Return
        ------
        bool
            True si les identifiants (pseudo, mdp) de l'utilisateur correspondent, False sinon
        """

        utili = self.utilisateurDao.get_utilisateur_by_parameters(pseudo=pseudo)
        if utili is not None and len(utili) > 0 and utili[0]["pseudo"] == pseudo:
            return utili[0]["password"] == mdp

        return False

    def supprimer_utilisateur(self, utilisateur):
        """Supprimer un utilisateur

        Parameters
        ----------
        utilisateur: Utilisateur
        """
        return self.utilisateurDao.delete_utilisateur(pseudo=utilisateur.pseudo)

    def supprimer_utilisateur_by_pseudo(self, pseudo):
        """Supprimer un utilisateur par son pseudo

        Parameters
        ----------
        pseudo: str
            Pseudo de l'utilisateur à supprimer
        """
        return self.utilisateurDao.delete_utilisateur(pseudo=pseudo)

    def se_connecter_administrateur(self, pseudo, mdp):
        """Connecter un administrateur

        Parameters
        ----------
        pseudo: str
            Pseudo de l'utilisateur administrateur
        mdp: str
            Mot de passe de l'utilisateur administrateur

        Return
        ------
        bool
            True si les identifiants correspondent, False sinon
        """
        utili = self.utilisateurDao.get_utilisateur_by_parameters(pseudo=pseudo)
        if utili[0]["administrateur"]:
            if utili[0]["pseudo"] == pseudo:
                return utili[0]["password"] == mdp
        return False

    def se_connecter_organisateur(self, pseudo, mdp):
        """Connecter un organisateur

        Parameters
        ----------
        pseudo: str
            Pseudo de l'utilisateur organisateur
        mdp: str
            Mot de passe de l'utilisateur organisateur

        Return
        ------
        bool
            True si les identifiants correspondent, False sinon
        """
        utili = self.utilisateurDao.get_utilisateur_by_parameters(pseudo=pseudo)
        if utili[0]["organisateur"]:
            if utili[0]["pseudo"] == pseudo:
                return utili[0]["password"] == mdp
        return False

    def connection_ok(self, pseudo, mdp):
        """Connecter n'importe quel utilisateur

        Parameters
        ----------
        pseudo: str
            Pseudo de l'utilisateur
        mdp: str
            Mot de passe de l'utilisateur

        Return
        ------
        bool
            True si la connexion fonctionne, false sinon
        """
        utili = self.utilisateurDao.get_utilisateur_by_parameters(pseudo=pseudo)
        if utili == []:
            return False
        return (
            self.se_connecter_utilisateur(pseudo=pseudo, mdp=mdp)
            or self.se_connecter_administrateur(pseudo=pseudo, mdp=mdp)
            or self.se_connecter_organisateur(pseudo=pseudo, mdp=mdp)
        )

    def pseudo_exist(self, pseudo):
        """Vérifier si un pseudo d'utilisateur existe déjà dans la base

        Parameters
        ----------
        pseudo: str
            Pseudo d'utilisateur à vérifier

        Return
        ------
        bool
            True si le pseudo existe déjà, False sinon
        """
        return self.utilisateurDao.get_utilisateur_by_parameters(pseudo=pseudo) != []

    def return_utilisateur(self, pseudo):
        """Rechercher un utilisateur de la base à partir de son pseudo.

        Parameters
        ----------
        pseudo: str
            Pseudo de l'utilisateur recherché

        Return
        ------
        fetchall()
            Liste de dimension [1x1] contenant l'utilisateur correspondant
        """
        return self.utilisateurDao.get_utilisateur_by_parameters(pseudo=pseudo)
