from pathlib import Path

from ensure import ensure_annotations
from PIL import Image

from utils import logger


@ensure_annotations
def reshape_image(image_path: Path, image_size: tuple) -> Image.Image:
    """
    Resizes an image to a fixed size and ensures 3 RGB channels.

    Args:
        image_path (Path): Path to the input image
        image_size (tuple): Desired image size (width, height)

    Returns:
        PIL.Image.Image: Resized RGB image
    """
    try:
        img = Image.open(image_path).convert("RGB")
        img = img.resize((image_size), Image.BILINEAR)
        return img
    except Exception:
        logger.exception(f"Failed to resize image: {image_path}")
        raise


# @ensure_annotations
def save_image(image: Image.Image, save_path: Path) -> None:
    """
    Saves a PIL Image to the specified path.

    Args:
        image (PIL.Image.Image): Image to be saved
        save_path (Path): Path where the image will be saved

    Raises:
        Exception: If saving the image fails
    """
    try:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(save_path)
    except Exception:
        logger.exception(f"Failed to Save image to: {save_path}")
        raise
