import tensorflow as tf

from entity.config_entity import ModelHandlerConfig
from utils.s3_utils import S3Client


class ModelHandler:
    """
    Singleton service to load ML models from S3.

    Usage:
        loader = ModelLoader(config.model_loader)
        model = loader.get_model()
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config: ModelHandlerConfig):
        if self._initialized:
            return

        self.config = config
        self.model = None

        self.s3_client = S3Client(region_name=config.aws.region)

        # Ensure cache folder exists
        self.config.cache_dir.mkdir(parents=True, exist_ok=True)
        # Load Model Immediately
        self.load_model()

        self._initialized = True

    def load_model(self) -> tf.keras.Model:
        """
        Loads model from local cache or S3 if not cached yet.
        Returns TensorFlow model.
        """
        if self.model is not None:
            return self.model

        local_model_cache_path = self.config.cache_dir / "model.h5"
        latest_key = f"{self.config.aws.s3.model_prefix}/latest/model.h5"

        if not local_model_cache_path.exists():
            print(f"Downloading latest model from S3: {latest_key}")
            self.s3_client.download_model(
                bucket=self.config.aws.s3.bucket,
                key=latest_key,
                cache_path=local_model_cache_path,
            )

        print(f"Loading model from: {local_model_cache_path.resolve()}")
        self.model = tf.keras.models.load_model(local_model_cache_path, compile=False)

        return self.model
