"""
Example usage of validation utilities.
"""

from utils.validators import (
    is_valid_email,
    is_valid_service_account,
    is_valid_principal,
    is_safe_url,
    is_valid_release,
    is_valid_ip,
    is_valid_cidr,
)


def main():
    """Main example function demonstrating validators."""
    
    print("=" * 60)
    print("Email Validation Examples")
    print("=" * 60)
    
    emails = [
        "user@example.com",
        "invalid.email",
        "test@domain.co.uk",
        "@example.com",
    ]
    
    for email in emails:
        result = is_valid_email(email)
        print(f"  {email:30} -> {result}")
    
    print("\n" + "=" * 60)
    print("Service Account Validation Examples")
    print("=" * 60)
    
    service_accounts = [
        "my-sa@project-id.iam.gserviceaccount.com",
        "invalid@example.com",
        "toolongserviceaccountnamethatexceeds30chars@project.iam.gserviceaccount.com",
    ]
    
    for sa in service_accounts:
        result = is_valid_service_account(sa)
        print(f"  {sa:60} -> {result}")
    
    print("\n" + "=" * 60)
    print("Principal Validation Examples")
    print("=" * 60)
    
    principals = [
        "user@example.com",
        "my-sa@project.iam.gserviceaccount.com",
        "invalid",
    ]
    
    for principal in principals:
        result = is_valid_principal(principal)
        print(f"  {principal:50}")
        print(f"    Valid: {result['is_valid']}, Type: {result['type']}")
        print(f"    Message: {result['message']}")
    
    print("\n" + "=" * 60)
    print("URL Validation Examples")
    print("=" * 60)
    
    urls = [
        ("https://example.com/path", None),
        ("https://example.com/path", "example.com"),
        ("http://malicious.com", "example.com"),
        ("ftp://example.com", None),
    ]
    
    for url, allowed_host in urls:
        result = is_safe_url(url, allowed_host)
        print(f"  URL: {url:40} Host: {allowed_host or 'any':15} -> {result}")
    
    print("\n" + "=" * 60)
    print("Version Validation Examples")
    print("=" * 60)
    
    versions = ["1.2.3", "2.0.0-beta", "invalid", "v1.0.0"]
    
    for version in versions:
        result = is_valid_release(version)
        print(f"  {version:20} -> {result}")
    
    print("\n" + "=" * 60)
    print("IP Address Validation Examples")
    print("=" * 60)
    
    ips = ["192.168.1.1", "10.0.0.1", "256.1.1.1", "invalid"]
    
    for ip in ips:
        result = is_valid_ip(ip)
        print(f"  {ip:20} -> {result}")
    
    print("\n" + "=" * 60)
    print("CIDR Validation Examples")
    print("=" * 60)
    
    cidrs = ["192.168.1.0/24", "10.0.0.0/8", "192.168.1.0/33", "invalid"]
    
    for cidr in cidrs:
        result = is_valid_cidr(cidr)
        print(f"  {cidr:20} -> {result}")


if __name__ == "__main__":
    main()
