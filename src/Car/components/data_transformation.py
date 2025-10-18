import os 
import sys
import numpy as np
import pandas as pd
from src.Car.loggers import logger
from src.Car.exception import CarException 
from src.Car.utils.utils import read_yaml,save_pickle
from src.Car.entity.artifact_entity import DataTransformationArtifact
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer


class DataTransformation:
    def __init__(self,config_path="config/config.yml"):
        try:
            cfg=read_yaml(config_path)['default']
            self.numeric_features=cfg['numeric_features']
            self.categorical_features=cfg['categorical_features']
            self.artifacts_dir=cfg['artifacts_dir']
            self.preprocessor_path=os.path.join(cfg['artifacts_dir'],cfg['preprocessor_file'])
            os.makedirs(os.path.dirname(self.preprocessor_path),exist_ok=True)
        except Exception as e:
            logger.exception("Data transformation init error")
            raise CarException("Failed Data transformation init",sys) from e
        
    def get_preprocessor(self):
        try:
            num_pipeline=Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())
            ])
            cat_pipeline=Pipeline([
                ("imputer",SimpleImputer(strategy='most_frequent')),
                ("onehot",OneHotEncoder(handle_unknown="ignore",sparse_output=False))
            ])
            preprocessor=ColumnTransformer(transformers=[
                ('num',num_pipeline,self.numeric_features),
                ('cat',cat_pipeline,self.categorical_features)
            ])
            return preprocessor
        except Exception as e:
            logger.exception("Failed to create preprocessor")
            raise CarException("Preprocessor creation failed",sys) from e
        
    def initiate_data_transformation(self,input_data_path:str)-> DataTransformationArtifact:
        try:
            df=pd.read_csv(input_data_path)
            cfg=read_yaml("config/config.yml")['default']
            target=cfg['target_column']

            #split train and test data
            from sklearn.model_selection import train_test_split
            X=df.drop(columns=[target])
            y=df[target]

            X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=cfg['test_size'],random_state=cfg['random_state'])

            preprocessor= self.get_preprocessor()
            
            #fit on training data
            preprocessor.fit(X_train)
            
            #transform
            X_train_transformed=preprocessor.transform(X_train)
            X_test_transformed=preprocessor.transform(X_test)

            # save transformed arrays with target appended (for trainer convenience)
            train_arr=np.concatenate([X_train_transformed,np.array(y_train).reshape(-1,1)],axis=1)
            test_arr=np.concatenate([X_test_transformed,np.array(y_test).reshape(-1,1)],axis=1)

            transformed_train_path=os.path.join(self.artifacts_dir,"transformed",'train.npy')
            transformed_test_path=os.path.join(self.artifacts_dir,"transformed",'test.npy')
            os.makedirs(os.path.dirname(transformed_train_path),exist_ok=True)
            np.save(transformed_train_path,train_arr)
            np.save(transformed_test_path,test_arr)

            # save preprocessor
            save_pickle(preprocessor,self.preprocessor_path)
            logger.info("data transformation completed.")
            return DataTransformationArtifact(
                preprocessor_path=self.preprocessor_path,
                transformed_train_path=transformed_train_path,
                transformed_test_path=transformed_test_path
            )
        except Exception as e:
            logger.exception("data transformation failed")
            raise CarException("Data transformation failed",sys) from e