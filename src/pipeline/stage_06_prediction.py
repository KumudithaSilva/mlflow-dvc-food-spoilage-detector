from pathlib import Path
from components.prediction import Prediction
from config.configuration import ConfigurationManager
from utils import logger

STAGE_NAME = "Prediction Stage"

class PredictionPipeline:
    def __init__(self):
            # Initialize the ConfigurationManager
            config_manager = ConfigurationManager()
            # Get the prediction config
            self.pred_config = config_manager.get_prediction_config()
            # Initialize the Prediction class
            self.predictor = Prediction(config=self.pred_config)
    

    def run(self, image_paths: list[Path]):
        """
        Run prediction on provided images
        """
        return self.predictor.predict(image_paths)
    

if __name__ == "__main__":
    try:
        logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")

        images = [
            Path("object_store/prediction_data/p1.png"),
            Path("object_store/prediction_data/p2.png")
        ]

        pipeline = PredictionPipeline()
        output = pipeline.run(images)

        logger.info(f"Prediction Output: {output}")
        logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<< \n\n")

    except Exception as e:
        logger.exception(f">>>>> STAGE {STAGE_NAME} ERROR {e} <<<<< \n\n")
