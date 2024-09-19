import requests


reponseMatches = requests.get("https://api.rlcstatistics.net/matches?page=1&page_size=10")

if reponseMatches.status_code != 200:
    raise Exception(
        "Cannot reach (HTTP {}): {}".format(reponseMatches.status_code, reponseMatches.text)
    )

else:
    print(reponseMatches.json())
    for match in reponseMatches.json()["matches"]:
        id_match = match["id_match"]
        date = match["date"]
        event = match["event"]

        team1 = match["blue"]
        team1_name = team1["team"]
        team1_players = team1["players"]

        team2 = match["orange"]
        team2_name = team2["team"]
        team2_players = team2["players"]

reponseTeams = requests.get("https://api.rlcstatistics.net/team?team_name=" + team1_name)

print(reponseTeams.json())
