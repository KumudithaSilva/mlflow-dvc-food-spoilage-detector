# Pipeleline
from components.prepare_base_model import PrepareBaseModel
from config.configuration import ConfigurationManager
from utils import logger

STAGE_NAME = "Prepare Base Model Stage"


class PrepareBaseModelTraningPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            prepare_base_model_config = config.get_prepare_base_model_config()
            prepare_base_model = PrepareBaseModel(config=prepare_base_model_config)
            prepare_base_model.get_base_model()
            prepare_base_model.update_base_model()
        except Exception as e:
            raise e


if __name__ == '__main__':
    try:
        logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
        prepare_base_model = PrepareBaseModelTraningPipeline()
        prepare_base_model.main()
        logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<< \n\n")
    except Exception as e:
        logger.exception(f">>>>> STAGE {STAGE_NAME} ERROR {e} <<<<< \n\n")
