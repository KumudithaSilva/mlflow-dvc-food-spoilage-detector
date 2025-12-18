import os
from pathlib import Path

from entity.config_entity import DataPreprocessingConfig
from utils import logger
from utils.image_utils import reshape_image, save_image


# components
class DataPreprocessing:
    def __init__(self, config: DataPreprocessingConfig):
        self.config = config

    def reshape_extracted_data(self):
        """
        Reshape all images from unzip_dir to fixed size and save them to reshape_dir.
        Preserves class folder structure and logs progress.
        """
        source_dir = Path(self.config.unzip_dir)
        target_dir = Path(self.config.reshape_dir)
        os.makedirs(target_dir, exist_ok=True)

        total_images = 0

        # Iterate over class directories (fresh, spoiled)
        for class_dir in source_dir.iterdir():
            if not class_dir.is_dir():
                logger.info(f"Skipping non-directory item: {class_dir}")
                continue

            logger.info(f"Processing class directory: {class_dir.name}")

            # Create corresponding class folder in target_dir
            class_subdir = target_dir / class_dir.name
            class_subdir.mkdir(parents=True, exist_ok=True)

            image_count = 0

            # Recursively iterate all image files in class_dir
            for img_file in class_dir.rglob("*"):
                if img_file.is_file() and img_file.suffix.lower() in [
                    ".jpg",
                    ".jpeg",
                    ".png",
                ]:
                    try:
                        # Resize image
                        resized_image = reshape_image(
                            image_path=img_file,
                            image_size=tuple(self.config.image_size),
                        )

                        # Preserve nested subfolder structure
                        relative_path = img_file.relative_to(class_dir)
                        save_path = class_subdir / relative_path
                        save_path.parent.mkdir(parents=True, exist_ok=True)

                        save_image(resized_image, save_path)

                        image_count += 1
                        total_images += 1
                        logger.info(f"Resized and saved image to {save_path}")

                    except Exception as e:
                        logger.error(f"Error processing image {img_file}: {e}")
                        continue

            logger.info(f"Processed {image_count} images for class '{class_dir.name}'")

        logger.info(f"Total images resized and saved: {total_images}")
