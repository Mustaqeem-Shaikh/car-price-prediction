import os 
import pickle
import pandas as pd 
import yaml
from src.Car.exception import CarException
from src.Car.loggers import logger

def read_yaml(path: str)-> dict:
    try:
        with open(path,"r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.exception("Failed to read yaml")
        raise CarException(f"Failed to read yaml file:{path}") from e
    
def save_pickle(obj,filepath: str):
    dirpath=os.path.dirname(filepath)
    os.makedirs(dirpath,exist_ok=True)
    with open(filepath,"wb") as f:
        pickle.dump(obj,f)

def load_pickle(filepath: str):
    with open(filepath,"rb") as f:
        return pickle.load(f)

def save_df(df: pd.DataFrame,path:str):
    dirpath=os.path.dirname(path)
    os.makedirs(dirpath,exist_ok=True)
    df.to_csv(path, index=False)

def read_csv(path:str):
    return pd.read_csv(path) 
