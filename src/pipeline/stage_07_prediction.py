from pathlib import Path
from components.model_handler import ModelHandler
from components.prediction import Prediction
from config.configuration import ConfigurationManager
from logger.logging_config import logger

STAGE_NAME = "Prediction Stage"

class PredictionPipeline:
    def __init__(self):
            # Initialize the ConfigurationManager
            config_manager = ConfigurationManager()
            # Get the prediction config
            pred_config = config_manager.get_prediction_config()
            # Get the Model Handler config
            model_handler_config = config_manager.get_model_handler_config()
            # Initialize the ModelHandler class
            model_handler = ModelHandler(config=model_handler_config)
            # Initialize the Prediction class
            self.predictor = Prediction(config=pred_config, model_handler=model_handler)

    

    def main(self, image_paths: list[Path]):
        """
        Run prediction on provided images
        """
        return self.predictor.predict(image_paths)
    

if __name__ == "__main__":
    try:
        logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")

        images = [
            Path("temp/p1.png"),
            Path("temp/p2.png")
        ]

        pipeline = PredictionPipeline()
        output = pipeline.main(images)

        logger.info(f"Prediction Output: {output}")
        logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<< \n\n")

    except Exception as e:
        logger.exception(f">>>>> STAGE {STAGE_NAME} ERROR {e} <<<<< \n\n")
