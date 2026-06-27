from predict_game import predict_game 

def easy_predict():
    home_team = input("Enter Home Team")
    away_team = input("Enter Away Team")
    home_sp = input("Enter Home Starting Pitcher")
    away_sp = input("Enter away Starting pitcher")

    predict_game(home_team, away_team, home_sp, away_sp)

easy_predict()