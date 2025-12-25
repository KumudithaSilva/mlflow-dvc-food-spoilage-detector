from pipeline.stage_01_data_ingestion import DataIngestionTraningPipeline
from pipeline.state_02_data_preprocess import DataPreprocessTraningPipeline
from pipeline.state_03_prepare_base_model import \
    PrepareBaseModelTraningPipeline
from pipeline.state_04_model_training import TraningPipeline
from pipeline.stage_05_model_evaluation import EvaluationPipeline
from utils import logger

STAGE_NAME = "Data Ingestion Stage"

try:
    logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
    data_ingestion = DataIngestionTraningPipeline()
    data_ingestion.main()
    logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<< \n\n")
except Exception as e:
    logger.exception(f">>>>> STAGE {STAGE_NAME} ERROR {e} <<<<< \n\n")


STAGE_NAME = "Data Preprocssing Stage"

try:
    logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
    prepare_base_model = DataPreprocessTraningPipeline()
    prepare_base_model.main()
    logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<< \n\n")
except Exception as e:
    logger.error(f">>>>> STAGE {STAGE_NAME} ERROR {e} <<<<< \n\n")


STAGE_NAME = "Prepare Base Model Stage"

try:
    logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
    prepare_base_model = PrepareBaseModelTraningPipeline()
    prepare_base_model.main()
    logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<< \n\n")
except Exception as e:
    logger.error(f">>>>> STAGE {STAGE_NAME} ERROR {e} <<<<< \n\n")


STAGE_NAME = "Model Training Stage"

try:
    logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
    train_base_model = TraningPipeline()
    train_base_model.main()
    logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<< \n\n")
except Exception as e:
    logger.exception(f">>>>> STAGE {STAGE_NAME} ERROR {e} <<<<< \n\n")


STAGE_NAME = "Model Evaluation Stage"

try:
    logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
    model_eval = EvaluationPipeline()
    model_eval.main()
    logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<< \n\n")
except Exception as e:
        logger.exception(f">>>>> STAGE {STAGE_NAME} ERROR {e} <<<<< \n\n")