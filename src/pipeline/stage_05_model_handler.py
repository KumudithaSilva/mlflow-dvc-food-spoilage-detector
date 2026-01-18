# Pipeleline
from components.model_handler import ModelHandler
from config.configuration import ConfigurationManager
from utils import logger

STAGE_NAME = "Model Handler Stage"

class ModelHandlerPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            # Initialize the ConfigurationManager
            config = ConfigurationManager()
            # Get the config yaml file details
            model_handle_config = config.get_model_handler_config()
            # Initialize the ModelHandler
            model_handle = ModelHandler(model_handle_config)
            # Load the model
            model_handle.load_model()

        except Exception as e:
            raise e
    
        
if __name__ == "__main__":
    try:
        logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
        model_handle = ModelHandlerPipeline()
        model_handle.main()
        logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<< \n\n")
    except Exception as e:
        logger.exception(f">>>>> STAGE {STAGE_NAME} ERROR {e} <<<<< \n\n")
