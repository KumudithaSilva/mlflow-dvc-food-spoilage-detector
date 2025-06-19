from entity.config_entity import DataIngestionConfig
import os
import zipfile
import gdown
from utils import logger

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self)-> str:
        try:
            dataset_url = self.config.source_URL
            zip_donwload_dir = self.config.local_datafile
            os.makedirs("artifacts/data_ingestion", exist_ok=True)
            logger.info(f"Donwloaded data from {dataset_url} into file {zip_donwload_dir}")

            file_id = dataset_url.split("/")[-2]
            prefix_url = "https://drive.google.com/uc?/export=download&id="
            gdown.download(prefix_url+file_id, zip_donwload_dir)
        
        except Exception as e:
            raise e
    
    def extract_zip_file(self):
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_datafile, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)