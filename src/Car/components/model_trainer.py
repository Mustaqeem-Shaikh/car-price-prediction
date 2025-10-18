import os 
import sys
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error,r2_score,mean_absolute_error
from sklearn.model_selection import GridSearchCV
from src.Car.loggers import logger
from src.Car.exception import CarException
from src.Car.utils.utils import read_yaml,load_pickle,save_pickle
from src.Car.entity.artifact_entity import ModelTrainerArtifact

class ModelTrainer:
    def __init__(self,config_path='config/config,yml'):
        try:
            cfg=read_yaml(config_path)['default']
            self.models_dir=cfg["models_dir"] if 'models_dir' in cfg else os.path.join(cfg['artifact_dir'],"models")
            os.makedirs(self.models_dir,exist_ok=True)
            self.trained_model_file=os.path.join(self.models_dir,cfg["trained_model_file"])
            self.preprocessor_path=os.path.join(cfg["artifacts_dir"],cfg["preprocessor_file"])
            self.random_state=cfg["random_state"]
        except Exception as e:
            logger.exception("Model Trainer init failed ")
            raise CarException("Model Trainer init failed ",sys) from e 
        
    
    def _get_data(self,train_path: str,test_path: str):
        try:
            X_train=np.load(train_path)
            X_test=np.load(test_path)
            
            #last column is target 
            X_tr,y_tr=X_train[:,:-1],X_train[:,-1]
            X_te,y_te=X_test[:,:-1],X_test[:,-1]
            return X_tr,X_te,y_tr,y_te
        except Exception as e:
            logger.exception("failed reading transformed arrays")
            raise CarException("failed reading the transformed arrays",sys) from e
        
    
    def _evaluate(self,model,X,y):
        preds=model.predict(X)
        return {
            "mse":mean_squared_error(y,preds),
            "r2":r2_score(y,preds),
            "mae":mean_absolute_error(y,preds)
        }
    
    def initiate_model_trainer(self,transformed_train_path:str,transformed_test_path:str)-> ModelTrainerArtifact:
        try:
            X_tr,X_te,y_tr,y_te=self._get_data(transformed_train_path,transformed_test_path)

            # models to try
            models={
                "Linear Model": LinearRegression(),
                "Random model": RandomForestRegressor(random_state=self.random_state),
                "Gradient Boost": GradientBoostingRegressor(random_state=self.random_state)
            }

            # GridSearchCv params 
            params={
                "Random model":{
                    "n_estimators":[50,100],
                    "max_depth":[None,10]
                },
                "Gradient Boost":{
                    "n_estimators":[50,100],
                    "learning_rate":[0.05,0.1]
                }
            }

            best_model= None
            best_score=float("-inf")
            best_name=None
            best_metrics=None

            for name,model in models.items():
                logger.info(f"Training model name {name}")
                if name in params:
                    grid=GridSearchCV(estimator=model,param_grid=params[name],cv=3,n_jobs=1,scoring="r2")
                    grid.fit(X_tr,y_tr)
                    trained=grid.best_estimator_
                else:
                    model.fit(X_tr,y_tr)
                    trained = model
                
                metrics_train=self._evaluate(trained,X_tr,y_tr)
                metrics_test=self._evaluate(trained,X_te,y_te)
                logger.info(f"{name} train metrics: {metrics_train} | test metrics: {metrics_test}")


                #use test R2 to choose best 
                if metrics_test["r2"] > best_score:
                    best_score=metrics_test["r2"]
                    best_model=trained
                    best_name=name
                    best_metrics={"train": metrics_train, "test": metrics_test}
            
            # save best model along with preprocessor for convenience as a pipeline-like dict
            model_aritfact_path=self.trained_model_file
            save_pickle(best_model,model_aritfact_path)
            logger.info(f"Best model {best_name} save at {model_aritfact_path}")

            return ModelTrainerArtifact(
                model_path=model_aritfact_path,
                model_name=best_name,
                metrics=best_metrics
            )
        
        except Exception as e:
            logger.exception("model trainer failed")
            raise CarException("model trainer failed",sys) from e
