import statsapi
from player_pitching import pitcher_name_to_id




'''
we are going game by game for each game specified in range
 and associating a year, weight, home and away team, and score 
 with each game selected

'''


def get_index_games():
     #get 2023-26 season




    seasons = [
        (2026, 1.0,  '03/25/2026', '06/12/2026')
    ]

    allseason_games = [
   
]


    

    exclude ={'American League All-Stars', 'National League All-Stars'}


    for year, weight, start, end in seasons:
        
        games = statsapi.schedule(start_date=start, end_date=end)
        for game in games:
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

                "away_sp_id": pitcher_name_to_id.get(game["away_probable_pitcher"],-1 )

                })







    return (allseason_games)

                




