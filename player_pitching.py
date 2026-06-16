import json
import pandas as pd

with open('team_data_with_stats.json', 'r') as g:
    team_stats=json.load(g)

#helper methods/ lookup
pitcher_name_to_id = {}



def ip_conversion(value, default=0.0):
    try:
        value = float(value)

        whole_innings = int(value)
        outs = round((value - whole_innings) * 10)

        if outs == 0:
            return whole_innings
        elif outs == 1:
            return whole_innings + (1 / 3)
        elif outs == 2:
            return whole_innings + (2 / 3)
        else:
            return default

    except (ValueError, TypeError):
        return default
    

def safe_float(value, default = 0.0):
    try:
        return float(value)
    except(ValueError, TypeError):
        return default

starting_pitchers = []

for team in team_stats :

    for player in team_stats[team]['players']:
    
        pitcher_name_to_id[player["name"]] = player["id"]

    
        stats= player.get('stats',{})

        if not stats:
            continue

        

        if 'inningsPitched' not in stats:


            
            continue

      
            
        


    
   

        starting_pitchers.append({
            "id": int(player["id"]),
            "name": player["name"],
            "team": team,

            "era": safe_float(stats["era"]),
            "whip": safe_float(stats["whip"]),
            "strikeouts_per_9": safe_float(stats["strikeoutsPer9Inn"]),
            "walks_per_9": safe_float(stats["walksPer9Inn"]),
            "hits_per_9": safe_float(stats["hitsPer9Inn"]),
            "home_runs_per_9": safe_float(stats["homeRunsPer9"]),
            "strikeout_walk_ratio": safe_float(stats["strikeoutWalkRatio"]),
            "ground_outs_to_airouts": safe_float(stats["groundOutsToAirouts"]),
            "pitches_per_inning": safe_float(stats["pitchesPerInning"]),

            "games_started": int(stats["gamesStarted"]),
            "games_pitched": int(stats["gamesPitched"]),
            "innings_pitched": ip_conversion(stats["inningsPitched"])


        })


#convert id to int for key

sp_stats_df = pd.DataFrame(starting_pitchers) 
sp_stats_df["id"] = sp_stats_df["id"].astype(int)


sp_stats_df = sp_stats_df.set_index('id')



#add a fall back team team avg sp stats for missing starts
team_sp_avg_df = (
    sp_stats_df
    .groupby("team")
    .mean(numeric_only=True)
) 




