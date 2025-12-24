import tensorflow as tf

from entity.config_entity import TrainingConfig


class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config

    def get_based_model(self):
        self.model = tf.keras.models.load_model(self.config.updated_base_model_path)

    def train_valid_generator(self):
        # Normalize images and keep 20% aside for validation
        datagen_kwargs = dict(rescale=1.0 / 255, validation_split=0.20)

        # Image loading settings
        dataflow_kwargs = dict(
            target_size=self.config.params_image_size[:-1],  # Image size model expects
            batch_size=self.config.params_batch_size,  # Images per training step
            class_mode="categorical",  # For multi-class classification
            interpolation="bilinear",  # Interpolation means how the images are resized
        )

        # Augmentation settings for training generator
        if self.config.params_is_augmentation:
            train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                rotation_range=40,
                horizontal_flip=True,
                width_shift_range=0.2,
                height_shift_range=0.2,
                shear_range=0.2,
                zoom_range=0.2,
                **datagen_kwargs
            )
        else:
            # Create Training Generator
            train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
                **datagen_kwargs
            )

        self.train_generator = train_datagen.flow_from_directory(
            directory=self.config.training_data,
            subset="training",
            shuffle=True,
            **dataflow_kwargs
        )

        # Create Validation Generator
        valid_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagen_kwargs
        )

        self.valid_generator = valid_datagen.flow_from_directory(
            directory=self.config.training_data,
            subset="validation",
            shuffle=False,
            **dataflow_kwargs
        )

    def train(self):
        # Compile the based model
        self.model.compile(
            optimizer=tf.keras.optimizers.legacy.Adam(
                learning_rate=self.config.params_learning_rate
            ),
            loss="categorical_crossentropy",
            metrics=[
                "accuracy",
                tf.keras.metrics.Precision(name="precision"),
                tf.keras.metrics.Recall(name="recall"),
                tf.keras.metrics.AUC(name="auc"),
            ],
        )

        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor="val_loss", patience=5, restore_best_weights=True
            )
        ]

        # Train the model
        self.model.fit(
            self.train_generator,
            epochs=self.config.params_epochs,
            validation_data=self.valid_generator,
            callbacks=callbacks,
        )

    def save_model(self):
        if self.model is None:
            raise ValueError("Model not trained or loaded yet")

        path = self.config.trained_model_path.with_suffix(".keras")
        self.model.save(path)
