import os 
from src.Car.loggers import logger
from src.Car.exception import CarException
from src.Car.utils.utils import read_yaml
from src.Car.components.data_ingestion import DataIngestion
from src.Car.components.data_validation import DataValidation
from src.Car.components.data_transformation import DataTransformation
from src.Car.components.model_trainer import ModelTrainer
from src.Car.components.model_evaluation import ModelEvaluation

def start_training(config_path="config/config.yml"):
    cfg=read_yaml(config_path)["default"]
    artifacts_dir=cfg["artifacts_dir"]
    os.makedirs(artifacts_dir,exist_ok=True)

    # Ingestion 
    ingestion=DataIngestion(config_path=config_path)
    ingestion_artifact=ingestion.initiate_data_ingestion()

    # Validation
    validation=DataValidation(config_path=config_path)
    validation_artifact=validation.initiate_data_validation(ingestion_artifact.dataset_path)
    logger.info(f"Validation result: {validation_artifact}")

    # Transformation
    transformation=DataTransformation(config_path=config_path)
    transformation_artifact=transformation.initiate_data_transformation(ingestion_artifact.dataset_path)

    # Training
    trainer=ModelTrainer(config_path=config_path)
    trainer_artifact=trainer.initiate_model_trainer(
        transformed_train_path=transformation_artifact.transformed_train_path,
        transformed_test_path=transformation_artifact.transformed_test_path
    )

    # Evaluation
    evaluator=ModelEvaluation(config_path=config_path)
    metrics=evaluator.evaluate(transformation_artifact.transformed_test_path)
    logger.info(f"final model metrics: {metrics}")

    return {
        "ingestion": ingestion_artifact,
        "validation": validation_artifact,
        "transfromation": transformation_artifact,
        "trainer": trainer_artifact,
        "evaluation": metrics
    }

if __name__=="__main__":
    start_training()