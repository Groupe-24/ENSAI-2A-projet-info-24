from business_object.equipe import Equipe


class EquipeService:
    def __init__(self, equipe_dao):
        self.equipe_dao = equipe_dao

    def lister_equipes(self):
        """Lister toutes les équipes de la base

        Return
        ------
        list[Equipe]
        """
        equipes = self.equipe_dao.list_equipes()
        if not equipes:
            raise ValueError("Il n'y a aucune équipe.")
        liste_equipes = []
        for une_equipe in equipes:
            equipe = Equipe(id_equipe=une_equipe["id_equipe"], nom=une_equipe["nom"])
            liste_equipes.append(equipe)
        return liste_equipes

    def rechercher_equipe(self, id_equipe):
        """Rechercher une equipe par ID

        Paramerters
        -----------
        id_equipe: str
            ID de l'équipe spécifique

        Return
        ------
        Equipe
        """
        equipe = self.equipe_dao.get_equipe_by_id(id_equipe)
        if not equipe:
            raise ValueError("Il n'y a pas d'équipe avec cet ID.")
        return Equipe(id_equipe=equipe["id_equipe"], nom=equipe["id_equipe"])

    def equipe_existe(self, id_equipe):
        """Vérifier si une équipe existe selon son ID

        Parameters
        ----------
        id_equipe: str
            ID de l'équipe spécifique

        Return
        ------
        bool
            True si une équipe est trouvée à partir de l'ID spécifié, False sinon
        """
        return self.equipe_dao.get_equipe_by_id(id_equipe) is not None

    def ajouter_equipe(self, nom):
        """Ajouter une equipe

        Parameters
        ----------
        nom: str
        """
        self.equipe_dao.insert_equipe(nom)

    def modifier_equipe(self, id_equipe, nom_modif=None):
        """Modifier une équipe

        Parameters
        ----------
        id_equipe: str
            ID de l'équipe spécifique
        nom_modif: str
            nouveau nom modifié

        Return
        ------
        Equipe
        """
        equipe = self.equipe_dao.get_equipe_by_id(id_equipe)
        if not equipe:
            raise ValueError("Il n'y a pas d'équipe avec cet id.")
        if nom_modif:
            equipe["nom"] = nom_modif
        self.equipe_dao.update_equipe(equipe)
        return Equipe(id_equipe=id_equipe, nom=nom_modif)

    def supprimer_equipe(self, id_equipe):
        """Supprimer une équipe

        Parameters
        ----------
        id_equipe: str
            ID de l'équipe spécifique
        """
        equipe = self.equipe_dao.get_equipe_by_id(id_equipe)
        if not equipe:
            raise ValueError("Il n'y a pas d'équipe avec cet id.")
        self.equipe_dao.delete_equipe(id_equipe)
        return "Équipe supprimée avec succès"

    def lister_equipes_par_nom(self, nom):
        """Lister les équipes selon leur nom

        Parameters
        ----------
        nom: str
            Nom de l'équipe spécifique

        Return
        ------
        list[Equipe]
        """
        equipes = self.equipe_dao.list_equipes_by_name(nom)
        if not equipes:
            raise ValueError("Il n'y a aucune équipe correspondante.")
        liste_equipe = []
        for une_equipe in equipes:
            equipe = Equipe(id_equipe=une_equipe["id_equipe"], nom=une_equipe["nom"])
        liste_equipe.append(equipe)
        return liste_equipe

    def lister_equipes_par_tournoi(self, id_tournoi):
        """Lister les équipes d'un tournoi

        Parameters
        ----------
        id_tournoi: str
            ID du tournoi spécifique

        Return
        ------
        list[Equipe]
        """
        equipes = self.equipe_dao.list_equipes_by_tournoi(id_tournoi)
        if not equipes:
            raise ValueError("Aucune équipe n'est inscrite à ce tournoi.")
        liste_equipe = []
        for une_equipe in equipes:
            equipe = Equipe(id_equipe=une_equipe["id_equipe"], nom=une_equipe["nom"])
            liste_equipe.append(equipe)
        return liste_equipe
