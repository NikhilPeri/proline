import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import json
import pdb

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

win_set = {"<0.1>": 0, "<0.2>": 0, "<0.3>": 0, "<0.4>": 0, "<0.5>": 0, "<0.6>": 0, "<0.7>": 0, "<0.8>": 0, "<0.9>": 0, "<1-1.5>":0, "<1.5-2>":0, "<2+>": 0}
loss_set = {"<0.1>": 0, "<0.2>": 0, "<0.3>": 0, "<0.4>": 0, "<0.5>": 0, "<0.6>": 0, "<0.7>": 0, "<0.8>": 0, "<0.9>": 0, "<1-1.5>":0, "<1.5-2>":0, "<2+>": 0}
total_set = {"<0.1>": 0, "<0.2>": 0, "<0.3>": 0, "<0.4>": 0, "<0.5>": 0, "<0.6>": 0, "<0.7>": 0, "<0.8>": 0, "<0.9>": 0, "<1-1.5>":0, "<1.5-2>":0, "<2+>": 0}

for diff, win_count in lower_diff_won.iteritems():
    if diff < 0.1:
        win_set["<0.1>"] += win_count
        total_set["<0.1>"] += 1
    elif diff < 0.2:
        win_set["<0.2>"] += win_count
        total_set["<0.2>"] += 1
    elif diff < 0.3:
        win_set["<0.3>"] += win_count
        total_set["<0.3>"] += 1
    elif diff < 0.4:
        win_set["<0.4>"] += win_count
        total_set["<0.4>"] += 1
    elif diff < 0.5:
        win_set["<0.5>"] += win_count
        total_set["<0.6>"] += 1
    elif diff < 0.6:
        win_set["<0.6>"] += win_count
        total_set["<0.6>"] += 1
    elif diff < 0.7:
        win_set["<0.7>"] += win_count
        total_set["<0.7>"] += 1
    elif diff < 0.8:
        win_set["<0.8>"] += win_count
        total_set["<0.8>"] += 1
    elif diff < 0.9:
        win_set["<0.9>"] += win_count
        total_set["<0.9>"] += 1
    elif diff < 1.5:
        win_set["<1-1.5>"] += win_count
        total_set["<1-1.5>"] += 1
    elif diff < 2:
        win_set["<1.5-2>"] += win_count
        total_set["<1.5-2>"] += 1
    else:
        win_set["<2+>"] += win_count
        total_set["<2+>"] += 1

for diff, loss_count in lower_diff_lost.iteritems():
    if diff < 0.1:
        loss_set["<0.1>"] += loss_count
        total_set["<0.1>"] += 1
    elif diff < 0.2:
        loss_set["<0.2>"] += loss_count
        total_set["<0.2>"] += 1
    elif diff < 0.3:
        loss_set["<0.3>"] += loss_count
        total_set["<0.3>"] += 1
    elif diff < 0.4:
        loss_set["<0.4>"] += loss_count
        total_set["<0.4>"] += 1
    elif diff < 0.5:
        loss_set["<0.5>"] += loss_count
        total_set["<0.5>"] += 1
    elif diff < 0.6:
        loss_set["<0.6>"] += loss_count
        total_set["<0.6>"] += 1
    elif diff < 0.7:
        loss_set["<0.7>"] += loss_count
        total_set["<0.7>"] += 1
    elif diff < 0.8:
        loss_set["<0.8>"] += loss_count
        total_set["<0.8>"] += 1
    elif diff < 0.9:
        loss_set["<0.9>"] += loss_count
        total_set["<0.9>"] += 1
    elif diff < 1.5:
        loss_set["<1-1.5>"] += loss_count
        total_set["<1-1.5>"] += 1
    elif diff < 2:
        loss_set["<1.5-2>"] += loss_count
        total_set["<1.5-2>"] += 1
    else:
        loss_set["<2+>"] += loss_count
        total_set["<2+>"] += 1

diff_probability = {}

for diff, num_wins in win_set.iteritems():
    if num_wins == 0 and loss_set[diff] == 0:
        diff_probability[diff] = 0
        total_set[diff] = 0
        continue
    diff_probability[diff] = float(num_wins)/float(num_wins+loss_set[diff])
    total_set[diff] = num_wins + loss_set[diff]

difference_buckets = ["<0.1>", "<0.2>", "<0.3>", "<0.4>", "<0.5>", "<0.6>", "<0.7>", "<0.8>", "<0.9>", "<1-1.5>","<1.5-2>", "<2+>"]
probability = go.Bar(
    x=difference_buckets,
    y=[diff_probability["<0.1>"],
        diff_probability["<0.2>"],
        diff_probability["<0.3>"],
        diff_probability["<0.4>"],
        diff_probability["<0.5>"],
        diff_probability["<0.6>"],
        diff_probability["<0.7>"],
        diff_probability["<0.8>"],
        diff_probability["<0.9>"],
        diff_probability["<1-1.5>"],
        diff_probability["<1.5-2>"],
        diff_probability["<2+>"]]
)

plotly.tools.set_credentials_file(username='nikperi', api_key='julq605nwdbroEtAnbOw')
py.iplot([probability], filename='win-percentage')

trace1 = go.Bar(
    x=difference_buckets,
    y=[win_set["<0.1>"],
        win_set["<0.2>"],
        win_set["<0.3>"],
        win_set["<0.4>"],
        win_set["<0.5>"],
        win_set["<0.6>"],
        win_set["<0.7>"],
        win_set["<0.8>"],
        win_set["<0.9>"],
        win_set["<1-1.5>"],
        win_set["<1.5-2>"],
        win_set["<2+>"]],
    name='Lower Payout Won'
)
trace2 = go.Bar(

    x=difference_buckets,
    y=[loss_set["<0.1>"],
        loss_set["<0.2>"],
        loss_set["<0.3>"],
        loss_set["<0.4>"],
        loss_set["<0.5>"],
        loss_set["<0.6>"],
        loss_set["<0.7>"],
        loss_set["<0.8>"],
        loss_set["<0.9>"],
        loss_set["<1-1.5>"],
        loss_set["<1.5-2>"],
        loss_set["<2+>"]],
    name='Lower Payout Lost'
)
d = [trace1, trace2]
layout = go.Layout(
    barmode='stack'
)

py.iplot(go.Figure(data=d, layout=layout), filename='win-absolute')
