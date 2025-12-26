# Pipeleline
from components.data_ingestion import DataIngestion
from config.configuration import ConfigurationManager
from utils import logger

STAGE_NAME = "Data Ingestion Stage"


class DataIngestionTraningPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            # Initilize the ConfigurationManager
            config = ConfigurationManager()
            # Get the config yaml file details
            data_ingestion_config = config.get_data_ingestion_config()
            # Initilize the DataIngestion
            data_ingestion = DataIngestion(config=data_ingestion_config)
            # Call download file
            data_ingestion.download_file()
            # Call unzip file
            data_ingestion.extract_zip_file()
            # Move and cleanup
            data_ingestion.moved_and_cleanup()
        except Exception as e:
            raise e


if __name__ == "__main__":
    try:
        logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
        data_ingestion = DataIngestionTraningPipeline()
        data_ingestion.main()
        logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<< \n\n")
    except Exception as e:
        logger.exception(f">>>>> STAGE {STAGE_NAME} ERROR {e} <<<<< \n\n")
