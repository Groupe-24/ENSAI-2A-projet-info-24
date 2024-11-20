import uuid
from business_object.tournoi import Tournoi


class TournoiService:
    def __init__(self, tournoi_dao):
        self.tournoi_dao = tournoi_dao

    def creer_tournoi(
        self,
        id_tournoi=None,
        titre=None,
        description=None,
        date_debut=None,
        date_fin=None,
        organisateur=None,
    ):
        id_tournoi = str(uuid.uuid4())
        tournoi = Tournoi(
            id_tournoi=id_tournoi,
            titre=titre,
            description=description,
            date_debut=date_debut,
            date_fin=date_fin,
            id_organisateur=organisateur["id_utilisateur"],
        )
        self.tournoi_dao.insert_tournoi(
            id_tournoi=id_tournoi,
            titre=titre,
            description=description,
            date_debut=date_debut,
            date_fin=date_fin,
            id_organisateur=organisateur["id_utilisateur"],
        )
        return tournoi

    def lister_tournois(self):
        resultat = self.tournoi_dao.list_tournois()
        liste_tournois = []
        if resultat:
            for un_tournoi in resultat:
                tournoi = Tournoi(
                    id_tournoi=un_tournoi["id_tournoi"],
                    titre=un_tournoi["titre"],
                    description=un_tournoi["description"],
                    date_debut=un_tournoi["date_debut"],
                    date_fin=un_tournoi["date_fin"],
                    organisateur=un_tournoi["id_organisateur"],
                )
                liste_tournois.append(tournoi)
        return liste_tournois

    def rechercher_tournoi_nom(self, nom):
        resultat = self.tournoi_dao.tournoi_par_nom(nom)
        liste_tournois = []
        if resultat:
            for un_tournoi in resultat:
                tournoi = Tournoi(
                    id_tournoi=un_tournoi["id_tournoi"],
                    titre=un_tournoi["titre"],
                    description=un_tournoi["description"],
                    date_debut=un_tournoi["date_debut"],
                    date_fin=un_tournoi["date_fin"],
                    organisateur=un_tournoi["id_organisateur"],
                )
                liste_tournois.append(tournoi)
        return liste_tournois
