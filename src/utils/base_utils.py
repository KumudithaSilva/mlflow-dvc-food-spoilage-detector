import os
from box.exceptions import BoxValueError
from utils import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64
import yaml


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
        raise FileNotFoundError(f"YAML file not found at: {path_to_yaml}")
    try:
        with open(path_to_yaml, 'r') as yaml_file:
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
    pass

@ensure_annotations
def save_json(path_to_save: Path, data: dict):
    pass

@ensure_annotations
def load_json(path_json: Path) -> ConfigBox:
    pass

@ensure_annotations
def save_binary(path_to_save: Path, data: Any):
    pass

@ensure_annotations
def load_binary(path_to_binary: Path) -> Any:
    pass

@ensure_annotations
def get_file_size(path_to_file: Path) -> str:
    pass

@ensure_annotations
def encode_image_B64(path_to_image: Path) -> base64:
    pass

@ensure_annotations
def dencode_image(image_string: str, filename: str):
    pass