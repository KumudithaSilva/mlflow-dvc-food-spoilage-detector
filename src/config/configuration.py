import os
from pathlib import Path

from constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from entity.config_entity import (DataIngestionConfig, DataPreprocessingConfig,
                                  PrepareBaseModelConfig, TrainingConfig, EvaluationConfig)
from utils.base_utils import create_directories, read_yaml


class ConfigurationManager:

    def __init__(self, config_filepath=CONFIG_FILE_PATH, param_path=PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(param_path)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_datafile=config.local_datafile,
            unzip_dir=config.unzip_dir,
            data_folder=config.data_folder,
            moved_location=config.moved_location,
        )
        return data_ingestion_config

    def get_data_preprocess_config(self) -> DataPreprocessingConfig:
        config = self.config.data_preprocessing

        data_preproess_config = DataPreprocessingConfig(
            root_dir=config.root_dir,
            unzip_dir=config.unzip_dir,
            reshape_dir=config.reshape_dir,
            image_size=config.image_size,
        )
        return data_preproess_config

    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
        config = self.config.prepare_base_model

        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir=Path(config.root_dir),
            base_model_path=Path(config.base_model_path),
            updated_base_model_path=Path(config.updated_base_model_path),
            updated_base_model_image_path=Path(config.updated_base_model_image_path),
            params_image_size=self.params.IMAGE_SIZE,
            params_learning_rate=self.params.LEARNING_RATE,
            params_include_top=self.params.INCLUDE_TOP,
            params_weights=self.params.WEIGHTS,
            params_classes=self.params.CLASSES,
        )
        return prepare_base_model_config

    def get_training_config(self) -> TrainingConfig:
        training_config = self.config.training
        prepare_base_model_config = self.config.prepare_base_model
        params = self.params

        create_directories([training_config.root_dir])

        training_config = TrainingConfig(
            root_dir=Path(training_config.root_dir),
            trained_model_path=Path(training_config.trained_model_path),
            updated_base_model_path=Path(
                prepare_base_model_config.updated_base_model_path
            ),
            training_data=Path(training_config.training_data),
            params_epochs=params.EPOCHS,
            params_batch_size=params.BATCH_SIZE,
            params_is_augmentation=params.AUGMENTATION,
            params_image_size=params.IMAGE_SIZE,
            params_learning_rate=params.LEARNING_RATE,
            data_split_seed=params.SEED,
        )

        return training_config
    
    def get_evaluation_config(self) -> EvaluationConfig:
        eval_config = self.config.model_evaluation
        params = self.params

        create_directories([eval_config.root_dir])
        
        evaluation_config = EvaluationConfig(
            root_dir=Path(eval_config.root_dir),
            trained_model_path=Path(eval_config.trained_model_path),
            training_data=Path(eval_config.training_data),
            all_params=params,
            params_is_augmentation=params.AUGMENTATION,
            params_image_size=params.IMAGE_SIZE,
            params_batch_size=params.BATCH_SIZE,
            data_split_seed=params.SEED,
            reportfile=Path(eval_config.report_file),
        )
        return evaluation_config
