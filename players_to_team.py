import numpy as np
import time



import warnings
import statsapi

warnings.filterwarnings('ignore')


RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

#call the sagarin model
from sagarin_model import get_sagarin_ratings
final_ratings, team_list, team_to_index, ratings = get_sagarin_ratings()


#extract team ids to store in dictionary
team_ids= {}
for team in team_list:
    time.sleep(.5)
    result=  statsapi.lookup_team(team)
    team_ids[team]= {
        'id' : result[0]['id'],
        'roster' : None
    }


#add player rosters to each team in team id
for team in team_ids:
    time.sleep(.5)
    roster=statsapi.roster(team_ids[team]['id'])
    lines = roster.split('\n')

    players = []
    for line in lines:
        if line:
            parts = line.split('  ')
            name = parts[-1].strip()
            players.append(name)

    team_ids[team]['roster']= players




#add player ids to each player in players in team in team id 
for team in team_ids:
    team_ids[team]['players'] = []
    for name in team_ids[team]['roster']:
        time.sleep(1)
        result = statsapi.lookup_player(name)
        if result:
            player_id = result[0]['id']
            team_ids[team]['players'].append({
                'name':name,
                'id': player_id
            })




import json

# after your loops complete, save to file
with open('team_data.json', 'w') as f:
    json.dump(team_ids, f)