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

reponseMatches = requests.get("https://api.rlcstatistics.net/matches?page=1&page_size=1000")

if reponseMatches.status_code != 200:
    raise Exception(
        "Cannot reach (HTTP {}): {}".format(reponseMatches.status_code, reponseMatches.text)
    )

EquipeDAO().delete_equipe("67166b8ca4dfa73fb7bec33c")
# EquipeDAO().delete_equipe("6020c3d4f1e4807cc7032673")
JoueursDAO().delete_joueur("67166b8ca4dfa73fb7bec33f")

for match in reponseMatches.json()["matches"]:
    dict_equipe = {}
    if date.fromisoformat(match["date"][:10]) < date.today():
        id_match = match["id_match"]
        reponseStatistique = requests.get("https://api.rlcstatistics.net/match/" + id_match)
        if reponseStatistique.status_code != 200:
            raise Exception(
                "Cannot reach (HTTP {}): {}".format(reponseMatches.status_code, reponseMatches.text)
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
                for i in range(0, 3):
                    print(i)
                    joueurdao = JoueursDAO()
                    if not (
                        joueurdao.is_in_joueur(id_joueur=stat[color]["players"][i]["player"]["_id"])
                    ):
                        joueurdao.insert_joueur(
                            id_joueur=stat[color]["players"][i]["player"]["_id"],
                            pseudo=stat[color]["players"][i]["player"]["tag"],
                            equipe=dict_equipe[stat[color]["team"]["team"]["name"]],
                            professionnel=False,
                        )
                    else:
                        joueurdao.update_joueur(
                            id_joueur=stat[color]["players"][i]["player"]["_id"],
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
                    StatistiquesDAO().insert_statistique(
                        id_statistique=str(uuid4()),
                        joueur=stat[color]["players"][i]["player"]["_id"],
                        match=stat["_id"],
                        equipe=dict_equipe[stat[color]["team"]["team"]["name"]],
                        goals=stat[color]["players"][i]["stats"]["core"]["goals"],
                        shots=stat[color]["players"][i]["stats"]["core"]["shots"],
                        assists=stat[color]["players"][i]["stats"]["core"]["assists"],
                        saves=stat[color]["players"][i]["stats"]["core"]["saves"],
                        score=stat[color]["players"][i]["stats"]["core"]["score"],
                    )
                # cursor.execute(
                #     "INSERT INTO Tournois(Id_Tournois, Titre, Description, Date_Debut, Date_Fin, Id_Organisateur, Id_Equipe) VALUES                     "
                #     "(%(Id_Tournois)s, %(Titre)s, %(Description)s, %(Date_Debut)s, %(Date_Fin)s, %(Id_Organisateur)s, %(Id_Equipe)s);",
                #     {
                #         "Id_Tournois": stat["event"]["_id"],
                #         "Titre": stat["name"],
                #         "Description": None,
                #         "Date_Debut": None,
                #         "Date_Fin": None,
                #         "Id_Organisateur": None,
                #         "Id_Equipe": None,
                #     },
                # )


# connection.commit()
# cursor.close()
# connection.close()


# TournoiDAO(DBConnection()).insert_tournoi(
#     id_tournoi= stat["event"]["_id"],
#     titre = stat["name"],
# )

# cursor.execute(
#     "INSERT INTO Statistiques(Id_Statistique, Joueur, Match, Equipe, Goals, Shots, Assists, Saves) VALUES                     "
#     "(%(Id_Statistique)s, %(Joueur)s, %(Match)s, %(Equipe)s, %(Goals)s, %(Shots)s, %(Assits)s, %(Saves)s);",
#     {
#         "Id_Statistique": uuid4(),
#         "Joueur": stat["players"][color]["players"][i]["id"],
#         "Match": stat["_id"],
#         "Equipe": stat["players"][color]["team"]["team"]["_id"],
#         "Goals": stat["players"][color]["core"]["goals"],
#         "Shots": stat["players"][color]["core"]["shots"],
#         "Assists": stat["players"][color]["core"]["assists"],
#         "Saves": stat["players"][color]["core"]["saves"],
#         "Score": stat["players"][color]["core"]["score"],
#     },
# )
