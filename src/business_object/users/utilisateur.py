class Utilisateur:
    """
    Classe représentant un utilisateur

    Attributs
    ----------
    id_utilisteur : int
        identifiant de l'utilisateur
    pseudo : str
        pseudo de l'organisateur
    mdp : str
        le mot de passe de l'organisateur
    statut : str
        indique le statut
    """

    def __init__(self, pseudo, mdp=None, statut, id_utilisateur):
        """Constructeur"""
        self.id_utilisateur = id_utilisateur
        self.pseudo = pseudo
        self.mdp = mdp
        self.statut = statut


    def __str__(self):
        """Permet d'afficher les informations de l'organisateur"""
        return f"Utilisateur({self.pseudo}.)"

    def as_list(self) -> list[str]:
        """Retourne les attributs du joueur dans une liste"""
        return [self.pseudo]
