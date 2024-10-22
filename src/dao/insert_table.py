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

# # remplit les bdd joueurs, equipe, matches et tournois avec les données de l'API


# # Générer un identifiant unique basé sur une chaîne


# def generate_unique_id(data):
#     # Vérifier si 'data' est une chaîne de caractères
#     if isinstance(data, bytes):
#         # Si data est déjà en 'bytes', pas besoin d'encoder
#         return hashlib.sha256(data).hexdigest()
#     else:
#         # Sinon, on encode en 'utf-8' avant de générer le hachage
#         return hashlib.sha256(data.encode("utf-8")).hexdigest()


# # remplissage de Equipe

# response_team = requests.get("https://api.rlcstatistics.net/teams")

# if response_team.status_code != 200:
#     raise Exception(
#         "Cannot reach (HTTP {}): {}".format(response_team.status_code, response_team.text)
#     )


# connection = DBConnection().connection
# cursor = connection.cursor()

# for team in response_team.json():
#     id_team = generate_unique_id(team)
#     cursor.execute(
#         "INSERT INTO Equipe(Id_Equipe, Nom) VALUES                     "
#         "(%(Id_Equipe)s, %(Nom)s);",
#         {
#             "Id_Equipe": id_team,
#             "Nom": team,
#         },
#     )

# connection.commit()

# # remplissage de Joueur

# response_players = requests.get("https://api.rlcstatistics.net/players")

# if response_players.status_code != 200:
#     raise Exception(
#         "Cannot reach (HTTP {}): {}".format(response_players.status_code, response_players.text)
#     )


# for player in response_players.json():
#     id_player = generate_unique_id(player)
#     cursor.execute(
#         "INSERT INTO Joueurs(Id_Joueurs, Pseudo, Equipe, Professionnel) VALUES                     "
#         "(%(Id_Joueurs)s, %(Pseudo)s, %(Equipe)s, %(Professionnel)s);",
#         {
#             "Id_Joueurs": id_player,
#             "Pseudo": player,
#             "Equipe": None,
#             "Professionnel": False,
#         },
#     )

# connection.commit()

# # initialisation de la table Tournois

# response_events = requests.get("https://api.rlcstatistics.net/events")

# if response_events.status_code != 200:
#     raise Exception(
#         "Cannot reach (HTTP {}): {}".format(response_events.status_code, response_events.text)
#     )


# for event in response_events.json():  # a modif
#     id_event = generate_unique_id(event)
#     cursor.execute(
#         "INSERT INTO Tournois(Id_Tournois, Titre, Description, Date_Debut, Date_Fin, Id_Organisateur, Id_Equipe) VALUES                     "
#         "(%(Id_Tournois)s, %(Titre)s, %(Description)s, %(Date_Debut)s, %(Date_Fin)s, %(Id_Organisateur)s, %(Id_Equipe)s);",
#         {
#             "Id_Tournois": id_event,
#             "Titre": event,
#             "Description": None,
#             "Date_Debut": None,
#             "Date_Fin": None,
#             "Id_Organisateur": None,
#             "Id_Equipe": None,
#         },
#     )

# connection.commit()

# # remplissage de la table match

reponseMatches = requests.get("https://api.rlcstatistics.net/matches?page=1&page_size=1000")

if reponseMatches.status_code != 200:
    raise Exception(
        "Cannot reach (HTTP {}): {}".format(reponseMatches.status_code, reponseMatches.text)
    )


# for match in reponseMatches.json()["matches"]:
#     cursor.execute(
#         "INSERT INTO Matches(Id_Matches, Date, Id_Tournois, Equipe_Bleu, Equipe_Orange) VALUES                     "
#         "(%(Id_Matches)s, %(Date)s, %(Id_Tournois)s, %(Equipe_Bleu)s, %(Equipe_Orange)s);",
#         {
#             "Id_Matches": match["id_match"],
#             "Date": match["date"],
#             "Id_Tournois": generate_unique_id(match["event"]),
#             "Equipe_Bleu": generate_unique_id(match["blue"]["team"]),
#             "Equipe_Orange": generate_unique_id(match["orange"]["team"]),
#         },
#     )

# insertion des données statistiques

EquipeDAO().delete_equipe("67166b8ca4dfa73fb7bec33c")
JoueursDAO().delete_joueur("67166b8ca4dfa73fb7bec33f")

for match in reponseMatches.json()["matches"]:
    if date.fromisoformat(match["date"][:10]) < date.today():
        id_match = match["id_match"]
        reponseStatistique = requests.get("https://api.rlcstatistics.net/match/" + id_match)
        if reponseStatistique.status_code != 200:
            raise Exception(
                "Cannot reach (HTTP {}): {}".format(reponseMatches.status_code, reponseMatches.text)
            )
        else:
            stat = reponseStatistique.json()
            for color in ["blue", "orange"]:
                EquipeDAO().insert_equipe(
                    id_equipe=stat[color]["team"]["team"]["_id"],
                    nom=stat[color]["team"]["team"]["name"],
                )
                for i in range(1, 3):
                    joueurdao = JoueursDAO()
                    if not (
                        joueurdao.is_in_joueur(id_joueur=stat[color]["players"][i]["player"]["_id"])
                    ):
                        joueurdao.insert_joueur(
                            id_joueur=stat[color]["players"][i]["player"]["_id"],
                            pseudo=stat[color]["players"][i]["player"]["tag"],
                            equipe=stat[color]["team"]["team"]["_id"],
                            professionnel=False,
                        )
                    else:
                        joueurdao.update_joueur(
                            id_joueur=stat[color]["players"][i]["player"]["_id"],
                            equipe=stat[color]["team"]["team"]["_id"],
                        )
                    if i == 1 and color == "blue":
                        TournoiDAO().insert_tournoi(
                            id_tournoi=stat["event"]["_id"],
                            titre=stat["event"]["name"],
                        )
                        MatchDAO().insert_match(
                            id_match=stat["_id"],
                            id_tournoi=stat["event"]["_id"],
                            date=stat["date"],
                            equipe_orange=stat["orange"]["team"]["team"]["name"],
                            equipe_bleu=stat["blue"]["team"]["team"]["name"],
                        )
                    StatistiquesDAO().insert_statistique(
                        id_statistique=uuid4(),
                        joueur=stat[color]["players"][i]["player"]["_id"],
                        match=stat["_id"],
                        equipe=stat[color]["team"]["team"]["_id"],
                        goals=stat[color]["players"][i]["stat"]["core"]["goals"],
                        shots=stat[color]["players"][i]["stat"]["core"]["shots"],
                        assists=stat[color]["players"][i]["stat"]["core"]["assists"],
                        saves=stat[color]["players"][i]["stat"]["core"]["saves"],
                        score=stat[color]["players"][i]["stat"]["core"]["score"],
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
