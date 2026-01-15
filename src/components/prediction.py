import os
import numpy as np
from pathlib import Path
import tensorflow as tf
from entity.config_entity import PredictionConfig
from utils.base_utils import save_json

class Prediction:
    _instance = None

    # Make sure Model load once
    def __new__(cls, config: PredictionConfig):
        if cls._instance is None:
            cls._instance = super(Prediction, cls).__new__(cls)
            cls._instance.__init__(config)
        return cls._instance

    def __init__(self, config: PredictionConfig):
        """
        Constructor:
        - Store config
        - Load model ONCE 
        """
        self.config = config
        # Load model once during initialization
        self.model = tf.keras.models.load_model(self.config.trained_model_path, compile=False)
    

    def _preprocess_image(self, image_path: Path):
        """
        Image preprocessing:
        - Resize using config
        - Normalize
        - Add batch dimension
        """
        img = tf.keras.preprocessing.image.load_img(
            image_path, target_size=(224, 244))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = img_array / 255.0  # Normalize the image
        img_array = tf.expand_dims(img_array, 0) 
        return img_array
    
    def predict(self, image_path: list[Path]):
        """
        Predict for a batch of images
        """
        results = []

        for img_path in image_path:
            preprocessed_image = self._preprocess_image(img_path)
            predictions = self.model.predict(preprocessed_image, verbose=0)

            predicted_class = tf.argmax(predictions, axis=1).numpy()[0]
            confidence = float(np.max(predictions))

            results.append({
                "image": img_path.name,
                "class_index":  int(predicted_class),
                "confidence": float(confidence)
            })

        if self.config.prediction_output_file:
            save_json(
                self.config.prediction_output_file,
                {"predictions": results}
                )    
        return results