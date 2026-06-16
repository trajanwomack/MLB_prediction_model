
import pandas as pd

from sklearn.metrics import mean_squared_error, r2_score

import warnings


warnings.filterwarnings('ignore')

#here we seperate 


'''
we define what features are added to the teams playing 
Team batting, Team pitching, Team feilding, Team Sagarin
so we can run numbers.
 We have an ititial df defined here aswel
'''

#the option for pitching metrics are still availible 
import json 

with open ('team_data_with_batting.json', 'r') as f:
    team_batting = json.load(f)

#with open ('team_data_with_pitching.json', 'r') as f:
    #team_pitching = json.load(f)

with open('sagarin_ratings.json', 'r') as f:
    sagarin_ratings=json.load(f)


rows = []

for team in sagarin_ratings:
    row = {
        'team': team,
        'sagarin_rating': sagarin_ratings[team],
    }
    
    # add batting stats with bat_ prefix
    batting = {f'bat_{k}': v for k, v in team_batting[team]['team_batting'].items()}
    #pitching = {f'pit_{k}': v for k, v in team_pitching[team]['team_pitching'].items()}
    
    row.update(batting)
    #row.update(pitching)
    rows.append(row)
 
   
#!!!!
#create index for look up based on team 
team_stats_df = pd.DataFrame(rows)
team_stats_df = team_stats_df.set_index('team')


bat_cols = [col for col in team_stats_df.columns if col.startswith('bat_')]
pit_cols = [col for col in team_stats_df.columns if col.startswith('pit_')]


team_stats_df.to_json("team_features.json", orient="index")



