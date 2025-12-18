from pathlib import Path
from constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from entity.config_entity import (
    DataIngestionConfig,
    DataPreprocessingConfig,
    PrepareBaseModelConfig,
)
from utils.base_utils import create_directories, read_yaml


class ConfigurationManager:

    def __init__(self, config_filepath=CONFIG_FILE_PATH, param_path=PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.param = read_yaml(param_path)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_datafile=config.local_datafile,
            unzip_dir=config.unzip_dir,
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
            params_image_size=self.param.IMAGE_SIZE,
            params_learning_rate=self.param.LEARNING_RATE,
            params_include_top=self.param.INCLUDE_TOP,
            params_weights=self.param.WEIGHTS,
            params_classes=self.param.CLASSES,
        )
        return prepare_base_model_config
