from business_object.match import Match


class MatchService:
    def __init__(self, matchDao):
        self.matchDao = matchDao

    def rechercher_match_par_date(self, date):
        matches = self.matchDao.get_match_by_date(date)
        if matches:  # Vérifier si la liste de matches n'est pas vide
            return matches
        else:
            return "Il n'existe pas de matches à cette date-là"

    def afficher_calendrier(self):
        matches = self.matchDao.list_matches()
        if not matches:
            return "Aucun match prévu."
        calendrier = {}
        for match in matches:
            id_match = match[0]
            date = match[1]
            id_tournoi = match[2]
            equipe_orange = match[3]
            equipe_bleu = match[4]
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
        for date, matchs in sorted(calendrier.items()):
            print(f"Date : {date}")
            for match in matchs:
                print(
                    f"  Match {match['Id_Match']} : {match['Equipe_Orange']} vs {match['Equipe_Bleu']} (Tournoi: {match['Tournoi']})"
                )
            print("\n")

    def creer_match(
        self, id_match=None, date=None, id_tournoi=None, equipe_orange=None, equipe_bleu=None
    ):
        match = Match(id_match, date, id_tournoi, equipe_orange, equipe_bleu)
        self.matchDao.insert_match(id_match, date, id_tournoi, equipe_orange, equipe_bleu)
        return match

    def modifier_match(
        self, id_match, date=None, id_tournoi=None, equipe_orange=None, equipe_bleu=None
    ):
        self.matchDao.update_match(date, id_tournoi, equipe_orange, equipe_bleu)
        match = self.matchDao.get_match_by_id(id_match)
        return match
