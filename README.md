# MLB Game Score Prediction Model
A machine learning pipeline that predicts MLB game scores using team statistics, Sagarin-style power ratings, and starting pitcher matchups. Built entirely in Python using the MLB Stats API, scikit-learn, and Optuna.


## Pipeline Overview

### 1. Sagarin Ratings (`sagarin_model.py`)
Pulls multiple seasons of game results from the MLB Stats API and solves for team power ratings using least squares regression. Recent seasons are weighted more heavily. Outputs `sagarin_ratings.json`.

### 2. Player & Team Mapping (`players_to_team.py`)
Maps every player to their respective team roster using the MLB Stats API. Outputs `team_data.json`.

### 3. Player Stats (`stats_to_players.py`)
Pulls individual season stats for every player and associates them with their team. Outputs `team_data_with_stats.json`.

### 4. Team Level Aggregation (`team_hitting.py`, `team_pitching.py`)
Aggregates individual player stats to team level using plate appearance and innings pitched weighted averages. Outputs `team_data_with_batting.json` and `team_data_with_pitching.json`.

### 5. Feature Engineering (`team_features.py`, `player_pitching.py`)
Combines Sagarin ratings with team batting stats into a unified feature DataFrame. Builds a separate starting pitcher DataFrame indexed by player ID with team average fallback for missing starters.

### 6. Game Level Dataset (`game_level.py`, `game_dataset_builder.py`)
Pulls every game from the current season and constructs a game level dataset matching team features with starting pitcher stats. Final DataFrame: ~663 games × 104 features.

### 7. Model Training (`model_training.py`)
Trains a `MultiOutputRegressor` wrapping a `RandomForestRegressor` to simultaneously predict home and away runs. Hyperparameters tuned with Optuna and cross validation.


## Data Pipeline Execution Order
sagarin_model.py
players_to_team.py
stats_to_players.py
team_hitting.py
team_pitching.py
team_features.py
player_pitching.py
game_dataset_builder.py
model_training.py
predict_game.py


## MAE
Home MAE: ~2.42
Away MAE: ~2.60