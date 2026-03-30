"""
Error handling utilities with custom exceptions and error code mapping.
"""

import sys
import traceback
from typing import Optional, Dict, Any
from enum import Enum


class ErrorCode(Enum):
    """Standard error codes for the application."""
    SUCCESS = 0
    GENERAL_ERROR = 1
    VALIDATION_ERROR = 2
    RESOURCE_NOT_FOUND = 3
    UNSUPPORTED_ACTION = 4
    ACTION_EXECUTION_ERROR = 5
    AUTHENTICATION_ERROR = 6
    PERMISSION_ERROR = 7
    NETWORK_ERROR = 8
    TIMEOUT_ERROR = 9
    CONFIGURATION_ERROR = 10


class CustomError(Exception):
    """Base custom exception class with error code support."""
    
    def __init__(self, message: str, error_code: ErrorCode = ErrorCode.GENERAL_ERROR, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self):
        return f"[{self.error_code.name}] {self.message}"
    
    def to_dict(self):
        """Convert exception to dictionary for logging/serialization."""
        return {
            "error_code": self.error_code.value,
            "error_name": self.error_code.name,
            "message": self.message,
            "details": self.details,
        }


class ValidationError(CustomError):
    """Raised when validation fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, ErrorCode.VALIDATION_ERROR, details)


class ResourceNotFoundError(CustomError):
    """Raised when a required resource is not found."""
    
    def __init__(self, resource_type: str, resource_id: str, details: Optional[Dict[str, Any]] = None):
        message = f"{resource_type} not found: {resource_id}"
        if details is None:
            details = {}
        details.update({"resource_type": resource_type, "resource_id": resource_id})
        super().__init__(message, ErrorCode.RESOURCE_NOT_FOUND, details)


class UnsupportedActionError(CustomError):
    """Raised when an unsupported action is requested."""
    
    def __init__(self, action: str, details: Optional[Dict[str, Any]] = None):
        message = f"Unsupported action: {action}"
        if details is None:
            details = {}
        details.update({"action": action})
        super().__init__(message, ErrorCode.UNSUPPORTED_ACTION, details)


class ActionExecutionError(CustomError):
    """Raised when an action fails to execute."""
    
    def __init__(self, action: str, reason: str, details: Optional[Dict[str, Any]] = None):
        message = f"Failed to execute action '{action}': {reason}"
        if details is None:
            details = {}
        details.update({"action": action, "reason": reason})
        super().__init__(message, ErrorCode.ACTION_EXECUTION_ERROR, details)


class ErrorCodeMapper:
    """Maps exceptions to error codes for consistent error handling."""
    
    _error_map = {
        ValidationError: ErrorCode.VALIDATION_ERROR,
        ResourceNotFoundError: ErrorCode.RESOURCE_NOT_FOUND,
        UnsupportedActionError: ErrorCode.UNSUPPORTED_ACTION,
        ActionExecutionError: ErrorCode.ACTION_EXECUTION_ERROR,
        ValueError: ErrorCode.VALIDATION_ERROR,
        KeyError: ErrorCode.RESOURCE_NOT_FOUND,
        FileNotFoundError: ErrorCode.RESOURCE_NOT_FOUND,
        PermissionError: ErrorCode.PERMISSION_ERROR,
        TimeoutError: ErrorCode.TIMEOUT_ERROR,
    }
    
    @classmethod
    def get_error_code(cls, exception: Exception) -> ErrorCode:
        """
        Get error code for an exception.
        
        Args:
            exception: The exception to map
        
        Returns:
            ErrorCode: Corresponding error code
        """
        if isinstance(exception, CustomError):
            return exception.error_code
        
        for exc_type, error_code in cls._error_map.items():
            if isinstance(exception, exc_type):
                return error_code
        
        return ErrorCode.GENERAL_ERROR
    
    @classmethod
    def register_error(cls, exception_type: type, error_code: ErrorCode):
        """Register a new exception type to error code mapping."""
        cls._error_map[exception_type] = error_code


def handle_exception(exception: Exception, operation: str = "unknown", logger=None, exit_on_error: bool = False):
    """
    Handle exceptions with consistent logging and error code mapping.
    
    Args:
        exception: The exception to handle
        operation: Name of the operation that failed
        logger: Logger instance (optional)
        exit_on_error: Whether to exit the program on error
    
    Returns:
        ErrorCode: The error code for the exception
    """
    error_code = ErrorCodeMapper.get_error_code(exception)
    
    error_info = {
        "operation": operation,
        "error_code": error_code.name,
        "error_value": error_code.value,
        "exception_type": type(exception).__name__,
        "message": str(exception),
    }
    
    if isinstance(exception, CustomError):
        error_info.update(exception.details)
    
    if logger:
        logger.error(f"Exception in {operation}: {error_info}")
        logger.debug(f"Traceback: {traceback.format_exc()}")
    else:
        print(f"ERROR: {error_info}", file=sys.stderr)
        print(f"Traceback: {traceback.format_exc()}", file=sys.stderr)
    
    if exit_on_error:
        sys.exit(error_code.value)
    
    return error_code


def handle_exception_exit(exception: Exception, operation: str = "unknown", logger=None):
    """
    Handle exception and exit the program with appropriate error code.
    
    Args:
        exception: The exception to handle
        operation: Name of the operation that failed
        logger: Logger instance (optional)
    """
    handle_exception(exception, operation, logger, exit_on_error=True)


# Example usage
if __name__ == "__main__":
    try:
        raise ValidationError("Invalid input", details={"field": "email", "value": "invalid"})
    except Exception as e:
        error_code = handle_exception(e, "validation_test")
        print(f"Error code: {error_code}")
        
        if isinstance(e, CustomError):
            print(f"Error dict: {e.to_dict()}")
