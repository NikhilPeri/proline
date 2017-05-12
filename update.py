import urllib
import urllib2
import time
import json

# MLB Data
MLB_ENDPOINT = "https://erikberg.com/mlb/standings.json"
req = urllib2.Request(MLB_ENDPOINT)
req.add_header( "User-Agent", "MyRobot/1.0 (https://github.com/NikhilPeri/proline)")

response = urllib2.urlopen(req).read().decode('utf-8')

mlb_standings = json.loads(response).get("standing")

mlb_data = {}
for standing in mlb_standings:
    team = standing.get("first_name").upper()
    if team == "NEW YORK":
        if standing.get("last_name") == "Yankees":
            team = "NEW YORK-Y"
        elif standing.get("last_name") == "Mets":
            team = "NEW YORK-M"
    elif team == "CHICAGO":
        if standing.get("last_name") == "Cubs":
            team = "CHICAGO-C"
        elif standing.get("last_name") == "White Sox":
            team = "CHICAGO-S"
    elif team == "LOS ANGELES":
        if standing.get("last_name") == "Angels":
            team = "LA ANAHEIM"
        elif standing.get("last_name") == "Dodgers":
            team = "LOS ANGELES-D"

    mlb_data[team] = {}
    mlb_data[team]["rank"] = standing["rank"]
    mlb_data[team]["points_scored_per_game"] = float(standing["points_scored_per_game"])
    mlb_data[team]["points_allowed_per_game"] = float(standing["points_allowed_per_game"])
    mlb_data[team]["win_percentage"] = float(standing["win_percentage"])
    mlb_data[team]["home_win_percentage"] = float(standing["home_won"]) / (float(standing["home_won"]) + float(standing["home_lost"]))
    mlb_data[team]["visitor_win_percentage"] = float(standing["away_won"]) / (float(standing["away_won"]) + float(standing["away_lost"]))

    last_five_w = float(standing["last_five"].split("-")[0])
    last_five_l = float(standing["last_five"].split("-")[1])
    mlb_data[team]["last_five_won_percentage"] = float(last_five_w) / float(last_five_w + last_five_l)

    last_ten_w = float(standing["last_ten"].split("-")[0])
    last_ten_l = float(standing["last_ten"].split("-")[1])
    mlb_data[team]["last_ten_won_percentage"] = float(last_ten_w) / float(last_ten_w + last_ten_l)

    streak = -1 if standing["streak_type"].upper() == "LOSS" else 1
    streak = streak * int(0 if standing["streak_total"] == "-" else standing["streak_total"])
    mlb_data[team]["streak"] = streak

# OLG Data
OLG_EVENTS_ENDPOINT = "https://www.proline.ca/olg-proline-services/rest/api/proline/events/all.jsonp?callback=_jqjsp"
OLG_RESULTS_ENDPOINT = "https://www.proline.ca/olg-proline-services/rest/api/proline/results/all.jsonp?callback=_jqjsp"

with open('data/events.json') as data_file:
    data = json.load(data_file)

response = urllib.urlopen(OLG_EVENTS_ENDPOINT + "&_" + str(int(time.time()*1000))).read()
response = response.replace('_jqjsp(', '', 1)
response = response.replace(');', '', 1)

events = json.loads(response).get("response").get("events").get("eventList")

eventsAdded = 0
mlbEventsAdded = 0
for event in events:
    eventId = event.get("listNumber")
    #listNumber
    if not(data.has_key(eventId)):
        data[eventId] = {}

    #listDate
    if not(data[eventId].has_key("date")):
        data[eventId]["date"] = event.get("listDate")

    #eventsList
    if not(data[eventId].has_key("games")):
        data[eventId]["games"] = {}

    for game in event.get("eventList"):
        #gameId
        gameId = game.get("id")
        if not(data[eventId]["games"].has_key(gameId)):
            #gameId
            data[eventId]["games"][gameId] = {}

            # gameData
            data[eventId]["games"][gameId]["home"] = game.get("homeName")
            data[eventId]["games"][gameId]["visitor"] = game.get("visitorName")
            data[eventId]["games"][gameId]["sport"] = game.get("sport")
            data[eventId]["games"][gameId]["cutoffDate"] = game.get("cutoffDate")
            data[eventId]["games"][gameId]["outcomes"] = []

            #odds
            data[eventId]["games"][gameId]["v+"] = game.get("odds").get("vplus")
            data[eventId]["games"][gameId]["v"] = game.get("odds").get("v")
            data[eventId]["games"][gameId]["t"] = game.get("odds").get("t")
            data[eventId]["games"][gameId]["h"] = game.get("odds").get("h")
            data[eventId]["games"][gameId]["h+"] = game.get("odds").get("hplus")

            if game.get("sport") == "BBL":
                data[eventId]["games"][gameId]["mlb_standings"] = {}
                data[eventId]["games"][gameId]["mlb_standings"]["home"] = {}
                home_stats = mlb_data[data[eventId]["games"][gameId]["home"].upper()]
                data[eventId]["games"][gameId]["mlb_standings"]["home"]["rank"] = home_stats["rank"]
                data[eventId]["games"][gameId]["mlb_standings"]["home"]["points_scored_per_game"] = home_stats["points_scored_per_game"]
                data[eventId]["games"][gameId]["mlb_standings"]["home"]["points_allowed_per_game"] = home_stats["points_allowed_per_game"]
                data[eventId]["games"][gameId]["mlb_standings"]["home"]["win_percentage"] = home_stats["win_percentage"]
                data[eventId]["games"][gameId]["mlb_standings"]["home"]["location_win_percentage"] = home_stats["home_win_percentage"]
                data[eventId]["games"][gameId]["mlb_standings"]["home"]["last_five_won_percentage"] = home_stats["last_five_won_percentage"]
                data[eventId]["games"][gameId]["mlb_standings"]["home"]["last_ten_won_percentage"] = home_stats["last_ten_won_percentage"]
                data[eventId]["games"][gameId]["mlb_standings"]["home"]["streak"] = home_stats["streak"]

                data[eventId]["games"][gameId]["mlb_standings"]["visitor"] = {}
                visitor_stats = mlb_data[data[eventId]["games"][gameId]["visitor"].upper()]
                data[eventId]["games"][gameId]["mlb_standings"]["visitor"]["rank"] = visitor_stats["rank"]
                data[eventId]["games"][gameId]["mlb_standings"]["visitor"]["points_scored_per_game"] = visitor_stats["points_scored_per_game"]
                data[eventId]["games"][gameId]["mlb_standings"]["visitor"]["points_allowed_per_game"] = visitor_stats["points_allowed_per_game"]
                data[eventId]["games"][gameId]["mlb_standings"]["visitor"]["win_percentage"] = visitor_stats["win_percentage"]
                data[eventId]["games"][gameId]["mlb_standings"]["visitor"]["location_win_percentage"] = visitor_stats["visitor_win_percentage"]
                data[eventId]["games"][gameId]["mlb_standings"]["visitor"]["last_five_won_percentage"] = visitor_stats["last_five_won_percentage"]
                data[eventId]["games"][gameId]["mlb_standings"]["visitor"]["last_ten_won_percentage"] = visitor_stats["last_ten_won_percentage"]
                data[eventId]["games"][gameId]["mlb_standings"]["visitor"]["streak"] = visitor_stats["streak"]

                mlbEventsAdded += 1

            eventsAdded += 1

print "Events Added: ", eventsAdded
print "MLB Events Added: ", mlbEventsAdded

response = urllib.urlopen(OLG_RESULTS_ENDPOINT + "&_" + str(int(time.time()*1000))).read()
response = response.replace('_jqjsp(', '', 1)
response = response.replace(');', '', 1)

results = json.loads(response).get("response").get("results").get("resultList")

eventsUpdated = 0
for eventResult in results:
    eventId = eventResult.get("listNumber")
    if not(data.has_key(eventId)):
        break

    for gameResult in eventResult.get("results"):
        gameId = gameResult.get("id")

        if data[eventId]["games"].has_key(gameId):
            outcome = gameResult["odds"]
            data[eventId]["games"][gameId]["outcomes"] = []

            updated = False
            if outcome["vplus"] is not None:
                data[eventId]["games"][gameId]["outcomes"].append("v+")
                updated = True
            if outcome["v"] is not None:
                data[eventId]["games"][gameId]["outcomes"].append("v")
                updated = True
            if outcome["hplus"] is not None:
                data[eventId]["games"][gameId]["outcomes"].append("h+")
                updated = True
            if outcome["h"] is not None:
                data[eventId]["games"][gameId]["outcomes"].append("h")
                updated = True
            if outcome["t"] is not None:
                data[eventId]["games"][gameId]["outcomes"].append("t")
                updated = True
            if updated:
                eventsUpdated += 1

print "Events Updated: ", eventsUpdated

with open('data/events.json', 'w') as data_file:
    data_file.write(json.dumps(data, indent=2))
