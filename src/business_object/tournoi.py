class Tournoi:
    def __init__(
        self,
        id_tournoi=None,
        titre=None,
        description=None,
        date_debut=None,
        date_fin=None,
        organisateur=None,
    ):
        """Constructeur"""
        self.id_tournoi = id_tournoi
        self.titre = titre
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.organisateur = organisateur

    def __str__(self):
        """Permet d'afficher les informations d'un tournoi"""
        return (
            f"Tournoi: {self.titre} (ID: {self.id_tournoi})\n"
            f"Description: {self.description}\n"
            f"Date début: {self.prix}\n"
            f"Organisateur: {self.organisateur.nom}\n"
            f"Date début: {self.date_debut}\n"
            f"Date fin: {self.date_fin}"
        )
