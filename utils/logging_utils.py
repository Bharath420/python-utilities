"""
Logging utilities with context management and performance monitoring.
"""

import logging
import time
import functools
from contextlib import contextmanager
from typing import Any, Dict, Optional
from datetime import datetime


# Global logger configuration
_loggers = {}
_verbose_loggers = {}


def configure_logging(level=logging.INFO, format_string=None):
    """
    Configure logging for the application.
    
    Args:
        level: Logging level (default: INFO)
        format_string: Custom format string for log messages
    """
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=level,
        format=format_string,
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get or create a logger with the specified name.
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    if name not in _loggers:
        logger = logging.getLogger(name)
        _loggers[name] = logger
    return _loggers[name]


def get_verbose_logger(name: str) -> logging.Logger:
    """
    Get or create a verbose logger (DEBUG level).
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        logging.Logger: Configured verbose logger instance
    """
    if name not in _verbose_loggers:
        logger = logging.getLogger(f"{name}.verbose")
        logger.setLevel(logging.DEBUG)
        _verbose_loggers[name] = logger
    return _verbose_loggers[name]


@contextmanager
def log_context(operation: str, **kwargs):
    """
    Context manager for logging operation start and end with additional context.
    
    Args:
        operation: Name of the operation
        **kwargs: Additional context to log
    
    Example:
        with log_context(operation="process_data", user="admin", resource="db"):
            # Your code here
            pass
    """
    logger = get_logger(__name__)
    context_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
    
    logger.info(f"Starting operation: {operation} [{context_str}]")
    start_time = time.time()
    
    try:
        yield
    except Exception as e:
        logger.error(f"Operation failed: {operation} - {str(e)}")
        raise
    finally:
        duration = time.time() - start_time
        logger.info(f"Completed operation: {operation} (duration: {duration:.2f}s)")


def performance_monitor(operation_name: str):
    """
    Decorator to monitor function performance and log execution time.
    
    Args:
        operation_name: Name of the operation being monitored
    
    Example:
        @performance_monitor("data_processing")
        def process_data():
            pass
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger(func.__module__)
            start_time = time.time()
            
            logger.debug(f"Starting {operation_name}: {func.__name__}")
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.info(f"Completed {operation_name}: {func.__name__} (duration: {duration:.2f}s)")
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(f"Failed {operation_name}: {func.__name__} after {duration:.2f}s - {str(e)}")
                raise
        
        return wrapper
    return decorator


def operation_metrics(operation_name: str):
    """
    Decorator to track operation metrics (calls, success, failures).
    
    Args:
        operation_name: Name of the operation
    
    Example:
        @operation_metrics("api_call")
        def call_api():
            pass
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger(func.__module__)
            
            try:
                result = func(*args, **kwargs)
                logger.debug(f"Operation metric: {operation_name} - SUCCESS")
                return result
            except Exception as e:
                logger.debug(f"Operation metric: {operation_name} - FAILURE: {str(e)}")
                raise
        
        return wrapper
    return decorator


def track_error(error: Exception, context: Optional[Dict[str, Any]] = None):
    """
    Track and log errors with additional context.
    
    Args:
        error: The exception that occurred
        context: Additional context information
    
    Example:
        try:
            # code
        except Exception as e:
            track_error(e, {"user": "admin", "resource": "db"})
    """
    logger = get_logger(__name__)
    
    error_info = {
        "type": type(error).__name__,
        "message": str(error),
        "timestamp": datetime.now().isoformat(),
    }
    
    if context:
        error_info.update(context)
    
    logger.error(f"Error tracked: {error_info}")


# Example usage
if __name__ == "__main__":
    configure_logging(level=logging.DEBUG)
    
    logger = get_logger(__name__)
    logger.info("This is an info message")
    
    @performance_monitor("example_operation")
    def example_function():
        time.sleep(1)
        return "Done"
    
    with log_context(operation="test", user="admin"):
        result = example_function()
        logger.info(f"Result: {result}")
