class Match:
    """
    Classe représentant un Match.

    Attributs
    ---------
    id_match: str
        ID du match
    id_tournoi: str
        ID du tournoi auquel le match appartient
    date: str
        Date du match
    equipe_orange: Equipe
        Equipe orange
    equipe_bleu: Equipe
        Equipe bleue

    Parameters
    ----------
    id_match: str
    id_tournoi: str
    date: str
    equipe_orange: Equipe
    equipe_bleu: Equipe
    """

    def __init__(self, id_match, date, id_tournoi, equipe_orange, equipe_bleu):
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
