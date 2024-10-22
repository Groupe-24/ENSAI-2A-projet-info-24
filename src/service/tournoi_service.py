import uuid
from business_object.users.tournoi import Tournoi


class TournoiService:
    def __init__(self, tournoi_dao):
        self.tournoi_dao = tournoi_dao

    def creer_tournoi(
        self,
        date,
        nom_tournoi,
        taille_equipe,
        nb_equipes,
        prix,
        equipes=None,
        matchs=None,
        organisateur=None,
    ):
        id_tournoi = str(uuid.uuid4())
        tournoi = Tournoi(
            id_tournoi=id_tournoi,
            nom=nom_tournoi,
            nb_equipes=nb_equipes,
            taille_equipe=taille_equipe,
            prix=prix,
            equipes=equipes,
        )

        return tournoi
