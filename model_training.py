#from game_dataset_builder import game_df 
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error
import pandas as pd
import optuna
import joblib

#prediction target matrix
game_df=pd.read_pickle('game_df.pkl')
y = game_df[["home_runs", "away_runs"]]

X = game_df.drop(columns=[
    "home_runs",
    "away_runs",
    "home_team",
    "away_team",
    "season",
    "date/time"
  

 
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



# 1.suggest params, 2. build model, 3.evaluate, 4. return 


#random forrest
def rf_objective(rf_trial):

    #define params Random forrest 
    rf_n_estimators = rf_trial.suggest_int('rf_n_estimators', 100, 500)
    rf_max_depth = rf_trial.suggest_int('rf_max_depth', 5, 30)
    rf_min_samples_split = rf_trial.suggest_int('rf_min_samples_split', 2, 20)
    rf_min_samples_leaf = rf_trial.suggest_int('rf_min_samples_leaf', 1, 10)
   

    #build rf  model w params
    
    rf_model = MultiOutputRegressor(
        RandomForestRegressor(
            n_estimators=rf_n_estimators,
            max_depth=rf_max_depth,
            min_samples_split= rf_min_samples_split,
            min_samples_leaf= rf_min_samples_leaf,
            random_state= 42,
            n_jobs=-1

            )
        )
    
    #cross validation here evalutes mae 
    scores = cross_val_score(rf_model, X_train, y_train,
        cv=3,
        scoring = 'neg_mean_absolute_error',
        n_jobs =-1
        )

    return -scores.mean()


    #Xgboost
def xgb_objective(xgboost_trial):
 #define xgboost params
    
    xgboost_n_estimators = xgboost_trial.suggest_int('xgb_n_estimators', 100, 500)
    xgboost_max_depth = xgboost_trial.suggest_int('xgb_max_depth', 3, 10)
    xgboost_learning_rate = xgboost_trial.suggest_float('xgb_learning_rate', 0.01, 0.3)
    xgboost_subsample = xgboost_trial.suggest_float('xgb_subsample', 0.6, 1.0)
    xgboost_colsample_bytree = xgboost_trial.suggest_float('xgb_colsample_bytree', 0.6, 1.0)

     #build xgboost model  w params 
        
    xgboost_model = MultiOutputRegressor(
        XGBRegressor(
            n_estimators=xgboost_n_estimators,
            max_depth=xgboost_max_depth,
            learning_rate=xgboost_learning_rate,
            subsample=xgboost_subsample,
            colsample_bytree=xgboost_colsample_bytree,
            random_state=42,
            n_jobs=-1
            )
        )


     #cross validation here evalutes mae a
    scores = cross_val_score(xgboost_model, X_train, y_train,
        cv=3,
        scoring = 'neg_mean_absolute_error',
        n_jobs =-1
         )
    
    return -scores.mean()
    
    

#Start optuna hyper param 


#Create and run Optuna study to optimize the Random Forest + Xgb hyperparameters.

print("Random forrest model running")
rf_study = optuna.create_study(direction='minimize')
rf_study.optimize(rf_objective, n_trials = 10)
print("------------------------------------------------------------------------------")


xgb_study = optuna.create_study(direction='minimize')
xgb_study.optimize(xgb_objective, n_trials = 10)


#final model rf best params
rf_best_params = rf_study.best_trial.params


#final model xgb best params
print("XGboost model running")
xgb_best_params = xgb_study.best_trial.params
print("------------------------------------------------------------------------------")


#final random forrest model given best params

final_rf_model = MultiOutputRegressor(
    RandomForestRegressor(
        n_estimators=rf_best_params['rf_n_estimators'],
        max_depth=rf_best_params['rf_max_depth'],
        min_samples_split=rf_best_params['rf_min_samples_split'],
        min_samples_leaf=rf_best_params['rf_min_samples_leaf'],
        random_state=42,
        n_jobs=-1
    )
)


#final xgboost model given best params

final_xgboost_model = MultiOutputRegressor(
    XGBRegressor(
        n_estimators=xgb_best_params['xgb_n_estimators'],
        max_depth=xgb_best_params['xgb_max_depth'],
        learning_rate=xgb_best_params['xgb_learning_rate'],
        subsample=xgb_best_params['xgb_subsample'],
        colsample_bytree=xgb_best_params['xgb_colsample_bytree'],
        random_state=42,
        n_jobs=-1
    )
)

#fit both rf and xgb  final models
final_rf_model.fit(X_train, y_train)
final_xgboost_model.fit(X_train, y_train)

joblib.dump(final_rf_model, 'rf_model.pkl')
joblib.dump(final_xgboost_model, 'xgb_model.pkl')

print("RF and XGBoost models saved.")

#generate predictions from rf and xgb
rf_preds = final_rf_model.predict(X_test)
xgb_preds = final_xgboost_model.predict(X_test)

#create rf + xgb ensamble
ensemble_preds = (rf_preds + xgb_preds) / 2

rf_importances = final_rf_model.estimators_[0].feature_importances_
rf_feature_imp = pd.Series(rf_importances, index = X.columns)
print("THE MOST IMPORTANT RANDOM FORREST FEATURES ARE...")
print(rf_feature_imp.sort_values(ascending=False).head(20))
print("---------------------------------------------------------------------------------------")

xgb_importances = final_xgboost_model.estimators_[0].feature_importances_
xgb_feature_imp = pd.Series(xgb_importances, index = X.columns)
print("tHE MOST IMPORTANT xgBOOST FEATURES ARE...")
print(xgb_feature_imp.sort_values(ascending=False).head(20))


#print("Best Params:", study.best_params)
#print("Best CV MAE:", study.best_value)

#preds = final_model.predict(X_test)



print("After combining the Xgboost and RF models...")
home_mae = mean_absolute_error(
    y_test["home_runs"],
    ensemble_preds[:, 0]
)

away_mae = mean_absolute_error(
    y_test["away_runs"],
    ensemble_preds[:, 1]
)

overall_mae = (home_mae + away_mae) / 2

print("Home MAE:", home_mae)
print("Away MAE:", away_mae)
print("Overall MAE:", overall_mae)




