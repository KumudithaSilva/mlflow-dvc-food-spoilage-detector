# Pipeleline
from components.model_evaluation import ModelEvaluation
from config.configuration import ConfigurationManager
from utils import logger

STAGE_NAME = "Model Evaluation Stage"

class EvaluationPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            # Initilize the ConfigurationManager
            config = ConfigurationManager()
            # Get the config yaml file details
            eval_config = config.get_evaluation_config()
            # Initialize the ModelEvaluation class
            model_eval = ModelEvaluation(config=eval_config)
            # Create the validation generator
            model_eval.validation_generator()
            # Evaluate the model
            model_eval.evaluate_model()
            # Save the evaluation report
            model_eval.save_evaluation_report()
            # Configure mlflow
            model_eval.configure_mlflow()
            # Log evaluation metrics to mlflow
            model_eval.log_evaluation_metrics()
        except Exception as e:
            raise e
    
        
if __name__ == "__main__":
    try:
        logger.info(f">>>>> STAGE {STAGE_NAME} STARTED <<<<<")
        model_eval = EvaluationPipeline()
        model_eval.main()
        logger.info(f">>>>> STAGE {STAGE_NAME} COMPLETED <<<<< \n\n")
    except Exception as e:
        logger.exception(f">>>>> STAGE {STAGE_NAME} ERROR {e} <<<<< \n\n")
