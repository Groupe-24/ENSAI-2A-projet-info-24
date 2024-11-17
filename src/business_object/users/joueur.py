class Joueur:
    """
    Classe représentant un Joueur

    Attributs
    ----------
    id_joueur : int
        identifiant
    pseudo : str
        pseudo du joueur
    equipe: str
        equipe du joueur
    professionnel: booléen
        si c'est un joueur professionnel ou pas
    """

    def __init__(self, pseudo, equipe=None, id_joueur=None, professionnel=None):
        """Constructeur"""
        self.id_joueur = id_joueur
        self.pseudo = pseudo
        self.equipe = equipe
        self.professionnel = professionnel

    def __str__(self):
        """Permet d'afficher les informations du joueur"""
        return f"Joueur({self.pseudo},{self.id_joueur},{self.equipe},{self.professionnel}.)"
