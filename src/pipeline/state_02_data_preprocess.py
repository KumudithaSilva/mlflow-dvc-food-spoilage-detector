# Pipeleline
from components.data_preprocessing import DataPreprocessing
from config.configuration import ConfigurationManager
from utils import logger

STAGE_NAME = "Data Preprocssing Stage"


class DataPreprocessTraningPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            # Initilize the ConfigurationManager
            config = ConfigurationManager()
            # Get the config yaml file details
            data_preprocess_config = config.get_data_preprocess_config()
            # Initilize the DataPreprocessing
            data_preprocessing = DataPreprocessing(config=data_preprocess_config)
            # Call preprocess data
            data_preprocessing.reshape_extracted_data()
        except Exception as e:
            raise e


if __name__ == '__main__':
    try:
        logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
        data_preprocess = DataPreprocessTraningPipeline()
        data_preprocess.main()
        logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<< \n\n")
    except Exception as e:
        logger.exception(f">>>>> STAGE {STAGE_NAME} ERROR {e} <<<<< \n\n")
