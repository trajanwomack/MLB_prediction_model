

from game_level import get_index_games
from team_features import team_stats_df
from player_pitching import sp_stats_df, team_sp_avg_df
import pandas as pd





def build_game_dataset():

    game_level= get_index_games()

    games = []

    for game in game_level: #take each game in specified history

        #get season+weight+day
        game_season = game["season"]

        game_weight = game["weight"]

        game_date = game["game_date"]



        #get team names
        home_team = game["home_team"]
        away_team = game ["away_team"]

        #get runs
        home_runs = game["home_runs"]
        away_runs = game["away_runs"]

        #get pitchers
        home_sp_id = game["home_sp_id"]
        away_sp_id = game["away_sp_id"]


    #starting pitcher mapping loses about 200 games. Take the league avg for those games
        if home_sp_id is None or home_sp_id not in sp_stats_df.index:
            home_sp_features = team_sp_avg_df.loc[home_team]

        else:
            home_sp_features =  sp_stats_df.loc[home_sp_id]


        if away_sp_id is None or away_sp_id not in sp_stats_df.index:
            away_sp_features = team_sp_avg_df.loc[away_team]

        else:
            away_sp_features = sp_stats_df.loc[away_sp_id]


        #get stats using lookup index from features
        home_features = team_stats_df.loc[home_team]
        away_features = team_stats_df.loc[away_team]


        row = {

            "season" : game_season,
            "weight" : game_weight,

            "date/time" : game_date,
        
            "home_team" : home_team,
            "away_team" : away_team,

                    #targets 
            "home_runs" : home_runs,
            "away_runs" : away_runs
            ###"run_diff" : home_runs - away_runs
        }
        

            #features
        for feature in team_stats_df.columns: #loop through every feature column
            row[f"home_{feature}"] = home_features[feature]
            row[f"away_{feature}"] = away_features[feature]
            
            #only inlcude for non random forrest models
            '''row[f"diff_{feature}"] = ( 
                home_features[feature] - away_features[feature]
            )'''

    
        #match the features to players + op differ
        for feature in sp_stats_df.columns:
            if feature in ["name", "team"]:
                continue
            row[f"home_sp_{feature}"] = home_sp_features[feature]
            row[f"away_sp_{feature}"] = away_sp_features[feature]
            row[f"diff_sp_{feature}"] = home_sp_features[feature] - away_sp_features[feature]

        games.append(row)


    game_df = pd.DataFrame(games)
    game_df = game_df.apply(pd.to_numeric, errors= 'coerce') #change the data types to numeric and replace non numeric with nan
        
    return game_df

if __name__ =="__main__":
    game_df = build_game_dataset()
    game_df.to_pickle('game_df.pkl')
    print(f"Saved game_df with shape {game_df.shape}")