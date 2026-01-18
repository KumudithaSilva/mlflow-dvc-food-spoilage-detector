import boto3
from pathlib import Path
from ensure import ensure_annotations
from utils import logger
from utils.base_utils import load_env_variables

class S3Client:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, region_name: str = "us-east-1"):
        if getattr(self, "_initialized", False):
            return
        
        load_env_variables() 
        self.client = boto3.client("s3", region_name=region_name)
        self._initialized = True
    

    def upload_fileobj(self, file_obj, bucket: str, key: str) -> None:
        """
        Uploads a file object to an S3 bucket.

        Args:
            file_obj: The file object to be uploaded.
            bucket (str): The name of the S3 bucket.
            key (str): The key (file path) in the S3 bucket where the file will be stored.

        Returns:
            None
        """
        self.client.upload_fileobj(file_obj, bucket, key)
    
    # @ensure_annotations
    def upload_model(self, local_path: Path, bucket: str, key: str) -> None:
        """
        Saves Trained Model to AWS S3 bucket.

        Args:
            local_path (Path): Local path where model exists
            bucket (str): AWS S3 Bucket
            key (str): AWS S3 Key

        Raises:
            Exception: If Model Not Found
        """
        if not local_path.exists():
            logger.exception(f"Model local file path not found at {local_path}")
        self.client.upload_file(str(local_path), bucket, key)
    
    # @ensure_annotations
    def download_model(self, bucket: str, key: str, cache_path: Path) -> None:
        """
        Saves Trained Model to AWS S3 bucket.

        Args:
            cache_path (Path): Cache path where model exists temporary
            bucket (str): AWS S3 Bucket
            key (str): AWS S3 Key
        """
        self.client.download_file(Bucket=bucket,Key=key,Filename=str(cache_path))