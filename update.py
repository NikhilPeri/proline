import urllib
import time
import json

OLG_EVENTS_ENDPOINT = "https://www.proline.ca/olg-proline-services/rest/api/proline/events/all.jsonp?callback=_jqjsp"
OLG_RESULTS_ENDPOINT = "https://www.proline.ca/olg-proline-services/rest/api/proline/results/all.jsonp?callback=_jqjsp"

with open('data/events.json') as data_file:
    data = json.load(data_file)

response = urllib.urlopen(OLG_EVENTS_ENDPOINT + "&_" + str(int(time.time()*1000))).read()
response = response.replace('_jqjsp(', '', 1)
response = response.replace(');', '', 1)

events = json.loads(response).get("response").get("events").get("eventList")

eventsAdded = 0;
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
            data[eventId]["games"][gameId]["outcomes"] = []

            #odds
            data[eventId]["games"][gameId]["v+"] = game.get("odds").get("vplus")
            data[eventId]["games"][gameId]["v"] = game.get("odds").get("v")
            data[eventId]["games"][gameId]["t"] = game.get("odds").get("t")
            data[eventId]["games"][gameId]["h"] = game.get("odds").get("h")
            data[eventId]["games"][gameId]["h+"] = game.get("odds").get("hplus")

            print "Added: " + json.dumps(data[eventId]["games"][gameId])
            eventsAdded += 1

print "Events Added: ", eventsAdded

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
        status = gameResult["status"]

        if not(status["cancelled"] or status["suspended"]):
            outcome = gameResult["odds"]
            if not(data[eventId]["games"].has_key(gameId)):
                break

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
