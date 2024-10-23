from business_object.pari import Pari
import uuid


class PariService:
    def __init__(self, pari_dao):
        self.pari_dao = pari_dao

    def parier(self, match, equipe, utilisateur, mise, gain=None):
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

        match:Match
        """
        id_equipe_bleu = match.equipe_bleu.id_equipe
        id_equipe_orange = match.equipe_orange.id_equipe

        resultat = self.pari_dao.liste_pari_match(match.id_match)

        paris_equipe_bleu = paris_equipe_orange = 0
        if resultat:
            for un_pari in resultat:
                if un_pari["id_equipe"] == id_equipe_bleu:
                    paris_equipe_bleu += un_pari["mise"]
                elif un_pari["id_equipe"] == id_equipe_orange:
                    paris_equipe_orange += un_pari["mise"]
        cote_equipe_bleu = paris_equipe_bleu / (paris_equipe_orange + paris_equipe_bleu)
        cote_equipe_orange = paris_equipe_orange / (paris_equipe_orange + paris_equipe_bleu)

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
        """Afficher le gain potentiel

        mise: int
        equipe: Equipe
        """
        cotes = self.afficher_cote(match)
        couleur = cotes[equipe.id_equipe]
        return (cotes["cote_equipe_" + couleur] + 1) * mise
