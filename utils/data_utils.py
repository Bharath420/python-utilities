"""
Data processing utilities for YAML, JSON, and common data operations.
"""

import json
import yaml
import csv
from typing import Any, Dict, List, Optional
from pathlib import Path


class dotDict(dict):
    """
    Dictionary subclass that allows dot notation access to nested dictionaries.
    
    Example:
        >>> d = dotDict({'a': {'b': 1}})
        >>> d.a.b
        1
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = dotDict(value)
    
    def __getattr__(self, key):
        try:
            value = self[key]
            if isinstance(value, dict):
                return dotDict(value)
            return value
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")
    
    def __setattr__(self, key, value):
        self[key] = value
    
    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")


def load_yaml(file_path: str) -> Dict[str, Any]:
    """
    Load YAML file and return as dictionary.
    
    Args:
        file_path: Path to YAML file
    
    Returns:
        dict: Parsed YAML content
    
    Example:
        >>> data = load_yaml("config.yaml")
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def save_yaml(data: Dict[str, Any], file_path: str, sort_keys: bool = False):
    """
    Save dictionary to YAML file.
    
    Args:
        data: Dictionary to save
        file_path: Path to output YAML file
        sort_keys: Whether to sort keys alphabetically
    
    Example:
        >>> save_yaml({"key": "value"}, "output.yaml")
    """
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=sort_keys)


def load_json(file_path: str) -> Dict[str, Any]:
    """
    Load JSON file and return as dictionary.
    
    Args:
        file_path: Path to JSON file
    
    Returns:
        dict: Parsed JSON content
    
    Example:
        >>> data = load_json("data.json")
    """
    with open(file_path, 'r') as file:
        return json.load(file)


def save_json(data: Dict[str, Any], file_path: str, indent: int = 2):
    """
    Save dictionary to JSON file.
    
    Args:
        data: Dictionary to save
        file_path: Path to output JSON file
        indent: Indentation level for pretty printing
    
    Example:
        >>> save_json({"key": "value"}, "output.json")
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=indent)


def load_csv(file_path: str, delimiter: str = ',') -> List[Dict[str, Any]]:
    """
    Load CSV file and return as list of dictionaries.
    
    Args:
        file_path: Path to CSV file
        delimiter: CSV delimiter (default: comma)
    
    Returns:
        list: List of dictionaries, one per row
    
    Example:
        >>> data = load_csv("data.csv")
    """
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        return list(reader)


def save_csv(data: List[Dict[str, Any]], file_path: str, delimiter: str = ','):
    """
    Save list of dictionaries to CSV file.
    
    Args:
        data: List of dictionaries to save
        file_path: Path to output CSV file
        delimiter: CSV delimiter (default: comma)
    
    Example:
        >>> save_csv([{"name": "John", "age": 30}], "output.csv")
    """
    if not data:
        return
    
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys(), delimiter=delimiter)
        writer.writeheader()
        writer.writerows(data)


def table_format(data: List[Dict[str, Any]], headers: Optional[List[str]] = None) -> str:
    """
    Format list of dictionaries as a text table.
    
    Args:
        data: List of dictionaries to format
        headers: Optional list of headers to display (default: all keys)
    
    Returns:
        str: Formatted table as string
    
    Example:
        >>> data = [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]
        >>> print(table_format(data))
    """
    if not data:
        return ""
    
    # Determine headers
    if headers is None:
        headers = list(data[0].keys())
    
    # Calculate column widths
    col_widths = {h: len(h) for h in headers}
    for row in data:
        for header in headers:
            value = str(row.get(header, ''))
            col_widths[header] = max(col_widths[header], len(value))
    
    # Build table
    lines = []
    
    # Header row
    header_row = " | ".join(h.ljust(col_widths[h]) for h in headers)
    lines.append(header_row)
    lines.append("-" * len(header_row))
    
    # Data rows
    for row in data:
        data_row = " | ".join(str(row.get(h, '')).ljust(col_widths[h]) for h in headers)
        lines.append(data_row)
    
    return "\n".join(lines)


def merge_dicts(dict1: Dict, dict2: Dict, deep: bool = True) -> Dict:
    """
    Merge two dictionaries, optionally deep merging nested dicts.
    
    Args:
        dict1: First dictionary
        dict2: Second dictionary (takes precedence)
        deep: Whether to deep merge nested dictionaries
    
    Returns:
        dict: Merged dictionary
    
    Example:
        >>> d1 = {"a": 1, "b": {"c": 2}}
        >>> d2 = {"b": {"d": 3}, "e": 4}
        >>> merge_dicts(d1, d2)
        {'a': 1, 'b': {'c': 2, 'd': 3}, 'e': 4}
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if deep and key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value, deep=True)
        else:
            result[key] = value
    
    return result


def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
    """
    Flatten nested dictionary with dot notation keys.
    
    Args:
        d: Dictionary to flatten
        parent_key: Parent key prefix
        sep: Separator for nested keys
    
    Returns:
        dict: Flattened dictionary
    
    Example:
        >>> flatten_dict({"a": {"b": 1, "c": 2}})
        {'a.b': 1, 'a.c': 2}
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def unflatten_dict(d: Dict, sep: str = '.') -> Dict:
    """
    Unflatten dictionary with dot notation keys.
    
    Args:
        d: Flattened dictionary
        sep: Separator used in keys
    
    Returns:
        dict: Nested dictionary
    
    Example:
        >>> unflatten_dict({'a.b': 1, 'a.c': 2})
        {'a': {'b': 1, 'c': 2}}
    """
    result = {}
    for key, value in d.items():
        parts = key.split(sep)
        current = result
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    return result


# Example usage
if __name__ == "__main__":
    # dotDict example
    d = dotDict({'a': {'b': 1, 'c': 2}})
    print(f"dotDict access: d.a.b = {d.a.b}")
    
    # Table format example
    data = [
        {"name": "John", "age": 30, "city": "New York"},
        {"name": "Jane", "age": 25, "city": "San Francisco"},
    ]
    print("\nTable format:")
    print(table_format(data))
    
    # Flatten/unflatten example
    nested = {"a": {"b": 1, "c": {"d": 2}}}
    flattened = flatten_dict(nested)
    print(f"\nFlattened: {flattened}")
    print(f"Unflattened: {unflatten_dict(flattened)}")
