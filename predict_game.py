import joblib
import pandas as pd
from team_features import team_stats_df
from player_pitching import sp_stats_df, team_sp_avg_df
from player_pitching import pitcher_name_to_id

# load saved model
model = joblib.load('mlb_run_model.pkl')

def predict_game(home_team, away_team, home_sp_name, away_sp_name):
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
predict_game(
    'Philadelphia Phillies', #home
    'Milwaukee Brewers',     #away
    'Andrew Painter',        # home SP
    'Jacob Misiorowski '     # away SP
)