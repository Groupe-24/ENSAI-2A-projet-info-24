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
                    id_tournoi=un_tournoi["id_tournois"],
                    titre=un_tournoi["titre"],
                    description=un_tournoi["description"],
                    date_debut=un_tournoi["date_debut"],
                    date_fin=un_tournoi["date_fin"],
                    id_organisateur=un_tournoi["id_organisateur"],
                    id_equipe=un_tournoi["id_equipe"],
                )
                print(tournoi)
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
        resultat = self.tournoi_dao.get_tournoi_by_titre(titre=titre)
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
                print(tournoi)
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

    def equipe_dans_le_tournoi(self, tournoi_titre, nom_equipe):
        """Vérifier si une équipe existe déjà dans un tournoi.

        Parameters
        ----------
        tournoi_titre: str
            Titre du tournoi
        nom_equipe: str
            Nom de l'équipe à vérifier

        Return
        ------
        bool
            True si l'équipe existe dans le tournoi, False sinon
        """
        tournoi = self.tournoi_dao.get_tournoi_by_titre(tournoi_titre)
        if not tournoi:
            return False
        string_equipe = tournoi[0].get("id_equipe", None)
        if string_equipe is None:
            return False
        list_equipe = string_equipe.split(", ")
        return nom_equipe in list_equipe

    def ajout_equipe(self, tournoi_titre, nom_equipe):
        """Ajouter une équipe à un tournoi

        Parameters
        ----------
        tournoi_titre: str
            Titre du tournoi
        nom_equipe: str
            Nom de l'équipe à inscrire
        """
        if not self.equipe_dans_le_tournoi(tournoi_titre, nom_equipe):
            tournoi = self.tournoi_dao.get_tournoi_by_titre(tournoi_titre)[0]
            if tournoi["id_equipe"] is None:
                string_equipe = nom_equipe
            else:
                string_equipe = tournoi["id_equipe"] + ", " + nom_equipe
            self.tournoi_dao.update_tournoi(
                id_tournoi=tournoi["id_tournois"],
                id_equipe=string_equipe,
            )
