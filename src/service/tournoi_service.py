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
            id_organisateur=organisateur.id,
        )
        self.tournoi_dao.insert_tournoi(
            id_tournoi=id_tournoi,
            titre=titre,
            description=description,
            date_debut=date_debut,
            date_fin=date_fin,
            id_organisateur=organisateur.id,
        )
        return tournoi

    def lister_tournois(self):
        resultat = self.tournoi_dao.list_tournois()
        liste_tournois = []
        if resultat:
            for un_tournoi in resultat:
                tournoi = Tournoi(
                    id_tournoi=un_tournoi["id_tournois"],
                    titre=un_tournoi["titre"],
                    description=un_tournoi["description"],
                    date_debut=un_tournoi["date_debut"],
                    date_fin=un_tournoi["date_fin"],
                    id_organisateur=un_tournoi["id_organisateur"],
                    id_equipe=un_tournoi["id_equipe"],
                )
                liste_tournois.append(print(tournoi))
        return liste_tournois

    def rechercher_tournoi_titre(self, nom):
        resultat = self.tournoi_dao.get_tournoi_by_titre(nom)
        liste_tournois = []
        if resultat:
            for un_tournoi in resultat:
                tournoi = Tournoi(
                    id_tournoi=un_tournoi["id_tournois"],
                    titre=un_tournoi["titre"],
                    description=un_tournoi["description"],
                    date_debut=un_tournoi["date_debut"],
                    date_fin=un_tournoi["date_fin"],
                    id_organisateur=un_tournoi["id_organisateur"],
                    id_equipe=un_tournoi["id_equipe"],
                )
                liste_tournois.append(print(tournoi))
        return liste_tournois

    def supprimer_tournoi(self, id):
        resultat = self.tournoi_dao.get_tournoi_by_id(id)
        if resultat:
            self.tournoi_dao.delete_tournoi(id)
            return "Le tournoi a bien été supprimé."

        else:
            return "Le tournoi spécifié n'existe pas."
