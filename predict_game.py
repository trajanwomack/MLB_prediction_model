
import joblib
import pandas as pd
import json
from team_features import team_stats_df
from player_pitching import sp_stats_df, team_sp_avg_df
from player_pitching import pitcher_name_to_id
from difflib import get_close_matches


# load saved models
rf_model = joblib.load('rf_model.pkl')
xgb_model = joblib.load('xgb_model.pkl')


# get team stadiums
with open("team_to_venue.json", "r") as f:
    TEAM_TO_VENUE = json.load(f)

with open("park_factors.json", "r") as f:
    PARK_FACTORS = json.load(f)


# team name misspelling safety
def find_team(team_name, team_name_list):

    # if exists
    if team_name in team_name_list:
        return team_name

    # if misspelled
    team_name_matches = get_close_matches(
        team_name,
        team_name_list,
        n=1,
        cutoff=.6
    )

    if team_name_matches:
        print(
            f"Team '{team_name}' was misspelled, "
            f"Assuming you meant '{team_name_matches[0]}'"
        )
        return team_name_matches[0]

    # no team
    else:
        print(
            f"Team '{team_name}' was not found even after closest matching"
        )
        return None


# starting pitcher spell check
def find_pitcher(sp_name, sp_list):

    if sp_name in sp_list:
        return sp_name

    sp_name_matches = get_close_matches(
        sp_name,
        sp_list,
        n=1,
        cutoff=.6
    )

    if sp_name_matches:
        return sp_name_matches[0]

    else:
        return None


# actual prediction method
def predict_game(home_team, away_team, home_sp_name, away_sp_name):

    team_name_list = team_stats_df.index.tolist()
    sp_name_list = sp_stats_df['name'].tolist()

    home_team = find_team(home_team, team_name_list)
    away_team = find_team(away_team, team_name_list)

    home_sp_name = find_pitcher(home_sp_name, sp_name_list)
    away_sp_name = find_pitcher(away_sp_name, sp_name_list)

    if home_team is None or away_team is None:
        print("Spelling error rerun with valid names")
        return None

    # get home team's venue
    venue_id = TEAM_TO_VENUE.get(home_team, 0)

    # build prediction row
    row = {}

    # features from game_level.py
    row['weight'] = 1.0
    row['venue'] = venue_id
    row['park_factor'] = PARK_FACTORS.get(str(venue_id), 1.0)

    # game_level.py uses 0.5 as the default form
    # when no previous game history is available
    row['home_form'] = 0.5
    row['away_form'] = 0.5

    # get team features
    home_features = team_stats_df.loc[home_team]
    away_features = team_stats_df.loc[away_team]

    # get SP features
    home_sp_id = pitcher_name_to_id.get(home_sp_name)
    away_sp_id = pitcher_name_to_id.get(away_sp_name)

    # team average if SP not found
    if home_sp_id is None or home_sp_id not in sp_stats_df.index:
        home_sp = team_sp_avg_df.loc[home_team]
    else:
        home_sp = sp_stats_df.loc[home_sp_id]

    if away_sp_id is None or away_sp_id not in sp_stats_df.index:
        away_sp = team_sp_avg_df.loc[away_team]
    else:
        away_sp = sp_stats_df.loc[away_sp_id]

    # add team features
    for feature in team_stats_df.columns:
        row[f"home_{feature}"] = home_features[feature]
        row[f"away_{feature}"] = away_features[feature]

    # add starting pitcher features
    for feature in sp_stats_df.columns:
        if feature in ["name", "team"]:
            continue

        row[f"home_sp_{feature}"] = home_sp[feature]
        row[f"away_sp_{feature}"] = away_sp[feature]
        row[f"diff_sp_{feature}"] = (
            home_sp[feature] - away_sp[feature]
        )

    # prediction dataframe
    df = pd.DataFrame([row]).fillna(0)

    # generate predictions from both models
    rf_pred = rf_model.predict(df)
    xgb_pred = xgb_model.predict(df)

    # ensemble prediction
    pred = (rf_pred + xgb_pred) / 2

    home_runs = round(pred[0][0])
    away_runs = round(pred[0][1])

    print(f"{home_team}: {home_runs}")
    print(f"{away_team}: {away_runs}")

    return home_runs, away_runs


# test it
if __name__ == "__main__":
    predict_game(
        'Cardinals',       # home
        'Diamondbacks',    # away
        'Martin Perez',    # home SP
        'Kyle Harrison'    # away SP
    )

