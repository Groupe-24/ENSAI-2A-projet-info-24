class Equipe:
    """
    Classe représentant une Equipe.

    Attributs
    ---------
    id_equipe : int
        Identifiant de l'équipe
    nom : str
        Nom de l'équipe
    professionnel : bool
        Statut professionnel de l'équipe (True pour professionnel, False sinon)
    """

    def __init__(self, nom, id_equipe=None, professionnel=False):
        """Constructeur"""
        self.id_equipe = id_equipe
        self.nom = nom
        self.professionnel = professionnel

    def __str__(self):
        """Affiche les informations de l'équipe sous forme de chaîne de caractères"""
        return f"Equipe(id: {self.id_equipe}, nom: {self.nom}, professionnel: {self.professionnel})"
