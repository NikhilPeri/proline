import json
import urllib
import urllib2
from time import sleep

# v+, v, t, h, h+, h_total_p, h_home_p, h_last_5p, h_last_10p, h_streak,
def build_row(game):
    row = []
    row.append(game["v+"])
    row.append(game["v"])
    row.append(game["t"])
    row.append(game["h"])
    row.append(game["h+"])

    standings = get_standings(game)

    row.append(standings["home"]["win_percentage"])
    row.append(float(standings["home"]["home_won"]) / (float(standings["home"]["home_won"]) + float(standings["home"]["home_lost"])))

    last_five_w = float(standings["home"]["last_five"].split("-")[0])
    last_five_l = float(standings["home"]["last_five"].split("-")[1])
    row.append(last_five_w / (last_five_w + last_five_l))

    last_ten_w = float(standings["home"]["last_ten"].split("-")[0])
    last_ten_l = float(standings["home"]["last_ten"].split("-")[1])
    row.append(last_ten_w / (last_ten_w + last_ten_l))

    streak = -1 if standings["home"]["streak_type"].upper() == "LOSS" else 1
    streak = streak * int(0 if standings["home"]["streak_total"] == "-" else standings["home"]["streak_total"])
    row.append(streak)

    row.append(standings["visitor"]["win_percentage"])
    row.append(float(standings["visitor"]["away_won"]) / (float(standings["visitor"]["away_won"]) + float(standings["visitor"]["away_lost"])))

    last_five_w = float(standings["visitor"]["last_five"].split("-")[0])
    last_five_l = float(standings["visitor"]["last_five"].split("-")[1])
    row.append(last_five_w / (last_five_w + last_five_l))

    last_ten_w = float(standings["visitor"]["last_ten"].split("-")[0])
    last_ten_l = float(standings["visitor"]["last_ten"].split("-")[1])
    row.append(last_ten_w / (last_ten_w + last_ten_l))

    streak = -1 if standings["visitor"]["streak_type"].upper() == "LOSS" else 1
    streak = streak * int(0 if standings["visitor"]["streak_total"] == "-" else standings["visitor"]["streak_total"])
    row.append(streak)

    label = "v" if "v" in game["outcomes"] or "v+" in game["outcomes"] else "h"
    row.append(label)

    print row

MLB_ENDPOINT = "https://erikberg.com/mlb/standings/"
API_KEY = '56b0e173-170f-4dcb-983f-111b642e2def'
def get_data(url):
    req = urllib2.Request(url)
    req.add_header("Authorization", "Bearer " + API_KEY)
    req.add_header("Accept-encoding", "gzip")

    data = None
    response = urllib2.urlopen(req)
    sleep(10)
    if "gzip" == response.info().get("Content-encoding"):
        buf = StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        data_json = f.read()
    else:
        data_json = response.read()

    return json.loads(data_json)

def get_standings(game):
    yyyyMMDD = game["cutoffDate"].split(" ")[0].replace("-", "")
    standings = get_data(MLB_ENDPOINT + yyyyMMDD + ".json").get("standing")

    home_standings = standings.find(lambda s: s["first_name"].upper() == game["home"].upper())
    visitor_standings = standings.find(lambda s: s["first_name"].upper() == game["visitor"].upper())

    return {"home" : home_standings, "visitor" : visitor_standings}

with open('data/events.json') as data_file:
    data = json.load(data_file)

for event in data.values():
    for game in event["games"].values():
        if game.has_key("cutoffDate") and game.has_key("outcomes") and len(game["outcomes"]) != 0 and game["sport"] == "BBL":
            build_row(game)
