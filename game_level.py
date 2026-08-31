import statsapi
from player_pitching import pitcher_name_to_id
import json
import time


'''
we are going game by game for each game specified in range
 and associating a year, weight, home and away team, and score 
 with each game selected

'''
#calculate form helper methods
def calculate_form(team_record, team, window = 10 ):
     if team not in team_record:
          return 0.5
     
     history = team_record[team][-window:]

     return sum(history) / len(history)

def update_record(team_record, home, away, home_runs, away_runs):
    team_record.setdefault(home, [])
    team_record.setdefault(away, [])

    if home_runs > away_runs:
          team_record[home].append(1)
          team_record[away].append(0)
    else:
        team_record[home].append(0)
        team_record[away].append(1)



def get_index_games():
     #get 2023-26 season
    seasons = [(2025, 0.30, '03/27/2025', '09/28/2025'),
         (2026, 1.0,  '03/25/2026', '06/16/2026')]

    allseason_games = []
    
    exclude ={'American League All-Stars', 'National League All-Stars'}

    venue_lookup ={}


    for year, weight, start, end in seasons:
        
        games = statsapi.schedule(start_date=start, end_date=end)
        for game in games:
            time.sleep(1)
        # rename first
            if game['home_name'] == 'Oakland Athletics':
                game['home_name'] = 'Athletics'
            if game['away_name'] == 'Oakland Athletics':
                game['away_name'] = 'Athletics'

                    #check all star games 
            if game ['home_name'] not in exclude and game ['away_name'] not in exclude:

                #add projected pitcher...and map projected piter to player in team_daata_withstats. 
    
                
                

                allseason_games.append({
                "season" : year,
                "weight" : weight,
                "game_date" : game['game_datetime'],
                "home_team": game["home_name"],
                "away_team" : game["away_name"],
                "home_runs" : int(game["home_score"]),
                "away_runs" : int(game["away_score"]),
                "home_sp" : game["home_probable_pitcher"],
                "away_sp" : game["away_probable_pitcher"],

                "home_sp_id": pitcher_name_to_id.get(game["home_probable_pitcher"], -1), #-1 should give us deafualt if lookup fails

                "away_sp_id": pitcher_name_to_id.get(game["away_probable_pitcher"],-1 ),


                "venue_id": game["venue_id"]

                })




                venue_lookup[game["home_name"]] = game["venue_id"]
                
                

    #implement park factor logic ;) calculate
    venue_runs = {} 
    venue_games = {}
    for game in allseason_games:
        vid = game['venue_id']
        venue_runs[vid] = venue_runs.get(vid,0) + game['home_runs'] + game['away_runs']
        venue_games[vid]= venue_games.get(vid,0) +1
                
    #league avg for that PARK
    league_avg = sum(venue_runs.values()) / sum(venue_games.values())

    #park facro =(runs/games)/league avg
    park_factors = {vid: (venue_runs[vid]/venue_games[vid])/ league_avg for vid in venue_runs}

    #add park factor back to each game
    for game in allseason_games:
        game['park_factor']= park_factors[game['venue_id']]

    with open ("team_to_venue.json" , "w") as f:
                    json.dump(venue_lookup, f )
    
    with open ('park_factors.json', 'w') as f:
         json.dump({str(k): v for k, v in park_factors.items()}, f)






    #start current form logic

    allseason_games.sort(key=lambda g: g["game_date"]) #sort recorded games
    team_record = {} 
    for game in allseason_games: #loop through recorded games get home and away team
        home = game["home_team"]
        away = game["away_team"]

        #write home and away from to the game[]
        game["home_form"]= calculate_form(team_record, home) #define "home/awayform" as product of helper method passed team record and team
        game["away_form"] = calculate_form(team_record, away)

        update_record(team_record, home, away, game["home_runs"], game["away_runs"] ) #write to team record

            

    return allseason_games, venue_lookup





if __name__ == "__main__":
    (games, lookup) = get_index_games()
    print("games:", len(games))
    print("lookup size", len(lookup))


