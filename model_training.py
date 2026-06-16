from game_dataset_builder import game_df
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error
#import pandas as pd
import optuna
import joblib

#prediction target matrix
y = game_df[["home_runs", "away_runs"]]

X = game_df.drop(columns=[
    "home_runs",
    "away_runs",
    "home_team",
    "away_team",
    "season",
    "date/time",
    "weight"

 
], errors= 'ignore')

X =X.fillna(0) #fill nan cols with 0 for RF

X_train, X_test, y_train, y_test = train_test_split(
X,
y,
test_size = 0.2,
random_state= 42
)


#original model before hyper param tuning
'''model = MultiOutputRegressor(
    RandomForestRegressor(
        n_estimators = 200,
        random_state= 42
    )
  )

model.fit(X_train, y_train)'''

#original model fit
'''
print(X.shape) 
print(X.isnull().sum().sum())
'''

#original model estimator importances
'''
#importances = model.estimators_[0].feature_importances_
#feature_imp = pd.Series(importances, index = X.columns)
#print(feature_imp.sort_values(ascending=False).head(20))
'''


#hyper param order
    # 1.suggest params, 2. build model, 3.evaluate, 4. return 
def objective(trial):

    #define params
    n_estimators = trial.suggest_int('n_estimators', 100, 500)
    max_depth = trial.suggest_int('max_depth', 5, 30)
    min_samples_split = trial.suggest_int('min_samples_split', 2, 20)
    min_samples_leaf = trial.suggest_int('min_samples_leaf', 1, 10)

    #build model w params
    model = MultiOutputRegressor(
        RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split= min_samples_split,
            min_samples_leaf= min_samples_leaf,
            random_state= 42,
            n_jobs=-1

            )
        )

    #cross validation here evalutes mae across both 
    scores = cross_val_score(
        model, X_train, y_train,
        cv=3,
        scoring = 'neg_mean_absolute_error',
        n_jobs =-1
        )

    return -scores.mean()

#Create and run Optuna study to optimize the Random Forest hyperparameters.
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials = 50)

#final model
best_params = study.best_trial.params

final_model = MultiOutputRegressor(
    RandomForestRegressor(
        n_estimators=best_params['n_estimators'],
        max_depth=best_params['max_depth'],
        min_samples_split=best_params['min_samples_split'],
        min_samples_leaf=best_params['min_samples_leaf'],
        random_state=42,
        n_jobs=-1
    )
)

final_model.fit(X_train, y_train)

print("Best Params:", study.best_params)
print("Best CV MAE:", study.best_value)

preds = final_model.predict(X_test)




home_mae = mean_absolute_error(
    y_test["home_runs"],
    preds[:,0]
)

away_mae = mean_absolute_error(
    y_test["away_runs"],
    preds[:,1]
)

print("Home MAE:", home_mae)
print("Away MAE", away_mae)
overall_mae = (home_mae + away_mae) / 2
print("Overall MAE:", overall_mae)



joblib.dump(final_model, "mlb_run_model.pkl")




