from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    dataset_path: str

@dataclass
class DataValidationArtifact:
    validated: bool
    message: str

@dataclass
class DataTransformationArtifact:
    preprocessor_path: str
    transformed_train_path: str
    transformed_test_path: str

@dataclass 
class ModelTrainerArtifact:
    model_path: str
    model_name: str
    metrics: dict