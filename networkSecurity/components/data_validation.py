from networkSecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networkSecurity.entity.config_entity import DataValidationConfig
from networkSecurity.exception.exception import NetworkSecurityException 
from networkSecurity.logging.logger import logging 
from networkSecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
import os,sys
from networkSecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod    
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config)
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Dataframe has columns: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    
    def validate_numerical_columns_exist(self, dataframe: pd.DataFrame) -> bool:
        try:
            numerical_columns = dataframe.select_dtypes(include=[np.number]).columns
            if len(numerical_columns) > 0:
                logging.info(f"Numerical columns found: {list(numerical_columns)}")
                return True
            else:
                logging.info("No numerical columns found.")
                return False

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(self, base_df, current_df, threshold=0.05):
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({
                    column: {
                        "p_value": float(is_same_dist.pvalue),
                        "drift_status": is_found
                    }
                })
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            # Creating Directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report) 

        except Exception as e:
            raise NetworkSecurityException(e, sys)



    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            ## Read the train and test data
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            ## Validate the number of columns
            status=self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message=f"Train dataframe does not contain all columns.\n"

            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message=f"Test dataframe does not contain all columns.\n"  

            ## Validate the numerical columns exist or not 
            status = self.validate_numerical_columns_exist(dataframe=train_dataframe)
            if not status:
                error_message=f"Train dataframe does not contain any numerical columns.\n"

            status = self.validate_numerical_columns_exist(dataframe=test_dataframe)
            if not status:
                error_message=f"Test dataframe does not contain any numerical columns.\n"
             
            ## Checking Data Drift
            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
            