"""
Validation utilities for common data types and formats.
"""

import re
from urllib.parse import urlparse
from typing import Dict, Optional
from packaging.version import Version


def is_valid_email(email: str, allowed_domains: Optional[list] = None) -> bool:
    """
    Validate email address format and optionally check domain.
    
    Args:
        email: Email address to validate
        allowed_domains: Optional list of allowed domains
    
    Returns:
        bool: True if email is valid
    
    Example:
        >>> is_valid_email("user@example.com")
        True
        >>> is_valid_email("invalid.email")
        False
    """
    if not email or "@" not in email:
        return False
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False
    
    # Check local part is not empty
    local, domain = email.split("@", 1)
    if not local.strip():
        return False
    
    # Check allowed domains if specified
    if allowed_domains:
        if domain not in allowed_domains:
            return False
    
    return True


def is_valid_service_account(sa_account: str) -> bool:
    """
    Validate Google Cloud service account format.
    
    Args:
        sa_account: Service account email to validate
    
    Returns:
        bool: True if valid service account format
    
    Example:
        >>> is_valid_service_account("my-sa@project-id.iam.gserviceaccount.com")
        True
    """
    try:
        sa_name, domain = sa_account.split("@", 1)
    except ValueError:
        return False
    
    # Check service account name length (max 30 characters)
    if len(sa_name) > 30:
        return False
    
    # Check domain format: <project-id>.iam.gserviceaccount.com
    parts = domain.split(".")
    if len(parts) < 4:
        return False
    
    # Check for expected domain structure
    if parts[-3:] != ["iam", "gserviceaccount", "com"]:
        return False
    
    return True


def is_valid_principal(principal_name: str, allowed_domains: Optional[list] = None) -> Dict[str, any]:
    """
    Validate if a principal is either a valid email or service account.
    
    Args:
        principal_name: The principal to validate
        allowed_domains: Optional list of allowed email domains
    
    Returns:
        dict: Validation result with type and message
    
    Example:
        >>> result = is_valid_principal("user@example.com")
        >>> result['is_valid']
        True
    """
    if not principal_name or principal_name == "":
        return {
            'is_valid': False,
            'type': 'unknown',
            'message': 'Principal name cannot be empty',
        }
    
    # Check if it's a valid service account
    if is_valid_service_account(principal_name):
        return {
            'is_valid': True,
            'type': 'service_account',
            'message': f'Valid Google service account: {principal_name}',
        }
    
    # Check if it's a valid email
    if is_valid_email(principal_name, allowed_domains):
        return {
            'is_valid': True,
            'type': 'email',
            'message': f'Valid email address: {principal_name}',
        }
    
    return {
        'is_valid': False,
        'type': 'unknown',
        'message': f'Invalid principal: {principal_name}',
    }


def is_safe_url(url: str, allowed_host: Optional[str] = None) -> bool:
    """
    Validate URL and optionally check if it's from an allowed host.
    
    Args:
        url: URL to validate
        allowed_host: Optional allowed hostname
    
    Returns:
        bool: True if URL is safe
    
    Example:
        >>> is_safe_url("https://example.com/path", "example.com")
        True
    """
    try:
        parsed = urlparse(url)
        
        # Check for valid scheme
        if parsed.scheme not in ['http', 'https']:
            return False
        
        # Check for hostname
        if not parsed.hostname:
            return False
        
        # Check allowed host if specified
        if allowed_host and parsed.hostname != allowed_host:
            return False
        
        return True
    except Exception:
        return False


def is_valid_release(release: str) -> bool:
    """
    Validate if a string is a valid semantic version.
    
    Args:
        release: Version string to validate
    
    Returns:
        bool: True if valid version
    
    Example:
        >>> is_valid_release("1.2.3")
        True
        >>> is_valid_release("invalid")
        False
    """
    try:
        Version(release)
        return True
    except Exception:
        return False


def is_valid_ip(ip: str) -> bool:
    """
    Validate IPv4 address format.
    
    Args:
        ip: IP address to validate
    
    Returns:
        bool: True if valid IPv4 address
    
    Example:
        >>> is_valid_ip("192.168.1.1")
        True
    """
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    
    parts = ip.split('.')
    return all(0 <= int(part) <= 255 for part in parts)


def is_valid_cidr(cidr: str) -> bool:
    """
    Validate CIDR notation.
    
    Args:
        cidr: CIDR notation to validate (e.g., "192.168.1.0/24")
    
    Returns:
        bool: True if valid CIDR notation
    
    Example:
        >>> is_valid_cidr("192.168.1.0/24")
        True
    """
    try:
        ip, prefix = cidr.split('/')
        prefix_len = int(prefix)
        return is_valid_ip(ip) and 0 <= prefix_len <= 32
    except Exception:
        return False


# Example usage
if __name__ == "__main__":
    print("Email validation:")
    print(f"  user@example.com: {is_valid_email('user@example.com')}")
    print(f"  invalid: {is_valid_email('invalid')}")
    
    print("\nService account validation:")
    print(f"  my-sa@project.iam.gserviceaccount.com: {is_valid_service_account('my-sa@project.iam.gserviceaccount.com')}")
    
    print("\nURL validation:")
    print(f"  https://example.com: {is_safe_url('https://example.com')}")
    
    print("\nVersion validation:")
    print(f"  1.2.3: {is_valid_release('1.2.3')}")
