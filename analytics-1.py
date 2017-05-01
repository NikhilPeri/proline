import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import json

# Analyze sucess  given difference in odds

with open('data/events.json') as data_file:
    data = json.load(data_file)

lower_diff_won = {}
lower_diff_lost = {}

for event in data.values():
    for game in event["games"].values():
        if len(game["outcomes"]) == 0:
            continue
        if game["sport"] == "SCR":
            continue
        diff = 0
        lower_won = False
        if float(game["v"]) > float(game["h"]):
            diff = float(game["v"]) - float(game["h"])
            lower_won = "h" in game["outcomes"]
        else:
            diff = float(game["h"]) - float(game["v"])
            lower_won = "v" in game["outcomes"]

        if lower_won:
            if not lower_diff_won.has_key(diff):
                lower_diff_won[diff] = 0
            lower_diff_won[diff] +=1
        else:
            if not lower_diff_lost.has_key(diff):
                lower_diff_lost[diff] = 0
            lower_diff_lost[diff] +=1
        if diff > 5:
            print json.dumps(game, indent=4, sort_keys=True)

trace1 = go.Bar(
    x=lower_diff_won.keys(),
    y=lower_diff_won.values(),
    name='Won'
)
trace2 = go.Bar(
    x=lower_diff_lost.keys(),
    y=lower_diff_lost.values(),
    name='Lost'
)
d = [trace1, trace2]
layout = go.Layout(
    barmode='stack'
)
plotly.tools.set_credentials_file(username='nikperi', api_key='julq605nwdbroEtAnbOw')

fig = go.Figure(data=d, layout=layout)
py.iplot(fig, filename='stacked-bar')
