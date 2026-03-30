# Python Utilities Library

A collection of reusable Python utilities for logging, error handling, debugging, and common operations.

## Features

- **Logging Framework**: Structured logging with context and performance monitoring
- **Error Handling**: Custom exceptions and error code mapping
- **Debugging Tools**: Performance monitoring and operation metrics
- **Validation Utilities**: Email, URL, service account validation
- **Data Processing**: YAML, JSON, CSV handling utilities
- **Network Utilities**: CIDR calculations, IP validation

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Logging

```python
from utils.logging_utils import get_logger, log_context, performance_monitor

logger = get_logger(__name__)

@performance_monitor("my_operation")
def my_function():
    with log_context(operation="my_operation", user="admin"):
        logger.info("Processing data")
```

### Error Handling

```python
from utils.error_handling import CustomError, handle_exception, ErrorCodeMapper

try:
    # Your code
    pass
except Exception as e:
    handle_exception(e, "operation_name")
```

### Validation

```python
from utils.validators import is_valid_email, is_valid_service_account, is_safe_url

if is_valid_email("user@example.com"):
    print("Valid email")
```

## Directory Structure

```
python-utilities/
├── README.md
├── requirements.txt
├── setup.py
├── utils/
│   ├── __init__.py
│   ├── logging_utils.py      # Logging framework
│   ├── error_handling.py     # Error handling and custom exceptions
│   ├── validators.py          # Validation utilities
│   ├── data_utils.py          # Data processing utilities
│   └── network_utils.py       # Network utilities
└── examples/
    ├── logging_example.py
    ├── error_handling_example.py
    └── validation_example.py
```

## License

MIT
