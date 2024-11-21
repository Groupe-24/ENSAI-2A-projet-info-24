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
        id_organisateur=None,
        id_equipe=None,
    ):
        """Créer un tournoi

        Parameters
        ----------
        id_tounoi

        Return
        ------
        Tournoi
        """
        if id_tournoi is None:
            id_tournoi = str(uuid.uuid4())
        tournoi = Tournoi(
            id_tournoi=id_tournoi,
            titre=titre,
            description=description,
            date_debut=date_debut,
            date_fin=date_fin,
            id_organisateur=id_organisateur,
            id_equipe=id_equipe,
        )
        self.tournoi_dao.insert_tournoi(
            id_tournoi=id_tournoi,
            titre=titre,
            description=description,
            date_debut=date_debut,
            date_fin=date_fin,
            id_organisateur=id_organisateur,
            id_equipe=id_equipe,
        )
        return tournoi

    def lister_tournois(self):
        """Lister les tournois

        Return
        ------
        list[Tournoi]
        """
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
                    id_organisateur=un_tournoi["id_organisateur"],
                    id_equipe=un_tournoi["id_equipe"],
                )
                liste_tournois.append(tournoi)
        return liste_tournois

    def rechercher_tournoi_nom(self, titre):
        """Rechercher un tournoi avec son titre

        Parameters
        ----------
        Titre : str
            Titre du tournoi

        Return
        ------
        list[Tournoi]
        """
        resultat = self.tournoi_dao.tournoi_by_titre(titre)
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
                    id_equipe=un_tournoi["id_equipe"],
                )
                liste_tournois.append(tournoi)
        return liste_tournois

    def supprimer_tournoi(self, id_tournoi):
        """Supprimer un tournoi

        Parameters
        ----------
        id_tournoi: str
            Tournoi à supprimer
        """
        resultat = self.tournoi_dao.get_tournoi_by_id(id_tournoi)
        if not resultat:
            raise ValueError("Le tournoi spécifié n'existe pas.")
        self.tournoi_dao.delete_tournoi(id_tournoi)
        return "Le tournoi a bien été supprimé."

    def inscrire_tournoi(self, tournoi, pseudo_utilisateur, joueur1, joueur2):
        """S'inscrire à un tournoi

        Parameters
        ----------
        tournoi: Tournoi
            Tournoi spécifique pour lequel l'utilisateur souhaite s'inscire
        joueur1: str
            Nom du 1er joueur avec lequel l'utilisateur souhaite s'inscrire
        joueur2: str
            Nom du 2eme joueur
        """
        resultat = self.tournoi_dao.get_tournoi_by_id(tournoi.id_tournoi)
        if not resultat:
            raise ValueError("Le tournoi spécifié n'existe pas.")
        self.tournoi_dao.update_tournoi(
            id_tournoi=tournoi.id_tournoi,
            id_equipe=resultat["id_equipe"].append([pseudo_utilisateur, joueur1, joueur2]),
        )
