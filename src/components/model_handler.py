from pathlib import Path
from threading import Lock

import tensorflow as tf

from entity.config_entity import ModelHandlerConfig
from utils.s3_utils import S3Client


class ModelHandler:
    """
    Handles ML model loading with lazy in-memory caching.
    """

    def __init__(self, config: ModelHandlerConfig):
        self.config = config
        self.s3_client = S3Client(region_name=config.aws.region)

        # Ensure cache folder exists
        self.config.cache_dir.mkdir(parents=True, exist_ok=True)

        # Lazy-loaded model cache
        self.model = None

        # Thread lock to ensure safe lazy loading
        self.model_lock = Lock()

    def load_model(self, force_reload: bool = False) -> tf.keras.Model:
        """
        Loads model from local cache or S3 if not cached yet.
        force_reload=True ignores cache and reloads from S3.
        Returns TensorFlow model.
        """
        with self.model_lock:
            if self.model is not None and not force_reload:
                return self.model

        local_model_cache_path = self.config.cache_dir / "model.h5"
        latest_key = f"{self.config.aws.s3.model_prefix}/latest/model.h5"

        if force_reload or not local_model_cache_path.exists():
            print(f"Downloading latest model from S3: {latest_key}")
            self.s3_client.download_model(
                bucket=self.config.aws.s3.bucket,
                key=latest_key,
                cache_path=local_model_cache_path,
            )

        print(f"Loading model from: {local_model_cache_path.resolve()}")
        self.model = self._load_model_from_file(local_model_cache_path)

        return self.model

    def _load_model_from_file(self, path: Path):
        """
        Loads a TensorFlow model from the given file path.
        """
        return tf.keras.models.load_model(path, compile=False)
