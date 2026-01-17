import boto3
from pathlib import Path
from ensure import ensure_annotations
from utils import logger

class S3Client:
    def __init__(self, region_name: str):
        self.client = boto3.client("s3", region_name=region_name)
    
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