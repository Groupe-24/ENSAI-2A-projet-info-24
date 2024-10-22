class Match:
    def __init__(self, id_match, date, id_tournoi, equipe_orange, equipe_bleu):
        """Constructeur"""
        self.id_match = id_match
        self.id_tournoi = id_tournoi
        self.date = date
        self.equipe_orange = equipe_orange
        self.equipe_bleu = equipe_bleu

    def __str__(self):
        """Permet d'afficher les informations d'un match"""

        return (
            f"Match ID: {self.id_match}\n"
            f"Événement: {self.id_tournoi} - Date: {self.date}\n"
            f"{self.equipe_orange.nom} vs {self.equipe_bleu.nom}\n\n"
        )
