class Statistics:
    def __init__(
        self,
        id_statistique,
        joueur,
        match,
        equipe,
        goals=None,
        assists=None,
        saves=None,
        shots=None,
        score=None,
    ):
        """Constructeur"""
        self.id_statistique = id_statistique
        self.joueur = joueur
        self.match = match
        self.equipe = equipe
        self.goals = goals if goals is not None else 0  # Défaut à 0 si None
        self.assists = assists if assists is not None else 0
        self.saves = saves if saves is not None else 0
        self.shots = shots if shots is not None else 0
        self.score = score if score is not None else 0

    def __str__(self):
        """Permet d'afficher les informations d'un match avec les statistiques des joueurs"""
        return (
            f"Statistique ID : {self.id_statistique}\n"
            f"Joueur: {self.joueur}\n"
            f"Match ID: {self.match}\n"
            f"Equipe: {self.equipe}\n"
            f"Buts: {self.goals}\n"
            f"Assists: {self.assists}\n"
            f"Saves: {self.saves}\n"
            f"Shots: {self.shots}\n"
            f"Score: {self.score}"
        )
