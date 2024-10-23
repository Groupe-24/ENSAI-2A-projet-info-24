import requests
from dao.db_connection import DBConnection
from datetime import date, datetime
from dao.equipe_dao import EquipeDAO
from dao.joueur_dao import JoueursDAO
from dao.match_dao import MatchDAO
from dao.pari_dao import ParisDAO
from dao.statistique_dao import StatistiquesDAO
from dao.utilisateur_dao import UtilisateurDAO
from dao.tournoi_dao import TournoiDAO
from uuid import uuid4

reponseMatches_init = requests.get("https://api.rlcstatistics.net/matches?page=1000&page_size=30")

if reponseMatches_init.status_code != 200:
    raise Exception(
        "Cannot reach (HTTP {}): {}".format(
            reponseMatches_init.status_code, reponseMatches_init.text
        )
    )


totalCount = reponseMatches_init.json()["totalCount"]
pages = 0
dict_equipe = {}
dict_joueur = {}
while 30 * pages < totalCount:

    pages = pages + 1
    reponseMatches = requests.get(
        "https://api.rlcstatistics.net/matches?page=" + str(pages) + "&page_size=30"
    )

    if reponseMatches.status_code != 200:
        raise Exception(
            "Cannot reach (HTTP {}): {}".format(reponseMatches.status_code, reponseMatches.text)
        )

    for match in reponseMatches.json()["matches"]:
        if date.fromisoformat(match["date"][:10]) < date.today():
            id_match = match["id_match"]
            # print(dict_equipe)
            reponseStatistique = requests.get("https://api.rlcstatistics.net/match/" + id_match)
            if reponseStatistique.status_code != 200:
                raise Exception(
                    "Cannot reach (HTTP {}): {}".format(
                        reponseMatches.status_code, reponseMatches.text
                    )
                )
            else:
                stat = reponseStatistique.json()
                id_orange = str(uuid4())
                id_bleu = str(uuid4())
                # dict_color_clef = {"blue": id_bleu, "orange": id_orange}
                if not EquipeDAO().is_in_equipe_by_name(nom=stat["blue"]["team"]["team"]["name"]):
                    EquipeDAO().insert_equipe(
                        id_equipe=id_bleu,
                        nom=stat["blue"]["team"]["team"]["name"],
                    )
                    dict_equipe[stat["blue"]["team"]["team"]["name"]] = id_bleu
                if not EquipeDAO().is_in_equipe_by_name(nom=stat["orange"]["team"]["team"]["name"]):
                    EquipeDAO().insert_equipe(
                        id_equipe=id_orange,
                        nom=stat["orange"]["team"]["team"]["name"],
                    )
                    dict_equipe[stat["orange"]["team"]["team"]["name"]] = id_orange
                for color in ["blue", "orange"]:
                    if stat[color].get("players") is None:
                        n = 3
                    else:
                        n = len(stat[color].get("players"))
                    for i in range(0, n):
                        id_joueur = str(uuid4())
                        joueurdao = JoueursDAO()
                        if stat[color].get("players") is not None:
                            id_ou_None = dict_joueur.get(stat[color]["players"][i]["player"]["tag"])
                            if id_ou_None is None:
                                joueurdao.insert_joueur(
                                    id_joueur=id_joueur,
                                    pseudo=stat[color]["players"][i]["player"]["tag"],
                                    equipe=dict_equipe[stat[color]["team"]["team"]["name"]],
                                    professionnel=False,
                                )
                                dict_joueur[stat[color]["players"][i]["player"]["tag"]] = id_joueur
                            else:
                                joueurdao.update_joueur(
                                    id_joueur=id_ou_None,
                                    equipe=dict_equipe[stat[color]["team"]["team"]["name"]],
                                )
                        # if i == 3 and color == "orange":
                        if not TournoiDAO().is_in_tournoi(stat["event"]["_id"]):
                            TournoiDAO().insert_tournoi(
                                id_tournoi=stat["event"]["_id"],
                                titre=stat["event"]["name"],
                                description="region: "
                                + stat["event"]["region"]
                                + ", mode: "
                                + str(stat["event"]["mode"])
                                + ", tier: "
                                + stat["event"]["tier"],
                            )
                        if not MatchDAO().is_in_match(stat["_id"]):
                            MatchDAO().insert_match(
                                id_match=stat["_id"],
                                id_tournoi=stat["event"]["_id"],
                                date=stat["date"],
                                equipe_orange=dict_equipe[stat[color]["team"]["team"]["name"]],
                                equipe_bleu=dict_equipe[stat[color]["team"]["team"]["name"]],
                            )
                        if stat[color].get("players") is not None:
                            StatistiquesDAO().insert_statistique(
                                id_statistique=str(uuid4()),
                                joueur=dict_joueur[stat[color]["players"][i]["player"]["tag"]],
                                match=stat["_id"],
                                equipe=dict_equipe[stat[color]["team"]["team"]["name"]],
                                goals=stat[color]["players"][i]["stats"]["core"]["goals"],
                                shots=stat[color]["players"][i]["stats"]["core"]["shots"],
                                assists=stat[color]["players"][i]["stats"]["core"]["assists"],
                                saves=stat[color]["players"][i]["stats"]["core"]["saves"],
                                score=stat[color]["players"][i]["stats"]["core"]["score"],
                            )
