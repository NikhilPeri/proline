require 'json'
require 'date'

data = JSON.parse(File.read('data/events.json'))

new_data = Hash.new
new_data['data'] = data.values.map do |event|
  {
    'date' => event['date'],
    'games' => event['games'].values.map do |game|
        {
          'v' => game['v'].to_f,
          'v+' => game['v+'].to_f,
          't' => game['t'].to_f,
          'h+' => game['h+'].to_f,
          'h' => game['h'].to_f,
          'cutoffDate' => game['cutoffDate'],
          'outcomes' => game['outcomes'],
          'visitor' => game['visitor'].strip,
          'home' => game['home'].strip,
          'sport' => game['sport'],
        }
    end.compact
  }
end

File.write('data/clean_data.json', JSON.pretty_generate(new_data))
puts " #{new_data['data'].count} days of data"
