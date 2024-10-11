import requests
from dao.db_connection import DBConnection
import hashlib

# remplit les bdd joueurs, equipe et matches
# problème dans l'insertion dans matches avec la cohérence des clef etrangere avec tournois


# Générer un identifiant unique basé sur une chaîne
def generate_unique_id(data):
    return hashlib.sha256(data.encode()).hexdigest()


reponseMatches = requests.get("https://api.rlcstatistics.net/matches?page=1&page_size=10")

if reponseMatches.status_code != 200:
    raise Exception(
        "Cannot reach (HTTP {}): {}".format(reponseMatches.status_code, reponseMatches.text)
    )


connection = DBConnection().connection
cursor = connection.cursor()


for match in reponseMatches.json()["matches"]:
    cursor.execute(
        "INSERT INTO Matches(Id_Matches, Date, Id_Tournois, Equipe_Bleu, Equipe_Orange) VALUES                     "
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

# remplissage de Equipe

response_team = requests.get("https://api.rlcstatistics.net/team")

if response_team.status_code != 200:
    raise Exception(
        "Cannot reach (HTTP {}): {}".format(response_team.status_code, response_team.text)
    )

connection = DBConnection().connection
cursor = connection.cursor()

for team in response_team:
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
cursor.close()
connection.close()

# remplissage de Joueur

response_players = requests.get("https://api.rlcstatistics.net/players")

if response_players.status_code != 200:
    raise Exception(
        "Cannot reach (HTTP {}): {}".format(response_players.status_code, response_players.text)
    )

connection = DBConnection().connection
cursor = connection.cursor()

for player in response_players:
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
cursor.close()
connection.close()
