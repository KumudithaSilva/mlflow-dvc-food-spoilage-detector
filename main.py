from pathlib import Path

from logger.logging_config import logger
from pipeline.stage_01_data_ingestion import DataIngestionTraningPipeline
from pipeline.stage_05_model_handler import ModelHandlerPipeline
from pipeline.stage_06_model_evaluation import EvaluationPipeline
from pipeline.stage_07_prediction import PredictionPipeline
from pipeline.state_02_data_preprocess import DataPreprocessTraningPipeline
from pipeline.state_03_prepare_base_model import \
    PrepareBaseModelTraningPipeline
from pipeline.state_04_model_training import TraningPipeline


def run_stage(stage_name: str, pipeline_class, *args, **kwargs):
    """
    Run any stage with standardized logging and exception handling.

    Args:
        stage_name (str): Name of the stage
        pipeline_class (type): The pipeline class to instantiate
        *args, **kwargs: Arguments to pass to the pipeline's main method
    """
    logger.info(f">>>>> STAGE {stage_name} STARTED <<<<<")
    try:
        pipeline = pipeline_class()

        # If the pipeline has a 'main' method, call it with args/kwargs
        if hasattr(pipeline, "main"):
            return pipeline.main(*args, **kwargs)

        logger.info(f">>>>> STAGE {stage_name} COMPLETED <<<<<\n\n")
    except Exception as e:
        logger.exception(f">>>>> STAGE {stage_name} ERROR: {e} <<<<<\n\n")
        raise


if __name__ == "__main__":
    # ------------------------
    # Run all stages
    # ------------------------

    # Data ingestion
    run_stage("Data Ingestion Stage", DataIngestionTraningPipeline)

    # Data preprocessing
    run_stage("Data Preprocessing Stage", DataPreprocessTraningPipeline)

    # Prepare base model
    run_stage("Prepare Base Model Stage", PrepareBaseModelTraningPipeline)

    #  Model training
    run_stage("Model Training Stage", TraningPipeline)

    # Model handler
    run_stage("Model Handler Stage", ModelHandlerPipeline)

    # Model evaluation
    run_stage("Model Evaluation Stage", EvaluationPipeline)

    # Prediction stage
    images_to_predict = [Path("temp/p1.png"), Path("temp/p2.png")]
    existing_images = [img for img in images_to_predict if img.exists()]
    if not existing_images:
        logger.warning("No images found to process. Skipping prediction stage.")
    else:
        prediction_output = run_stage(
            "Prediction Stage", PredictionPipeline, images_to_predict
        )
        logger.info(f"Final Prediction Output: {prediction_output}")
