class Tournoi:
    def __init__(
        self, id, nom, nb_equipes, taille_equipe, prix, equipes=None, matchs=None, organisateur=None
    ):
        """Constructeur"""
        self.id = id
        self.nom = nom
        self.nb_equipes = nb_equipes
        self.taille_equipe = taille_equipe
        self.prix = prix
        self.equipes = equipes if equipes is not None else []
        self.matchs = matchs if matchs is not None else []
        self.organisateur = organisateur  # Doit être un utilisateur avec organisateur=True

    def __str__(self):
        """Permet d'afficher les informations d'un tournoi"""
        return (
            f"Tournoi: {self.nom} (ID: {self.id})\n"
            f"Nombre d'équipes: {self.nb_equipes}, Taille d'équipe: {self.taille_equipe}\n"
            f"Prix: {self.prix}\n"
            f"Organisateur: {self.organisateur.nom}\n"
            f"Équipes: {[equipe.nom for equipe in self.equipes]}\n"
            f"Matchs: {len(self.matchs)} matchs prévus"
        )
