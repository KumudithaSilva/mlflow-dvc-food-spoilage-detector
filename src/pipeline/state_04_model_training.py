# Pipeleline
from components.model_training import Training
from config.configuration import ConfigurationManager
from utils import logger

STAGE_NAME = "Model Training Stage"


class TraningPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            prepare_train_model_config = config.get_training_config()
            prepare_train_model = Training(config=prepare_train_model_config)
            prepare_train_model.get_based_model()
            prepare_train_model.train_valid_generator()
            prepare_train_model.train()
            prepare_train_model.save_model()
        except Exception as e:
            raise e


if __name__ == "__main__":
    try:
        logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
        train_base_model = TraningPipeline()
        train_base_model.main()
        logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<< \n\n")
    except Exception as e:
        logger.exception(f">>>>> STAGE {STAGE_NAME} ERROR {e} <<<<< \n\n")
