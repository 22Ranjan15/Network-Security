from networkSecurity.components.data_ingestion import DataIngestion
from networkSecurity.components.data_validation import DataValidation
from networkSecurity.components.data_transformation import DataTransformation
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
from networkSecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from networkSecurity.entity.config_entity import TrainingPipelineConfig
import sys

if __name__=='__main__':
    try:
        trainingpipelineconfig = TrainingPipelineConfig()

        ## Data Ingestion
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion.")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed.")
        print(dataingestionartifact)

        ## Data Validation
        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestionartifact, data_validation_config)
        logging.info("Initiate the data validation.")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation completed.")
        print(data_validation_artifact)

        ## Data Transformation
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        logging.info("Data Transformation started.")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data Transformation completed.")
        print(data_transformation_artifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)