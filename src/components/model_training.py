import tensorflow as tf
from datetime import datetime
from entity.config_entity import TrainingConfig
from utils.base_utils import save_json, load_env_variables
from utils.s3_utils import S3Client


class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config        
        load_env_variables() 
        

    # ===== Load Base Model =====
    def get_based_model(self):
        self.model = tf.keras.models.load_model(self.config.updated_base_model_path)

    # ===== Create Train & Validation Generators =====
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

        # ===== Training generator =====
        self.train_generator = train_datagen.flow_from_directory(
            directory=self.config.training_data,
            subset="training",
            shuffle=True,
            seed=self.config.data_split_seed,
            **dataflow_kwargs
        )

        # ===== Save class indices =====
        class_indices = self.train_generator.class_indices
        save_json(self.config.class_indices, class_indices)
        
        print(f"Class Indices saved to {self.config.class_indices}")

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

    # ===== Compile & Train Model =====
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
        
      # ===== Save Trained Model =====
    def save_model(self):
        if self.model is None:
            raise ValueError("Model not trained or loaded yet")
        
        # ----- Save to artifacts -----
        artifacts_model_path = self.config.trained_model_path.with_suffix(".h5")
        self.model.save(artifacts_model_path)
        print(f"Model saved artifacts at {artifacts_model_path}")


        # ----- Save to local -----
        # overwrite
        local_model_path = self.config.move_trained_model_path.with_suffix(".h5")

        local_model_path.parent.mkdir(parents=True, exist_ok=True)
        self.model.save(local_model_path)
        print(f"Model saved locally at {local_model_path}")


        # ----- Save to AWS S3 production  -----
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")

        s3_client = S3Client(region_name=self.config.aws.region)

        versioned_key = (f"{self.config.aws.s3.model_prefix}/versions/{timestamp}/model.h5")
        latest_key = (f"{self.config.aws.s3.model_prefix}/latest/model.h5")
        class_indices_key = (f"{self.config.aws.s3.model_prefix}/latest/class_indices.json")

        # Upload versioned model
        s3_client.upload_model(
            local_path=local_model_path,
            bucket=self.config.aws.s3.bucket,
            key=versioned_key
        )

        # Upload and overwrite latest model
        s3_client.upload_model(
            local_path=local_model_path,
            bucket=self.config.aws.s3.bucket,
            key=latest_key
        )

        # Upload and overwrite latest model indices
        s3_client.upload_model(
            local_path=self.config.class_indices,
            bucket=self.config.aws.s3.bucket,
            key=class_indices_key
        )

        print(
        f"Model and Indices uploaded to:\n"
        f" - s3://{self.config.aws.s3.bucket}/{versioned_key}\n"
        f" - s3://{self.config.aws.s3.bucket}/{latest_key}\n"
        f" - s3://{self.config.aws.s3.bucket}/{class_indices_key}"
        )
