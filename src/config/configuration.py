from constants import *
from entity.config_entity import DataIngestionConfig
from utils.base_utils import read_yaml, create_directories

class ConfigurationManager:

    def __init__(self, config_filepath = CONFIG_FILE_PATH, param_path = PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.param = read_yaml(param_path)
        
        create_directories([self.config.artifacts_root])


    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([self.config.artifacts_root])

        data_ingestion_config = DataIngestionConfig(
            root_dir = config.root_dir,
            source_URL = config.source_URL,
            local_datafile = config.local_datafile ,
            unzip_dir = config.unzip_dir
        )
        return data_ingestion_config