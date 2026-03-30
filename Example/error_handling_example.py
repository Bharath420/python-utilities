"""
Example usage of error handling utilities.
"""

from utils.error_handling import (
    ValidationError,
    ResourceNotFoundError,
    UnsupportedActionError,
    ActionExecutionError,
    handle_exception,
    ErrorCodeMapper,
)
from utils.logging_utils import configure_logging, get_logger


configure_logging()
logger = get_logger(__name__)


def validate_user_input(user_id, email):
    """Example validation function."""
    if not user_id:
        raise ValidationError(
            "User ID is required",
            details={"field": "user_id", "value": user_id}
        )
    
    if "@" not in email:
        raise ValidationError(
            "Invalid email format",
            details={"field": "email", "value": email}
        )


def fetch_resource(resource_type, resource_id):
    """Example resource fetching function."""
    # Simulate resource not found
    raise ResourceNotFoundError(
        resource_type=resource_type,
        resource_id=resource_id,
        details={"attempted_at": "2026-03-30"}
    )


def execute_action(action_name):
    """Example action execution function."""
    supported_actions = ["create", "update", "delete"]
    
    if action_name not in supported_actions:
        raise UnsupportedActionError(
            action=action_name,
            details={"supported_actions": supported_actions}
        )
    
    # Simulate action failure
    raise ActionExecutionError(
        action=action_name,
        reason="Database connection failed",
        details={"retry_count": 3}
    )


def main():
    """Main example function demonstrating error handling."""
    
    # Example 1: Validation error
    try:
        validate_user_input("", "invalid-email")
    except Exception as e:
        error_code = handle_exception(e, "user_validation", logger)
        logger.info(f"Handled with error code: {error_code}")
    
    # Example 2: Resource not found
    try:
        fetch_resource("user", "12345")
    except Exception as e:
        error_code = handle_exception(e, "fetch_user", logger)
        logger.info(f"Handled with error code: {error_code}")
    
    # Example 3: Unsupported action
    try:
        execute_action("invalid_action")
    except Exception as e:
        error_code = handle_exception(e, "execute_action", logger)
        logger.info(f"Handled with error code: {error_code}")
    
    # Example 4: Action execution error
    try:
        execute_action("create")
    except Exception as e:
        error_code = handle_exception(e, "execute_create", logger)
        logger.info(f"Handled with error code: {error_code}")
        
        # Get error details if it's a custom error
        if hasattr(e, 'to_dict'):
            logger.info(f"Error details: {e.to_dict()}")


if __name__ == "__main__":
    main()
