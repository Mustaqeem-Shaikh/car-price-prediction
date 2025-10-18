import os
import sys
from src.Car.exception import CarException
from src.Car.loggers import logger
from src.Car.utils.utils import read_yaml, read_csv
from src.Car.entity.artifact_entity import DataIngestionArtifact


class DataIngestion:
    def __init__(self,config_path:str = "config/config.yml"):
        try:
            self.config=read_yaml(config_path)['default']
            self.dataset_path=self.config['dataset_path']
            self.artifacts_dir=self.config["artifacts_dir"]
            os.makedirs(self.artifacts_dir,exist_ok=True)
        except Exception as e:
            logger.exception("Error in Dataingestion init")
            raise CarException("Failed to Dataingestion init",sys) from e 
        
    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            if not os.path.exists(self.dataset_path):
                raise FileNotFoundError(f"Dataset not found at {self.dataset_path}")
            df= read_csv(self.dataset_path)
            target_path=os.path.join(self.artifacts_dir,"data","raw_data.csv")
            os.makedirs(os.path.dirname(target_path),exist_ok=True)
            df.to_csv(target_path,index=False)
            logger.info(f"Data ingestion completed. Data saved to {target_path}")
            
            return DataIngestionArtifact(dataset_path=target_path)
        except Exception as e:
            logger.exception("failed during data ingestion")
            raise CarException("Data ingestion failed",sys) from e
    