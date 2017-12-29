require 'json'
require 'date'

data = JSON.parse(File.read('data/events.json'))

data = data.values.sort_by do |event|
  event['date']
end.sample(30)

outcomes = data.map do |event|
  games_by_diff  = event['games'].values.sort_by do |game|
    (game['h'].to_f - game['v'].to_f).abs
  end
  selected_games = games_by_diff.last(3)
  win = selected_games.all? do |game|
    if game['h'].to_f - game['v'].to_f > 0
      game['outcomes'].include?('v')
    else
      game['outcomes'].include?('h')
    end
  end

  payouts = selected_games.map do |game|
    if game['h'].to_f - game['v'].to_f > 0
      game['v'].to_f
    else
      game['h'].to_f
    end
  end

  if win
    payouts.reduce(:+)
  else
    -1
  end
end
puts outcomes
puts outcomes.reduce(0, :+)
