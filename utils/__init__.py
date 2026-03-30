"""
Python Utilities Library
A collection of reusable utilities for logging, error handling, validation, and more.
"""

__version__ = "1.0.0"

from .logging_utils import (
    get_logger,
    get_verbose_logger,
    configure_logging,
    log_context,
    performance_monitor,
    operation_metrics,
    track_error,
)

from .error_handling import (
    CustomError,
    UnsupportedActionError,
    ActionExecutionError,
    ResourceNotFoundError,
    ValidationError,
    handle_exception,
    ErrorCodeMapper,
)

from .validators import (
    is_valid_email,
    is_valid_service_account,
    is_valid_principal,
    is_safe_url,
    is_valid_release,
)

from .data_utils import (
    load_yaml,
    load_json,
    save_yaml,
    save_json,
    table_format,
    dotDict,
)

__all__ = [
    # Logging
    "get_logger",
    "get_verbose_logger",
    "configure_logging",
    "log_context",
    "performance_monitor",
    "operation_metrics",
    "track_error",
    # Error Handling
    "CustomError",
    "UnsupportedActionError",
    "ActionExecutionError",
    "ResourceNotFoundError",
    "ValidationError",
    "handle_exception",
    "ErrorCodeMapper",
    # Validators
    "is_valid_email",
    "is_valid_service_account",
    "is_valid_principal",
    "is_safe_url",
    "is_valid_release",
    # Data Utils
    "load_yaml",
    "load_json",
    "save_yaml",
    "save_json",
    "table_format",
    "dotDict",
]
