import os
from pathlib import Path

import yaml
from box import ConfigBox
from ensure import ensure_annotations

from utils import logger


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns a ConfigBox (dict-like object with dot notation access).

    Args:
        path_to_yaml (Path): Path to the YAML file.

    Returns:
        ConfigBox: Parsed YAML content.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the YAML file is empty.
        Exception: For other YAML loading issues.
    """
    if not path_to_yaml.exists():
        logger.info(f"YAML file {path_to_yaml} not found")
        raise FileNotFoundError(f"YAML file not found at: {path_to_yaml}")
    try:
        with open(path_to_yaml, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)
            if content is None:
                raise ValueError(f"YAML file is empty: {path_to_yaml}")
            logger.info(f"YAML file {path_to_yaml} loaded successfully")
            return ConfigBox(content)

    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file: {e}")
        raise e


@ensure_annotations
def create_directories(path_to_dirs: list, verbose=True):
    """
    Creates directories from a list of Path objects.

    Args:
        path_to_dirs (List[Path]): A list of directory paths to create.
        verbose (bool): If True, logs directory creation status.

    Raises:
        Exception: If directory creation fails for reasons other than already existing.
    """
    for path in path_to_dirs:
        try:
            os.makedirs(path, exist_ok=True)
            if verbose:
                logger.info(f"Directory created at {path}")
        except Exception as e:
            logger.info(f"Error creating directory at {path}")
            raise e


@ensure_annotations
def save_json(path_to_save: Path, data: dict):
    """
    Saves a dictionary as a JSON file. Appends new entries to a list.

    Args:
        path_to_save (Path): Path where the JSON file will be saved.
        data (dict): Data to be saved in JSON format.

    Raises:
        Exception: If saving the JSON file fails.
    """
    import json

    try:
        if path_to_save.exists():
            with open(path_to_save, "r") as json_file:
                existing_data = json.load(json_file)
            
            if not isinstance(existing_data, list):
                existing_data = [existing_data]
        else:
            existing_data = []
        
        existing_data.append(data)
        
        with open(path_to_save, "w") as json_file:
            json.dump(existing_data, json_file, indent=4)
            logger.info(f"JSON file saved at {path_to_save}")

    except Exception as e:
        logger.error(f"Error saving JSON file at {path_to_save}: {e}")
        raise e

@ensure_annotations
def load_env_variables():
    """
    Loads environment variables from a .env file located in the current or parent directories.

    Raises:
        FileNotFoundError: If the .env file is not found.
    """
    from dotenv import load_dotenv, find_dotenv

    try:
        dotenv_path = find_dotenv()
        if not dotenv_path:
            raise FileNotFoundError(".env file not found in current or parent directories")
    except Exception as e:
        logger.error(f"Error finding .env file: {e}")
        raise
    
    load_dotenv(dotenv_path)
    logger.info(f".env file loaded from: {dotenv_path}")

# @ensure_annotations
# def load_json(path_json: Path) -> ConfigBox:
#     pass

# @ensure_annotations
# def save_binary(path_to_save: Path, data: Any):
#     pass

# @ensure_annotations
# def load_binary(path_to_binary: Path) -> Any:
#     pass

# @ensure_annotations
# def get_file_size(path_to_file: Path) -> str:
#     pass

# @ensure_annotations
# def encode_image_B64(path_to_image: Path) -> base64:
#     pass

# @ensure_annotations
# def dencode_image(image_string: str, filename: str):
#     pass

# @ensure_annotations
# def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
#     pass

# @ensure_annotations
# def flip_image(image: np.ndarray, horizontal: bool = True) -> np.ndarray:
#     pass

# @ensure_annotations
# def change_brightness(image: np.ndarray, factor: float) -> np.ndarray:
#     pass

# @ensure_annotations
# def change_contrast(image: np.ndarray, factor: float) -> np.ndarray:
#     pass

# @ensure_annotations
# def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
#     pass

# @ensure_annotations
# def change_rgb_channels(image: np.ndarray, r: float, g: float, b: float) -> np.ndarray:
#     pass
