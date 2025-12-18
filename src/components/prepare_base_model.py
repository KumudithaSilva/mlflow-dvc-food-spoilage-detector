from pathlib import Path

import tensorflow as tf
import visualkeras

from entity.config_entity import PrepareBaseModelConfig


class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config

    """
    Loads the base pre-trained model (e.g., VGG16) with specified input shape, weights, and whether to include the top layer.
    Then saves the base model to disk.
    """

    def get_base_model(self):
        self.model = tf.keras.applications.vgg16.VGG16(
            input_shape=self.config.params_image_size,
            weights=self.config.params_weights,
            include_top=self.config.params_include_top,  # Here removes the final FC layers sicnce we need our own classifier layers
        )
        self.save_model(path=self.config.base_model_path, model=self.model)

    def update_base_model(self):
        self.full_model = self._prepare_full_modle(
            model=self.model,
            classes=self.config.params_classes,
            freeze_all=True,
            freeze_till=None,
            learning_rate=self.config.params_learning_rate,
        )
        self.save_model(path=self.config.updated_base_model_path, model=self.full_model)
        self.save_diagram(
            path=self.config.updated_base_model_image_path, model=self.full_model
        )

    @staticmethod
    def _prepare_full_modle(model, classes, freeze_all, freeze_till, learning_rate):
        """
        Freezing a layer means setting layer.trainable = False, so its weights will not be updated during training.
        This is commonly done to preserve the learned features from a pre-trained model when we want to use it as a feature extractor.
        """
        if freeze_all:
            for layer in model.layers:
                layer.trainable = False
        # To selectively freeze some layers of the model while leaving others trainable.
        elif (freeze_till is not None) and (freeze_till > 0):
            for layer in model.layers[:-freeze_till]:
                layer.trainable = False
        """
        The output of the base model (e.g., VGG16) is usually a 3D tensor: (height, width, channels)
        Flatten() converts this 3D output into a 1D tensor so that it can be fed into a fully connected (Dense) layer.
        """
        flatten_in = tf.keras.layers.Flatten()(model.output)
        """
        To add a custom classification head on top of the base model.
        creates a fully connected layer with classes output neurons — one for each target class.
        activation="softmax" is used for multi-class classification — it outputs a probability distribution over all classes.
        """
        prediction = tf.keras.layers.Dense(units=classes, activation="softmax")(
            flatten_in
        )

        """
        To create a new Keras model by combining input of the based model and custom output
        """
        full_model = tf.keras.models.Model(inputs=model.input, outputs=prediction)

        full_model.compile(
            optimizer=tf.keras.optimizers.legacy.SGD(learning_rate=learning_rate),
            loss=tf.keras.losses.CategoricalCrossentropy(),
            metrics=[tf.keras.metrics.Accuracy()],
        )

        full_model.summary()
        return full_model

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)

    @staticmethod
    def save_diagram(path: Path, model: tf.keras.Model):
        diagram = visualkeras.layered_view(
            model=model,
            min_z=20,
            min_xy=20,
            max_z=100,
            max_xy=800,
            scale_z=0.05,
            scale_xy=1.5,
            background_fill="white",
            font_color="black",
            padding=20,
            spacing=20,
            draw_volume=True,
            draw_funnel=True,
            legend=True,
            shade_step=10,
            show_dimension=True,
        )
        diagram.save(path)
