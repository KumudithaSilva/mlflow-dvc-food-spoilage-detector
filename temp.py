import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime) : %(message)s:]')

project_name = "src"

# Initilize the folder structure
list_of_folders = [
    ".github/workflow/.gitkeep",
    f"{project_name}/data/__init__.py",
    f"{project_name}/models/__init__.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/config/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/config/configuration.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/constants/__init__.py",
    "config/config.yaml",
    "dvc.yaml",
    "params.yaml",
    "requirements/requirement.txt",
    "setup.py",
    "notebooks/food_spoilage_trails.ipynb",
    "template/__init__.py",
    "reports/__init__.py",
]

for filepath in list_of_folders:
    path = Path(filepath)
    filedir = path.parent
    filename = path.name

    if filedir != Path(""):
        os.makedirs(filedir, exist_ok=True)
        # logging.info(f"Creating Directory: {filedir}")

    if not path.exists():
        with open(filepath, "w") as f:
            path.touch
            # logging.info(f"Creating empty file: {filepath}")
