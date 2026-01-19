import boto3
from utils.base_utils import  load_env_variables

class AWSClient:
    """
    Singleton AWS session manager.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, region_name: str = "us-east-1"):
        if getattr(self, "_initialized", False):
            return
        
        load_env_variables() 
        self.session = boto3.Session(region_name=region_name)
        self._initialized = True