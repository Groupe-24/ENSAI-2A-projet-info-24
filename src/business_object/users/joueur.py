class Joueur:
    """
    Classe représentant un Joueur

    Attributs
    ----------
    id_joueur : int
        identifiant
    pseudo : str
        pseudo du joueur
    utilisateur : Utilisateur
        objet de la classe utilisateur
    """

    def __init__(self, pseudo, utilisateur=None, equipe=None, id_joueur=None, professionnel=None):
        """Constructeur"""
        self.id_joueur = id_joueur
        self.pseudo = pseudo
        self.utilisateur = utilisateur
        self.equipe = equipe
        self.professionnel = professionnel

    def __str__(self):
        """Permet d'afficher les informations du joueur"""
        return f"Joueur({self.pseudo},{self.utilisateur}.)"

    def as_list(self) -> list[str]:
        """Retourne les attributs du joueur dans une liste"""
        return [self.pseudo, self.utilisateur, self.mail]
