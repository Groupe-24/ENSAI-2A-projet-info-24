class Statistics:
    """
    Classe représentant une Statistique.

    Attributs
    ---------
    id_statistique: str
        ID de la statistique
    equipe: str
        nom de l'équipe concernée
    match: str
        ID du match concerné
    joueur: str
        pseudo du joueur concerné
    but: int
        Nombre de but inscrit (None par défaut)
    score_de_match: float
        Score total dans le match
    consommation_boost: float
        Consommation total de boost (None par défaut)

    Parameters
    ----------
    id_statistique: str
    equipe: str
    match: str
    joueur: str
    but: int
    score_de_match: float
    consommation_boost: float
    """

    def __init__(
        self,
        id_statistique,
        equipe,
        match,
        joueur,
        but=None,
        score_de_match=None,
        consommation_boost=None,
    ):
        """Constructeur"""
        self.id_statistique = id_statistique
        self.equipe = equipe
        self.match = match
        self.joueur = joueur
        self.but = but if but is not None else {}
        self.score_de_match = score_de_match if score_de_match is not None else {}
        self.consommation_boost = consommation_boost if consommation_boost is not None else {}

    def __str__(self):
        """Permet d'afficher les informations d'un match avec les statistiques des joueurs"""
        score_line = f"{self.equipe}: {sum(self.score_de_match)}"
        return (
            f"Statistique ID :{self.id_statistique}\n"
            f"Match ID: {self.match}\n"
            f"Score:\n{score_line}"
            f"Statistiques de {self.equipe}:\n"
            f"Buts: {self.but}\n"
        )
