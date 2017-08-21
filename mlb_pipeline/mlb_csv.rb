require 'json'
require 'csv'
require 'pry'

file = File.read('../data/events.json')
hash = JSON.parse(file)

CSV.open("mlb_events.csv", "wb") do |csv|
  csv << ["outcome", "h-strk", "h-pspg", "h-papg", "h-10w", "h-rnk", "h-5w", "h-lw", "h-w", \
          "v-strk", "v-pspg", "v-papg", "v-10w", "v-rnk", "v-5w", "v-lw", "v-w", \
          "h+", "h", "t", "v", "v+"]

  hash.values.each do |entry|
      entry["games"].each do |id, game|
        next unless game.has_key?("mlb_standings")
        next if game["outcomes"].nil? || game["outcomes"].empty?

        if game["outcomes"].include?("h+")
          outcome = 1
        elsif game["outcomes"].include?("h")
          outcome = 1
        elsif game["outcomes"].include?("v+")
          outcome = -1
        elsif game["outcomes"].include?("v")
          outcome = -1
        else
          puts "butts"
        end

        h_mlb = game["mlb_standings"]["home"]
        v_mlb = game["mlb_standings"]["visitor"]

        csv << [outcome, h_mlb["streak"], h_mlb["points_scored_per_game"], h_mlb["points_allowed_per_game"], h_mlb["last_ten_won_percentage"], \
                h_mlb["rank"], h_mlb["last_five_won_percentage"], h_mlb["location_win_percentage"], h_mlb["win_percentage"], \
                v_mlb["streak"], v_mlb["points_scored_per_game"], v_mlb["points_allowed_per_game"], v_mlb["last_ten_won_percentage"], \
                v_mlb["rank"], v_mlb["last_five_won_percentage"], v_mlb["location_win_percentage"], v_mlb["win_percentage"]]
      end
  end
end
