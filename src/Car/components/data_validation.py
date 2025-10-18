import os 
import sys
from src.Car.loggers import logger
from src.Car.exception import CarException
from src.Car.utils.utils import read_csv,read_yaml
from src.Car.entity.artifact_entity import DataValidationArtifact

class DataValidation:
    def __init__(self,config_path="config/config.yml"):
        try:
            cfg= read_yaml(config_path)["default"]
            self.required_columns=[
                "name","year","selling_price","fuel","transmission","km_driven","owner"
            ]
            self.dataset_path=cfg["dataset_path"]
        except Exception as e:
            logger.exception("Datavalidation init error")
            raise CarException("Failed Datavalidation init",sys) from e
    
    def initiate_data_validation(self,data_path: str) ->DataValidationArtifact:
        try:
            df= read_csv(data_path)
            missing=[c for c in self.required_columns if c not in df.columns]
            if missing:
                msg=f"missing columns: {missing}"
                logger.error(msg)
                return DataValidationArtifact(validated=False,message=msg)
            
            # basic checks 
            if df.isnull().sum().sum() > 0:
                msg="Null values found in dataset - please handle them or drop them."
                logger.warning(msg)
                
                #still return validated true so transformation can handle; or choose false
                return DataValidationArtifact(validated=True,message=msg)
            return DataValidationArtifact(validated=True,message="all required columns present")
        except Exception as e:
            logger.exception("Data validation failed ")
            raise CarException("Data validation failed ",sys) from e