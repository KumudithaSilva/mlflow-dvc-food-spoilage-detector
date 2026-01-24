from unittest.mock import patch

import pytest
import tensorflow as tf

from components.model_handler import ModelHandler
from entity.config_entity import AWSConfig, ModelHandlerConfig, S3Config


# ---------------------------
# Fixtures for Configurations
# ---------------------------
@pytest.fixture
def model_handler_config(tmp_path):
    return ModelHandlerConfig(
        cache_dir=tmp_path,
        aws=AWSConfig(
            region="us-east-1",
            s3=S3Config(
                bucket="dummy",
                model_prefix="model",
            ),
        ),
    )


# ---------------------------
# Helper function to mock S3 download
# ---------------------------
def mock_s3_download(bucket, key, cache_path):
    """Writes a tiny TensorFlow model to disk"""
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    model = tf.keras.Sequential([tf.keras.layers.Dense(1, input_shape=(1,))])
    model.save(cache_path)


# ---------------------------
#  Test Loading Model
# ---------------------------
@patch("components.model_handler.S3Client")
def test_model_load(MockS3, model_handler_config):
    """Test that ModelHandler loads a model correctly"""
    mock_s3 = MockS3.return_value
    mock_s3.download_model.side_effect = mock_s3_download

    handler = ModelHandler(model_handler_config)
    model = handler.load_model()

    assert isinstance(model, tf.keras.Model)


# ---------------------------
#  Test Loading Model Using Cache
# ---------------------------
@patch("components.model_handler.S3Client")
def test_model_memory_cache(MockS3, model_handler_config):
    """Test that ModelHandler caches model in memory after first load"""
    mock_s3 = MockS3.return_value
    mock_s3.download_model.side_effect = mock_s3_download

    handler = ModelHandler(model_handler_config)
    model1 = handler.load_model()  # first load → downloads
    model2 = handler.load_model()  # second load → memory cache

    assert model1 is model2  # memory cache works
    assert mock_s3.download_model.call_count == 1  # S3 called only once


# ---------------------------
#  Test Loading Model Using disk Cache
# ---------------------------
@patch("components.model_handler.S3Client")
def test_model_disk_cache(MockS3, model_handler_config):
    """Test that a new ModelHandler instance loads model from disk without extra S3 download"""
    mock_s3 = MockS3.return_value
    mock_s3.download_model.side_effect = mock_s3_download

    # First handler downloads model from S3
    handler1 = ModelHandler(model_handler_config)
    model1 = handler1.load_model()

    # Second handler load model from disk cache
    handler2 = ModelHandler(model_handler_config)
    model2 = handler2.load_model()

    assert model2 is not model1  # different instance
    assert isinstance(model2, tf.keras.Model)
    assert mock_s3.download_model.call_count == 1  # S3 called only once
