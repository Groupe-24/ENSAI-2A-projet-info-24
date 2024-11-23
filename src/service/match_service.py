from business_object.match import Match


class MatchService:
    def __init__(self, matchDao):
        self.matchDao = matchDao

    def rechercher_match_par_date(self, date):
        """Rechercher un match selon sa date

        Parameters
        ----------
        date: str
            Date spécifique
        """
        matches = self.matchDao.get_match_by_date(date)
        if matches:
            return matches
        else:
            return "Il n'existe pas de matches à cette date-là."

    def afficher_calendrier(self):
        """Afficher le calendrier des matchs"""
        matches = self.matchDao.list_matches()
        if not matches:
            return "Aucun match prévu."
        calendrier = {}
        for match in matches:
            id_match = match["id_matches"]
            date = match["date"]
            id_tournoi = match["id_tournois"]
            equipe_orange = match["equipe_orange"]
            equipe_bleu = match["equipe_bleu"]
            if date not in calendrier:
                calendrier[date] = []
            calendrier[date].append(
                {
                    "Id_Match": id_match,
                    "Tournoi": id_tournoi,
                    "Equipe_Orange": equipe_orange,
                    "Equipe_Bleu": equipe_bleu,
                }
            )

        output = ""
        for date, matchs in sorted(calendrier.items()):
            output += f"Date : {date}\n"
            for match in matchs:
                output += (
                    f"  Match {match['Id_Match']} : {match['Equipe_Orange']} vs "
                    f"{match['Equipe_Bleu']} (Tournoi: {match['Tournoi']})\n"
                )
            output += "\n"

        print(output.strip())

    def creer_match(
        self, id_match=None, date=None, id_tournoi=None, equipe_orange=None, equipe_bleu=None
    ):
        """Créer un match

        Parameters
        ----------
        id_match: str
            ID du match à créer (None par défaut)
        date: str
            Date du match
        id_tournoi: str
            ID du tournoi
        equipe_orange: str
            ID de l'équipe orange
        equipe_bleu: str
            ID de l'équipe bleu
        """
        match = Match(id_match, date, id_tournoi, equipe_orange, equipe_bleu)
        self.matchDao.insert_match(id_match, date, id_tournoi, equipe_orange, equipe_bleu)
        return match

    def modifier_match(
        self, id_match, date=None, id_tournoi=None, equipe_orange=None, equipe_bleu=None
    ):
        if not self.matchDao.is_in_match(id_match):
            return "Le match n'existe pas."

        self.matchDao.update_match(id_match, date, id_tournoi, equipe_orange, equipe_bleu)
        match = self.matchDao.get_match_by_id(id_match)
        return match

    def supprimer_match(self, id_match):
        if not self.matchDao.is_in_match(id_match):
            return "Le match n'existe pas."
        self.matchDao.delete_match(id_match)
        return f"Match avec l'ID {id_match} supprimé avec succès."


# from dao.match_dao import MatchDAO

# MatchService(MatchDAO()).afficher_calendrier()
