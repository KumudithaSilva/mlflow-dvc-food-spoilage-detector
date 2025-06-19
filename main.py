from utils import logger
from pipeline.stage_01_data_ingestion import DataIngestionTraningPipeline

STAGE_NAME = "Data Ingestion Stage"        

try:
    logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
    data_ingestion = DataIngestionTraningPipeline()
    data_ingestion.main()
    logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<< \n\n")
except Exception as e:
    logger.exception(f">>>>> STAGE {STAGE_NAME} ERROR {e} <<<<< \n\n")