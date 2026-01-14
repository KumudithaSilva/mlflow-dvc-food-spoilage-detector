import os
import numpy as np
from pathlib import Path
import tensorflow as tf
from entity.config_entity import PredictionConfig
from utils.base_utils import save_json

class Prediction:

    def __init__(self, config: PredictionConfig):
        self.config = config
        self.model = None
    
    @staticmethod
    def load_model(path: Path) -> tf.keras.Model:
        return tf.keras.models.load_model(path, compile=False)
    
    def _preprocess_image(self, image_path: Path):
        img = tf.keras.preprocessing.image.load_img(
            image_path, target_size=(224, 244))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = img_array / 255.0  # Normalize the image
        img_array = tf.expand_dims(img_array, 0) 
        return img_array
    
    def predict(self, image_path: list[Path]):
        if self.model is None:
            self.model = self.load_model(self.config.trained_model_path)
        
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

        save_json(self.config.prediction_output_file, {"predictions": results})
        print(f"Prediction report saved to {self.config.prediction_output_file}")