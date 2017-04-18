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
        if status["closed"] and not(status["suspended"] or status["cancelled"]):
            outcome = gameResult["odds"]
            #visitor wins
            if outcome["v+"]:
                data[eventId]["games"]["outcomes"].push("v+")
            if outcome["v"]:
                data[eventId]["games"]["outcomes"].push("v")
            #home wins
            if outcome["h+"]:
                data[eventId]["games"]["outcomes"].push("h+")
            if outcome["h"]:
                data[eventId]["games"]["outcomes"].push("h")
            #tie game
            if outcome["t"]:
                ddata[eventId]["games"]["outcomes"].push("h")

            eventsUpdated += 1

print "Events Updated: ", eventsUpdated

with open('data/events.json', 'w') as data_file:
    data_file.write(json.dumps(data, indent=2))
