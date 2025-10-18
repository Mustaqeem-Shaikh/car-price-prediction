import os
import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from src.Car.exception import CarException
from src.Car.loggers import logger
from src.Car.utils.utils import read_yaml,load_pickle

class PredictionPipeline:
    def __init__(self,config_path="config/config.yml"):
        try:
            cfg=read_yaml(config_path)['default']
            self.preprocessor_path=os.path.join(cfg['artifacts_dir'],cfg['preprocessor_file'])
            self.model_path=os.path.join(cfg['artifacts_dir'],"models",cfg["trained_model_file"])
            self.numeric_feautres=cfg["numeric_features"]
            self.categorical_features=cfg["categorical_features"]
            self.target=cfg["target_column"]
            self.preprocessor=load_pickle(self.preprocessor_path)
            self.model=load_pickle(self.model_path)
        
        except Exception as e:
            logger.exception(" Prediction Pipeline init failed")
            raise CarException(" Prediction pipeline init failed",sys) from e
    
    def predict(self,input_df:pd.DataFrame):
        try:
            X=input_df[self.numeric_feautres + self.categorical_features]
            X_transformed=self.preprocessor.transform(X)
            preds=self.model.predict(X_transformed)
            return preds
        
        except Exception as e:
            logger.exception("prediction failed")
            raise CarException("prediction failed",sys) from e 