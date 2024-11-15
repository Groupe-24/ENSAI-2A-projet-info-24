class EquipeService:
    def __init__(self, equipeDao):
        self.equipeDao = equipeDao

    def lister_equipes(self):
        equipes = self.equipeDao.list_equipes()
        if equipes:
            return equipes
        return "Il n'y a aucune équipe."

    def rechercher_equipe(self, id_equipe):
        equipe = self.equipeDao.get_equipe_by_id(id_equipe)
        if equipe:
            return equipe
        return "Il n'y a pas d'équipe avec cet ID."

    def equipe_existe(self, id_equipe):
        return self.equipeDao.get_equipe_by_id(id_equipe) is not None

    def ajouter_equipe(self, nom, description):
        return self.equipeDao.insert_equipe(nom, description)

    def modifier_equipe(self, id_equipe, nom=None, description=None):
        equipe = self.equipeDao.get_equipe_by_id(id_equipe)
        if equipe:
            if nom:
                equipe["nom"] = nom
            if description:
                equipe["description"] = description
            self.equipeDao.update_equipe(equipe)
            return equipe
        return "Il n'y a pas d'équipe avec cet id"

    def supprimer_equipe(self, id_equipe):
        equipe = self.equipeDao.get_equipe_by_id(id_equipe)
        if equipe:
            self.equipeDao.delete_equipe(id_equipe)
            return "Équipe supprimée avec succès"
        return "Il n'y a pas d'équipe avec cet id"

    def lister_equipes_par_nom(self, nom):
        equipes = self.equipeDao.list_equipes_by_name(nom)
        return equipes if equipes else "Il n'y a aucune équipe correspondante"

    def lister_equipes_par_tournoi(self, id_tournoi):
        equipes = self.equipeDao.list_equipes_by_tournament(id_tournoi)
        if equipes:
            return equipes
        else:
            return "Aucune équipe n'est inscrite à ce tournoi"
