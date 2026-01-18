from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class S3Config:
    bucket: str
    model_prefix: str


@dataclass
class AWSConfig:
    region: str
    s3: S3Config


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_datafile: Path
    unzip_dir: Path
    data_folder: Path
    moved_location: Path


@dataclass(frozen=True)
class DataPreprocessingConfig:
    root_dir: Path
    unzip_dir: Path
    reshape_dir: Path
    image_size: tuple


@dataclass(frozen=True)
class PrepareBaseModelConfig:
    root_dir: Path
    base_model_path: Path
    updated_base_model_path: Path
    updated_base_model_image_path: Path
    params_image_size: list
    params_learning_rate: float
    params_include_top: bool
    params_weights: str
    params_classes: int


@dataclass(frozen=True)
class TrainingConfig:
    root_dir: Path
    trained_model_path: Path
    updated_base_model_path: Path
    training_data: Path
    move_trained_model_path: Path
    class_indices: Path
    params_epochs: int
    params_batch_size: int
    params_is_augmentation: bool
    params_image_size: list
    params_learning_rate: float
    data_split_seed: int
    aws: AWSConfig


@dataclass(frozen=True)
class ModelHandlerConfig:
    aws: AWSConfig
    cache_dir: Path


@dataclass(frozen=True)
class EvaluationConfig:
    root_dir: Path
    trained_model_path: Path
    training_data: Path
    all_params: dict
    params_is_augmentation: bool
    params_image_size: list
    params_batch_size: int
    data_split_seed: int
    reportfile: Path

@dataclass(frozen=True)
class PredictionConfig:
    root_dir: Path
    trained_model_path: Path
    prediction_output_file: Path