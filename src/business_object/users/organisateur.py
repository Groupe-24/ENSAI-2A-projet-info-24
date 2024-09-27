class Organisateur:
    """
    Classe représentant un organisateur

    Attributs
    ----------
    pseudo : str
        pseudo de l'organisateur
    mdp : str
        le mot de passe de l'organisateur
    statut : str
        indique le statut
    """

    def __init__(self, pseudo, mdp=None, statut):
        """Constructeur"""
        self.pseudo = pseudo
        self.mdp = mdp
        self.statut = statut

    def __str__(self):
        """Permet d'afficher les informations de l'organisateur"""
        return f"Organisateur({self.pseudo}.)"

    def as_list(self) -> list[str]:
        """Retourne les attributs du joueur dans une liste"""
        return [self.pseudo]
