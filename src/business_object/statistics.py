class Statistics:
    def __init__(
        self,
        id_equipe,
        id_match,
        id_joueur,
        buts1=None,
        buts2=None,
        tirs1=None,
        tirs2=None,
        score1=None,
        score2=None,
        assists1=None,
        assists2=None,
        arrets1=None,
        arrets2=None,
    ):
        """Constructeur"""
        self.id_equipe = id_equipe
        self.id_match = id_match
        self.id_joueur = id_joueur
        self.buts1 = buts1 if buts1 is not None else {}
        self.buts2 = buts2 if buts2 is not None else {}
        self.tirs1 = tirs1 if tirs1 is not None else {}
        self.tirs2 = tirs2 if tirs2 is not None else {}
        self.score1 = score1 if score1 is not None else {}
        self.score2 = score2 if score2 is not None else {}
        self.assists1 = assists1 if assists1 is not None else {}
        self.assists2 = assists2 if assists2 is not None else {}
        self.arrets1 = arrets1 if arrets1 is not None else {}
        self.arrets2 = arrets2 if arrets2 is not None else {}

    def __str__(self):
        """Permet d'afficher les informations d'un match avec les statistiques des joueurs"""
        score_line = (
            f"{self.equipe1.nom}: {sum(self.score1.values())}, "
            f"{self.equipe2.nom}: {sum(self.score2.values())}\n\n"
        )
        return (
            f"Match ID: {self.id}\n"
            f"{self.equipe1.nom} vs {self.equipe2.nom}\n\n"
            f"Score:\n{score_line}"
            f"Statistiques de {self.equipe1.nom}:\n"
            f"Buts: {self.buts1}\n"
            f"Tirs: {self.tirs1}\n"
            f"Assists: {self.assists1}\n"
            f"Arrêts: {self.arrets1}\n\n"
            f"Statistiques de {self.equipe2.nom}:\n"
            f"Buts: {self.buts2}\n"
            f"Tirs: {self.tirs2}\n"
            f"Assists: {self.assists2}\n"
            f"Arrêts: {self.arrets2}"
        )
