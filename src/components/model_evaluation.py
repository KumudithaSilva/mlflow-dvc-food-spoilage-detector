import os
from pathlib import Path
import tensorflow as tf
import dagshub
import mlflow
from urllib.parse import urlparse
from entity.config_entity import EvaluationConfig
from utils.base_utils import load_env_variables, save_json

class ModelEvaluation:
    
    def __init__(self, config: EvaluationConfig):
        self.config = config
        self.model = None
        self.valid_generator = None
        self.scores = None
    
    # ===== Create Train & Validation Generators =====
    def validation_generator(self):

        # Normalize images and keep 20% aside for validation
        datagen_kwargs = dict(rescale=1.0 / 255, validation_split=0.20)

        # Image loading settings
        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],  # Image size model expects
            batch_size=self.config.params_batch_size,  # Images per training step
            class_mode="categorical",  # For multi-class classification
            interpolation="bilinear",  # Interpolation means how the images are resized
        )

         # ===== Validation generator =====
        valid_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagen_kwargs
        )

        self.valid_generator = valid_datagen.flow_from_directory(
            directory=self.config.training_data,
            subset="validation",
            shuffle=False,
            seed=self.config.data_split_seed,
            **dataflow_kwargs
        )
    
    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        return tf.keras.models.load_model(path, compile=False)
    
    # ===== Evaluate Model =====
    def evaluate_model(self):
        self.model = self.load_model(self.config.trained_model_path)
        self.model.compile(
            optimizer=tf.keras.optimizers.legacy.Adam(),
            loss="categorical_crossentropy",
            metrics=[
                "accuracy",
                tf.keras.metrics.Precision(name="precision"),
                tf.keras.metrics.Recall(name="recall"),
                tf.keras.metrics.AUC(name="auc"),
            ],
        )
        self.validation_generator()
        self.scores = self.model.evaluate(self.valid_generator)
        print(f"Evaluation Scores: {self.scores}")

    
     # ===== Save Evaluation Report =====
    def save_evaluation_report(self):
        report = {
            "loss": self.scores[0],
            "accuracy": self.scores[1],
            "precision": self.scores[2],
            "recall": self.scores[3],
            "auc": self.scores[4],
        }
        save_json(self.config.reportfile, report)
        print(f"Evaluation report saved to {self.config.reportfile}")

    # ===== Configure MLflow =====
    def configure_mlflow(self):
        dagshub.init(
            repo_owner='KumudithaSilva',
            repo_name='mlflow-dvc-food-spoilage-detector',
            mlflow=True
        )
        load_env_variables()
        remote_server_uri = os.getenv("REMOTE_SERVER_URI")
        
        if remote_server_uri is None:
            raise ValueError("REMOTE_SERVER_URI environment variable is not set")

        mlflow.set_tracking_uri(remote_server_uri)
        mlflow.set_registry_uri(remote_server_uri)
        mlflow.set_experiment("Food_Spoilage_Classification_Experiment")

        tracked_uri = urlparse(mlflow.get_tracking_uri()).scheme
        print(
            f"Current MLflow tracking URI: {mlflow.get_tracking_uri()} "
            f"with scheme: {tracked_uri}"
        )
        
    # ===== Log Metrics & Model to MLflow =====
    def log_evaluation_metrics(self):
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():
            # Flattened parameter logging
            mlflow.log_params({
                "batch_size": self.config.params_batch_size,
                "image_size": self.config.params_image_size,
                "augmentation": self.config.params_is_augmentation,
                "seed": self.config.data_split_seed,
            })

            # Evaluation metrics
            mlflow.log_metrics({
                "eval_loss": self.scores[0],
                "eval_accuracy": self.scores[1],
                "eval_precision": self.scores[2],
                "eval_recall": self.scores[3],
                "eval_auc": self.scores[4],
            })

            # Log TensorFlow model
            if tracking_url_type_store != "file":
                mlflow.tensorflow.log_model(
                    model=self.model,
                    name="model",
                    registered_model_name="VGG16Model"
                )
            else:
                mlflow.tensorflow.log_model(
                    model=self.model,
                    name="model"
                )

            print("Evaluation metrics and model logged to MLflow successfully.")