from pathlib import Path
from components.prediction import Prediction
from config.configuration import ConfigurationManager
from utils import logger

STAGE_NAME = "Prediction Stage"

class PredictionPipeline:
    def __init__(self, image_paths: list[Path]):
        self.image_paths = image_paths

    def main(self):
        try:
            # Initilize the ConfigurationManager
            config_manager = ConfigurationManager()
            # Get the prediction config
            pred_config = config_manager.get_prediction_config()
            # Initialize the Prediction class
            predictor = Prediction(config=pred_config)
            # Perform predictions
            results = predictor.predict(self.image_paths)

            return results

        except Exception as e:
            raise e


if __name__ == "__main__":
    try:
        logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")

        images = [
            Path("prediction_data/p1.png"),
            Path("prediction_data/p2.png")
        ]

        pipeline = PredictionPipeline(images)
        output = pipeline.main()

        logger.info(f"Prediction Output: {output}")
        logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<< \n\n")

    except Exception as e:
        logger.exception(f">>>>> STAGE {STAGE_NAME} ERROR {e} <<<<< \n\n")
