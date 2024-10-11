import requests
from dao.db_connection import DBConnection

# reponseMatches = requests.get("https://api.rlcstatistics.net/matches?page=1&page_size=10")

# if reponseMatches.status_code != 200:
#     raise Exception(
#         "Cannot reach (HTTP {}): {}".format(reponseMatches.status_code, reponseMatches.text)
#     )

# else:
#     print(reponseMatches.json())
#     for match in reponseMatches.json()["matches"]:
#         id_match = match["id_match"]
#         date = match["date"]
#         event = match["event"]

#         team1 = match["blue"]
#         team1_name = team1["team"]
#         team1_players = team1["players"]

#         team2 = match["orange"]
#         team2_name = team2["team"]
#         team2_players = team2["players"]

# reponseTeams = requests.get("https://api.rlcstatistics.net/team?team_name=" + team1_name)

# print(reponseTeams.json())


reponseMatches = requests.get("https://api.rlcstatistics.net/matches?page=1&page_size=10")

if reponseMatches.status_code != 200:
    raise Exception(
        "Cannot reach (HTTP {}): {}".format(reponseMatches.status_code, reponseMatches.text)
    )

connection = DBConnection().connection
cursor = connection.cursor()

for match in reponseMatches.json()["matches"]:
    cursor.execute(
        "INSERT INTO match(id_match, date, event, blue_team, blue_players1, blue_players2, blue_players3, orange_team, orange_players1, orange_players2, orange_players3) VALUES                     "
        "(%(id_match)s, %(date)s, %(event)s, %(blue_team)s, %(blue_players1)s, %(blue_players2)s, %(blue_players3)s, %(orange_team)s, %(orange_players1)s, %(orange_players2)s, %(orange_players3)s);",
        {
            "id_match": match["id_match"],
            "date": match["date"],
            "event": match["event"],
            "blue_team": match["blue"]["team"],
            "blue_players1": match["blue"]["players"][0],
            "blue_players2": match["blue"]["players"][1],
            "blue_players3": match["blue"]["players"][2],
            "orange_team": match["orange"]["team"],
            "orange_players1": match["orange"]["players"][0],
            "orange_players2": match["orange"]["players"][1],
            "orange_players3": match["orange"]["players"][2],
        },
    )
