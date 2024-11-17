class Pari:
    def __init__(self, id_pari, match, equipe, utilisateur, mise, gain=None):
        self.id_pari = id_pari
        self.match = match
        self.equipe = equipe
        self.utilisateur = utilisateur
        self.mise = mise
        self.gain = gain

    def __str__(self):
        """Permet d'afficher les informations d'un tournoi"""
        return (
            f"ID: {self.id_pari})\n"
            f"Match: {self.match.id_match}\n"
            f"Equipe: {self.equipe.nom}\n"
            f"Utilisateur: {self.utilisateur.nom}\n"
            f"Mise: {self.mise}\n"
            f"Gain: {self.gain}"
        )
