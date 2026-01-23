from pathlib import Path

import numpy as np
import tensorflow as tf

from components.model_handler import ModelHandler
from entity.config_entity import PredictionConfig
from utils.base_utils import save_json


class Prediction:
    def __init__(self, config: PredictionConfig, model_handler: ModelHandler):
        self.config = config
        self.model_handler = model_handler
        self.model = None

    def _get_model(self):
        if self.model is None:
            self.model = self.model_handler.load_model()
        return self.model

    def _preprocess_image(self, image_path: Path):
        """
        Image preprocessing:
        - Resize using config
        - Normalize
        - Add batch dimension
        """
        img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 244))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = img_array / 255.0  # Normalize the image
        img_array = tf.expand_dims(img_array, 0)
        return img_array

    def predict(self, image_path: list[Path]):
        """
        Predict for a batch of images
        """
        results = []
        self.model = self._get_model()

        for img_path in image_path:
            preprocessed_image = self._preprocess_image(img_path)
            predictions = self.model.predict(preprocessed_image, verbose=0)

            predicted_class = tf.argmax(predictions, axis=1).numpy()[0]
            confidence = float(np.max(predictions))

            results.append(
                {
                    "image": img_path.name,
                    "class_index": int(predicted_class),
                    "confidence": float(confidence),
                }
            )

        if self.config.prediction_output_file:
            save_json(self.config.prediction_output_file, {"predictions": results})
        return results
