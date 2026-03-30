"""
Example usage of logging utilities.
"""

import time
from utils.logging_utils import (
    configure_logging,
    get_logger,
    log_context,
    performance_monitor,
    operation_metrics,
    track_error,
)


# Configure logging at the start of your application
configure_logging()

logger = get_logger(__name__)


@performance_monitor("data_processing")
@operation_metrics("process_data")
def process_data(data):
    """Example function with performance monitoring."""
    logger.info(f"Processing {len(data)} items")
    time.sleep(0.5)  # Simulate processing
    return [x * 2 for x in data]


def main():
    """Main example function."""
    logger.info("Starting application")
    
    # Using log context
    with log_context(operation="main_workflow", user="admin", env="production"):
        logger.info("Inside context manager")
        
        # Process some data
        data = [1, 2, 3, 4, 5]
        result = process_data(data)
        logger.info(f"Result: {result}")
        
        # Error tracking example
        try:
            raise ValueError("Example error")
        except Exception as e:
            track_error(e, {"operation": "example", "data_size": len(data)})
    
    logger.info("Application completed")


if __name__ == "__main__":
    main()
