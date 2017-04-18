import json

with open('data/events.json') as data_file:
    data = json.load(data_file)

totalGames = 0
totalCompleteGames = 0
totalTickets = len(data.values())

for event in data.values():
    for game in event["games"].values():
        totalGames += 1
        if game["outcome"] is not None:
            totalCompleteGames += 1

print "Total Tickets: ", totalTickets
print "Total Games: ", totalGames
print "Total Complete Games: ", totalCompleteGames
