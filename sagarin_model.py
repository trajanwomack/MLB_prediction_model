import statsapi
import numpy as np
import json
import time



def get_sagarin_ratings():
     #get 2023-26 season


    seasons = [
        (2026, 1.0,  '03/25/2026', '06/27/2026'),  # yesterday
        (2025, 0.30, '03/27/2025', '09/28/2025'),
        (2024, 0.15, '03/28/2024', '09/29/2024'),
        (2023, 0.10, '04/01/2023', '10/01/2023'),
    ]

    allseason_games=[]

    exclude ={'American League All-Stars', 'National League All-Stars'}


    for year, weight, start, end in seasons:
        time.sleep(5)
        games = statsapi.schedule(start_date=start, end_date=end)
        for game in games:
        # rename first
            if game['home_name'] == 'Oakland Athletics':
                game['home_name'] = 'Athletics'
            if game['away_name'] == 'Oakland Athletics':
                game['away_name'] = 'Athletics'

                    #check all star games 
            if game ['home_name'] not in exclude and game ['away_name'] not in exclude:
        #get margins weighted
                margin = (int(game['home_score'])-int(game['away_score']))* weight
                allseason_games.append({
                'home_team': game['home_name'],
                'away_team': game ['away_name'],
                'margin': margin
        })
                

     







    #isolate teams to map margins
    all_teams = set() 

    for game in allseason_games:
            all_teams.add(game['home_team'])
            all_teams.add(game['away_team'])

    team_list = sorted(list(all_teams))



    #index teams (give a numer)
    team_to_index = {}
    for index, team in enumerate(team_list):
        team_to_index[team] = index
        


    index_games = []

    for game in allseason_games:
        home = team_to_index[game['home_team']]
        away = team_to_index[game['away_team']]
        margin = game ['margin']

        index_games.append((home,away,margin))

        



    #sargin

    n_teams = len(team_to_index)
    n_games = len(index_games)

    A = np.zeros((n_games, n_teams))
    b = np.zeros(n_games)

    for i, (home,away,margin) in enumerate (index_games):
        A[i, home] = 1
        A[i, away] = -1
        b[i] = margin
        
    ratings = np.linalg.lstsq(A, b, rcond=None)[0]


    final_ratings=[]
    for team in team_to_index:
        rating = ratings[team_to_index[team]]
        final_ratings.append((team, rating))




    return (final_ratings, team_list,team_to_index, ratings)




def sort_by_max(final_ratings, reverse=False):
        return sorted(final_ratings, key=lambda x: x[1], reverse=reverse)



if __name__ == "__main__":
    final_ratings, team_list, team_to_index, ratings = get_sagarin_ratings()



    sorted_ratings = sort_by_max(final_ratings, reverse=True)

    for team, rating in sorted_ratings:
        print(f"{team}: {rating: .2f}")


    sagarin_dict = {}
    for team, rating in final_ratings:
        sagarin_dict[team] = float(rating)

    with open('sagarin_ratings.json', 'w') as f:
        json.dump(sagarin_dict, f)
