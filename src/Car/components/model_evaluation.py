import os
import pickle
import sys
from src.Car.loggers import logger
from src.Car.exception import CarException
from src.Car.utils.utils import load_pickle,read_yaml
import numpy as np
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score

class ModelEvaluation:
    def __init__(self,config_path="config/config.yml"):
        try:
            cfg=read_yaml(config_path)['default']
            self.preprocessor_path=os.path.join(cfg["artifacts_dir"],cfg['preprocessor_file'])
            self.model_path=os.path.join(cfg['artifacts_dir'],"models",cfg['trained_model_file'])   # added models here

        except Exception as e:
            logger.exception("Model Evaluation init failed")
            raise CarException("Model Evaluation failed",sys) from e
        
    def evaluate(self,transformed_test_path:str):
        try:
            '''# check that model file exists
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model file not found at {self.model_path}")
            print("model path being loaded:",self.model_path)'''
            
            # load the model 
            '''with open(self.model_path,"rb") as f:
                model=pickle.load(f)'''
            model=load_pickle(self.model_path)
            test_arr=np.load(transformed_test_path)
            X_test=test_arr[:,:-1]
            y_test=test_arr[:,-1]
            preds=model.predict(X_test)
            metrics={
                "mse":mean_squared_error(y_test,preds),
                "mae":mean_absolute_error(y_test,preds),
                "R2":r2_score(y_test,preds)
            }
            return metrics
        
        except Exception as e:
             logger.info("Model evaluation failed")
             raise CarException("Model evaluation failed",sys) from e