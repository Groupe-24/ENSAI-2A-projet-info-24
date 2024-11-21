from business_object.pari import Pari
import uuid


class PariService:
    def __init__(self, pari_dao):
        self.pari_dao = pari_dao

    def parier(self, match, equipe, utilisateur, mise, gain=None):
        """Créer un pari pour un match

        Parameters:
        -----------
        match: Match
            Le match à parier

        equipe: Equipe
            L'équipe à parier

        utilisateur: Utilisateur
            L'utilisateur qui pari

        mise: int
            La mise du pari

        gain: int
            None par defaut, le gain potentiel

        Return:
        -------
        Pari
        """
        id_pari = str(uuid.uuid4())
        pari = Pari(
            id_pari=id_pari,
            match=match,
            equipe=equipe,
            utilisateur=utilisateur,
            mise=mise,
            gain=gain,
        )
        self.pari_dao.insert_pari(
            id_pari=id_pari,
            id_match=match.id_match,
            id_equipe=equipe.id_equipe,
            id_utilisateur=utilisateur.id_utilisateur,
            mise=mise,
            gain=gain,
        )
        return pari

    def afficher_cote(self, match):
        """Afficher la cote d'un match

        Parameters:
        -----------
        match: Match
            Match spécifique

        Return:
        -------
        dict
        """
        id_equipe_bleu = match.equipe_bleu.id_equipe
        id_equipe_orange = match.equipe_orange.id_equipe

        resultat = self.pari_dao.list_pari_match(match.id_match)

        paris_equipe_bleu = paris_equipe_orange = 0
        if resultat:
            for un_pari in resultat:
                if un_pari["id_equipe"] == id_equipe_bleu:
                    paris_equipe_bleu += un_pari["mise"]
                elif un_pari["id_equipe"] == id_equipe_orange:
                    paris_equipe_orange += un_pari["mise"]

        total_paris = paris_equipe_bleu + paris_equipe_orange
        if total_paris == 0:
            cote_equipe_bleu = cote_equipe_orange = None
        else:
            cote_equipe_bleu = total_paris / paris_equipe_bleu
            cote_equipe_orange = total_paris / paris_equipe_orange

        print(
            f"Cote equipe bleu : {cote_equipe_bleu}\n" f"Cote equipe orange : {cote_equipe_orange}"
        )
        return {
            "match": match.id_match,
            id_equipe_bleu: "bleu",
            id_equipe_orange: "orange",
            "cote_equipe_bleu": cote_equipe_bleu,
            "cote_equipe_orange": cote_equipe_orange,
        }

    def gain_potentiel(self, mise, equipe, match):
        """Afficher le gain potentiel pour une mise spécifique

        Parameters:
        -----------
        mise: int
            Mise spécifique
        equipe: Equipe
            Equipe spécifique
        match: Match
            Match spécifique

        Return:
        -------
        float
        """
        if equipe.id_equipe not in [match.equipe_orange.id_equipe, match.equipe_bleu.id_equipe]:
            raise ValueError("L'équipe doit jouer dans le match spécifié.")
        cotes = self.afficher_cote(match)
        nom_equipe = "bleu" if equipe.id_equipe == match.equipe_bleu.id_equipe else "orange"
        if f"cote_equipe_{nom_equipe}" not in cotes:
            raise KeyError(f"L'équipe {equipe.id_equipe} n'a pas de cote pour ce match.")
        cote = cotes[f"cote_equipe_{nom_equipe}"]
        return (cote + 1) * mise

    def supprimer_pari(self, pari):
        """Supprimer un pari

        Parameters:
        -----------
        pari: Pari
            Pari spécifique
        """
        resultat = self.pari_dao.exists_by_id(pari.id_pari)
        if not resultat:
            raise ValueError("Le pari n'existe pas.")
        self.pari_dao.delete_pari(pari.id_pari)
        print("Le pari a bien été supprimé.")
