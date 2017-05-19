import json
import csv

with open('data/events.json') as data_file:
    data = json.load(data_file)

for event in data.values():
    for game in event["games"].values():
        if game.has_key("outcomes") and len(game["outcomes"]) != 0 and game.has_key("mlb_standings"):
                home_stats = game["mlb_standings"]["home"]
                visitor_stats = game["mlb_standings"]["visitor"]

                inputs = []
                inputs.append(home_stats["streak"] - visitor_stats["streak"])
                inputs.append(home_stats["points_scored_per_game"] - visitor_stats["points_scored_per_game"])
                inputs.append(home_stats["points_allowed_per_game"] - visitor_stats["points_allowed_per_game"])
                inputs.append(home_stats["location_win_percentage"] - visitor_stats["location_win_percentage"])
                inputs.append(home_stats["win_percentage"] - visitor_stats["win_percentage"])
                inputs.append(home_stats["last_five_won_percentage"] - visitor_stats["last_five_won_percentage"])
                inputs.append(home_stats["last_ten_won_percentage"] - visitor_stats["last_ten_won_percentage"])

                label = 0 if "h" in game["outcomes"] else 1
