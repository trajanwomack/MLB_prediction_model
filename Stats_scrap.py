import statsapi
import json



with open ('team_data_with_stats.json', 'r') as f:
    player_get= json.load(f)

    

for team in player_get:
    for player in player_get[team]['players']:
        if player ['name'] == 'Adrian Del Castillo':
            print (player['stats'])
            break



for team in player_get:
    for player in player_get[team]['players']:
        if player ['name'] == 'Brandon Pfaadt':
            print (player['stats'])
            break
