class Pari:
    """
    Classe représentant un Pari.

    Attributs
    ---------
    id_pari: str
        ID du pari
    match: Match
        Match du pari
    equipe: Equipe
        Equipe du pari
    utilisateur: Utilisateur
        Utilisateur qui pari
    mise: float
        Montant de la mise
    gain: float
        Gain du pari (si le pari est gagnant, il sera déterminé à partir de la cote du match,
        si il est perdant, il vaudra 0)

    Parameters
    ----------
    id_pari: str
    match: Match
    equipe: Equipe
    utilisateur: Utilisateur
    mise: float
    gain: float
    """

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
