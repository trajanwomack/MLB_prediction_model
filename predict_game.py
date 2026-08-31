import joblib
import pandas as pd
import json
from team_features import team_stats_df
from player_pitching import sp_stats_df, team_sp_avg_df
from player_pitching import pitcher_name_to_id
from difflib import get_close_matches



# load saved model
model = joblib.load('mlb_run_model.pkl')




#get team stadiums
with open("team_to_venue.json", "r") as f:
    TEAM_TO_VENUE = json.load(f)

with open("park_factors.json", "r") as f:
    PARK_FACTORS = json.load(f)


#team name mispelling safety
def find_team(team_name,team_name_list): 

    #if exists
    if team_name in team_name_list:
        return team_name
    

    #if missppelled
    team_name_matches = get_close_matches(team_name,team_name_list, n=1, cutoff =.6)

    if team_name_matches:
        print (f"Team '{team_name}' was mispelled, Assuming you meant '{team_name_matches[0]}'")
        return team_name_matches[0]

    #no team 
    else:
        print(f"Team '{team_name}' was not found even after closest matching")
        return None
    

#starting pitcher spell check
def find_pitcher(sp_name,sp_list):
    if sp_name in sp_list:
        return sp_name
    
    sp_name_matches= get_close_matches(sp_name, sp_list, n=1, cutoff=.6)

    if sp_name_matches:
        return sp_name_matches [0]
    
    else:
        return None




#actual prediction method 
def predict_game(home_team, away_team, home_sp_name, away_sp_name,):

    team_name_list = team_stats_df.index.tolist() #get valid teams
    sp_name_list = sp_stats_df['name'].tolist() #get valid sp's

    
    home_team = find_team(home_team, team_name_list) #wrap home/away team in spelling saftey
    away_team = find_team(away_team, team_name_list)
    home_sp_name = find_pitcher(home_sp_name, sp_name_list)#wrap pitcher in spelling saftey before id fall back 
    away_sp_name = find_pitcher(away_sp_name, sp_name_list)

  

    if home_team is None or away_team is None:
        print("Spelling error rerun with valid names")
        return None

      # load team to venue lookup
    venue_id = TEAM_TO_VENUE.get(home_team, 0)  
  
    row['park_factor'] =PARK_FACTORS [venue_id]



# get team features
    home_features = team_stats_df.loc[home_team]
    away_features = team_stats_df.loc[away_team]
    
    #get SP features
    home_sp_id = pitcher_name_to_id.get(home_sp_name)
    away_sp_id = pitcher_name_to_id.get(away_sp_name)
    
    #team avg if SP not found
    if home_sp_id is None or home_sp_id not in sp_stats_df.index:
        home_sp = team_sp_avg_df.loc[home_team]
    else:
        home_sp = sp_stats_df.loc[home_sp_id]
        
    if away_sp_id is None or away_sp_id not in sp_stats_df.index:
        away_sp = team_sp_avg_df.loc[away_team]
    else:
        away_sp = sp_stats_df.loc[away_sp_id]
    
    #build row
    row = {}

    
    for feature in team_stats_df.columns:
        row[f"home_{feature}"] = home_features[feature]
        row[f"away_{feature}"] = away_features[feature]
        
        
        

    for feature in sp_stats_df.columns:
        if feature in ["name", "team"]:
            continue
        row[f"home_sp_{feature}"] = home_sp[feature]
        row[f"away_sp_{feature}"] = away_sp[feature]
        row[f"diff_sp_{feature}"] = home_sp[feature] - away_sp[feature]
    
    #predict
    df = pd.DataFrame([row]).fillna(0)
    pred = model.predict(df)
    
    home_runs = round(pred[0][0])
    away_runs = round(pred[0][1])
    
    print(f"{home_team}: {home_runs}")
    print(f"{away_team}: {away_runs}")
    
    return home_runs, away_runs

# test it
if __name__ == "__main__": # allows for importation to run_easy_prediction
    predict_game(
        'Cardinals', #home
        'Diamondbacks',     #away
        'Martin Perez',        # home SP
        'Kyle Harrison'     # away SP
    )