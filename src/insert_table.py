import requests
from dao.db_connection import DBConnection
import hashlib
from utils.function import generate_unique_id

# remplit les bdd joueurs, equipe, matches et tournois avec les données de l'API


# Générer un identifiant unique basé sur une chaîne


def generate_unique_id(data):
    # Vérifier si 'data' est une chaîne de caractères
    if isinstance(data, bytes):
        # Si data est déjà en 'bytes', pas besoin d'encoder
        return hashlib.sha256(data).hexdigest()
    else:
        # Sinon, on encode en 'utf-8' avant de générer le hachage
        return hashlib.sha256(data.encode("utf-8")).hexdigest()


# remplissage de Equipe

response_team = requests.get("https://api.rlcstatistics.net/teams")

if response_team.status_code != 200:
    raise Exception(
        "Cannot reach (HTTP {}): {}".format(response_team.status_code, response_team.text)
    )


connection = DBConnection().connection
cursor = connection.cursor()

for team in response_team.json():
    id_team = generate_unique_id(team)
    cursor.execute(
        "INSERT INTO Equipe(Id_Equipe, Nom) VALUES                     "
        "(%(Id_Equipe)s, %(Nom)s);",
        {
            "Id_Equipe": id_team,
            "Nom": team,
        },
    )

connection.commit()

# remplissage de Joueur

response_players = requests.get("https://api.rlcstatistics.net/players")

if response_players.status_code != 200:
    raise Exception(
        "Cannot reach (HTTP {}): {}".format(response_players.status_code, response_players.text)
    )


for player in response_players.json():
    id_player = generate_unique_id(player)
    cursor.execute(
        "INSERT INTO Joueurs(Id_Joueurs, Pseudo, Equipe, Professionnel) VALUES                     "
        "(%(Id_Joueurs)s, %(Pseudo)s, %(Equipe)s, %(Professionnel)s);",
        {
            "Id_Joueurs": id_player,
            "Pseudo": player,
            "Equipe": None,
            "Professionnel": False,
        },
    )

connection.commit()

# initialisation de la table Tournois

response_events = requests.get("https://api.rlcstatistics.net/events")

if response_events.status_code != 200:
    raise Exception(
        "Cannot reach (HTTP {}): {}".format(response_events.status_code, response_events.text)
    )


for event in response_events.json():  # a modif
    id_event = generate_unique_id(event)
    cursor.execute(
        "INSERT INTO Tournois(Id_Tournois, Titre, Description, Date_Debut, Date_Fin, Id_Organisateur, Id_Equipe) VALUES                     "
        "(%(Id_Tournois)s, %(Titre)s, %(Description)s, %(Date_Debut)s, %(Date_Fin)s, %(Id_Organisateur)s, %(Id_Equipe)s);",
        {
            "Id_Tournois": id_event,
            "Titre": event,
            "Description": None,
            "Date_Debut": None,
            "Date_Fin": None,
            "Id_Organisateur": None,
            "Id_Equipe": None,
        },
    )

connection.commit()

# remplissage de la table match

reponseMatches = requests.get("https://api.rlcstatistics.net/matches?page=1&page_size=10")

if reponseMatches.status_code != 200:
    raise Exception(
        "Cannot reach (HTTP {}): {}".format(reponseMatches.status_code, reponseMatches.text)
    )


for match in reponseMatches.json()["matches"]:
    cursor.execute(
        "INSERT INTO Matches(Id_Matches, Date, Id_Tournois, Equipe_Bleu, Equipe_Orange) VALUES"
        "(%(Id_Matches)s, %(Date)s, %(Id_Tournois)s, %(Equipe_Bleu)s, %(Equipe_Orange)s);",
        {
            "Id_Matches": match["id_match"],
            "Date": match["date"],
            "Id_Tournois": generate_unique_id(match["event"]),
            "Equipe_Bleu": generate_unique_id(match["blue"]["team"]),
            "Equipe_Orange": generate_unique_id(match["orange"]["team"]),
        },
    )

connection.commit()
cursor.close()
connection.close()
