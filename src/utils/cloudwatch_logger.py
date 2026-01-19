import os
import logging
import watchtower

class CloudWatchLogger:
    """
    CloudWatch Logs handler factory (stateless).
    """

    def __init__(self, region_name: str = "us-east-1"):
        from utils.aws_client import AWSClient
        from utils.base_utils import load_env_variables

        aws = AWSClient(region_name)
        self.logs_client = aws.session.client("logs")
        load_env_variables() 

    
    def get_handler(self, logger_name: str) -> logging.Handler | None:
        # dynamically enable and disable logs
        if os.getenv("ENABLE_CLOUDWATCH_LOGS", "false").lower() != "true":
            return None
        
        log_group = os.getenv("CLOUDWATCH_LOG_GROUP", "fsd-logs")
        log_stream = os.getenv("CLOUDWATCH_LOG_STREAM", logger_name)

        handler = watchtower.CloudWatchLogHandler(
            boto3_client=self.logs_client,
            log_group=log_group,
            stream_name=log_stream,
            create_log_group=True
        )

        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
        )
        handler.setFormatter(formatter)

        return handler
    
    