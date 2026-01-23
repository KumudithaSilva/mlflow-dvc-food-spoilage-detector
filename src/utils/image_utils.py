import base64
from io import BytesIO
from pathlib import Path

from ensure import ensure_annotations
from PIL import Image

from logger.logging_config import logger


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


def decodeImageToPNGBytes(imageData: str) -> BytesIO:
    """
    Decodes base64 image, converts to PNG, and returns BytesIO for S3 upload.
    """
    try:
        # Remove base64 prefix if exists
        if "," in imageData:
            imageData = imageData.split(",")[1]

        # Decode base64 to bytes
        raw_bytes = base64.b64decode(imageData)

        # Convert to PIL Image
        img = Image.open(BytesIO(raw_bytes))
        img.load()

        # Save PIL Image as PNG in BytesIO
        file_obj = BytesIO()
        img.save(file_obj, format="PNG")
        file_obj.seek(0)

        return file_obj

    except Exception as e:
        raise e


def saveBytesToFile(file_obj: BytesIO, path: Path) -> Path:
    """
    Writes BytesIO content to a file.

    Args:
        file_obj (BytesIO): The in-memory file object.
        path (Path): Path where the file should be saved.

    Returns:
        Path: The path of the saved file.
    """
    try:
        # Ensure parent directories exist
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write BytesIO to file
        with open(path, "wb") as f:
            f.write(file_obj.getbuffer())

        logger.info(f"Saved BytesIO to {path}")
        file_obj.seek(0)

        return path

    except Exception as e:
        logger.exception(f"Failed to save BytesIO to {path}")
        raise e
