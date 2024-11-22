class Tournoi:
    """
    Classe représentant un Tournoi.

    Attributs
    ---------
    id_tournoi: str
        ID du tournoi
    titre: str
        Titre du tournoi
    description: str
        Description du tournoi
    date_debut: str
        Date du début du tournoi
    date_fin: str
        Date de fin du tournoi
    id_organisateur: str
        ID de l'organisateur
    id_equipe: list[str]
        Liste des ID des équipes participantes
    Parameters
    ----------
    id_tournoi: str
    titre: str
    description: str
    date_debut: str
    date_fin: str
    id_organisateur: str
    id_equipe: list[str]
    """

    def __init__(
        self,
        id_tournoi=None,
        titre=None,
        description=None,
        date_debut=None,
        date_fin=None,
        id_organisateur=None,
        id_equipe=None,
    ):
        """Constructeur"""
        self.id_tournoi = id_tournoi
        self.titre = titre
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.id_organisateur = id_organisateur  # Peut être un objet ou un ID
        self.id_equipe = id_equipe  # Liste des équipes participant au tournoi

    def __str__(self):
        """Permet d'afficher les informations d'un tournoi"""
        organisateur_nom = (
            self.id_organisateur.nom
            if hasattr(self.id_organisateur, "nom")
            else self.id_organisateur
        )
        return (
            f"Tournoi: {self.titre} (ID: {self.id_tournoi})\n"
            f"Description: {self.description}\n"
            f"Organisateur: {organisateur_nom}\n"
            f"Date début: {self.date_debut}\n"
            f"Date fin: {self.date_fin}\n"
            f"Équipes participantes: {self.id_equipe if self.id_equipe else 'Aucune'}"
        )
