from dataclasses import dataclass

@dataclass
class DataIngestionConfg:
    dataset_path: str
    artifacts_dir: str

@dataclass
class DataValidationConfig:
    required_columns:list 

@dataclass 
class DataTransformationConfig:
    numeric_features: list
    categorical_features: list
    preprocessor_path:str

@dataclass
class ModelTrainerConfig:
    models_dir: str
    trained_model_file: str
    test_size: float
    random_state: int
    