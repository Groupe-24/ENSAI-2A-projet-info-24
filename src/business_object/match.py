class Match:
    def __init__(self, id_match, evenement, date, equipe1, equipe2):
        """Constructeur"""
        self.id_match = id_match
        self.evenement = evenement
        self.date = date
        self.equipe1 = equipe1
        self.equipe2 = equipe2

    def __str__(self):
        """Permet d'afficher les informations d'un match"""

        return (
            f"Match ID: {self.id}\n"
            f"Événement: {self.evenement} - Date: {self.date}\n"
            f"{self.equipe1.nom} vs {self.equipe2.nom}\n\n"
        )
