class Joueur_pro:
    """
    Classe représentant un Joueur professionnel

    Attributs
    ----------
    id_joueur : int
        identifiant
    pseudo : str
        pseudo du joueur
    mdp : str
        le mot de passe du joueur
    mail : str
        mail du joueur
    statut : str
        statut du joueur
    """

    def __init__(self, pseudo, mail, mdp=None, statut, id_joueur=None):
        """Constructeur"""
        self.id_joueur = id_joueur
        self.pseudo = pseudo
        self.mdp = mdp
        self.mail = mail
        self.statut = statut

    def __str__(self):
        """Permet d'afficher les informations du joueur"""
        return f"Joueur({self.pseudo}, {self.statut}.)"

    def as_list(self) -> list[str]:
        """Retourne les attributs du joueur dans une liste"""
        return [self.pseudo, self.statut, self.mail]
