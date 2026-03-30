"""
Example usage of data utilities.
"""

from utils.data_utils import (
    dotDict,
    table_format,
    merge_dicts,
    flatten_dict,
    unflatten_dict,
    load_yaml,
    save_yaml,
    load_json,
    save_json,
)


def main():
    """Main example function demonstrating data utilities."""
    
    print("=" * 60)
    print("dotDict Example")
    print("=" * 60)
    
    # Create a dotDict
    config = dotDict({
        'database': {
            'host': 'localhost',
            'port': 5432,
            'credentials': {
                'username': 'admin',
                'password': 'secret'
            }
        },
        'app': {
            'name': 'MyApp',
            'version': '1.0.0'
        }
    })
    
    # Access using dot notation
    print(f"Database host: {config.database.host}")
    print(f"Database port: {config.database.port}")
    print(f"Username: {config.database.credentials.username}")
    print(f"App name: {config.app.name}")
    
    print("\n" + "=" * 60)
    print("Table Format Example")
    print("=" * 60)
    
    # Create sample data
    users = [
        {"name": "John Doe", "age": 30, "city": "New York", "role": "Engineer"},
        {"name": "Jane Smith", "age": 25, "city": "San Francisco", "role": "Designer"},
        {"name": "Bob Johnson", "age": 35, "city": "Chicago", "role": "Manager"},
    ]
    
    # Format as table
    print(table_format(users))
    
    print("\n" + "=" * 60)
    print("Dictionary Merge Example")
    print("=" * 60)
    
    dict1 = {
        'a': 1,
        'b': {'c': 2, 'd': 3},
        'e': 5
    }
    
    dict2 = {
        'b': {'d': 4, 'f': 6},
        'g': 7
    }
    
    merged = merge_dicts(dict1, dict2, deep=True)
    print(f"Dict 1: {dict1}")
    print(f"Dict 2: {dict2}")
    print(f"Merged: {merged}")
    
    print("\n" + "=" * 60)
    print("Flatten/Unflatten Example")
    print("=" * 60)
    
    nested = {
        'server': {
            'host': 'localhost',
            'port': 8080,
            'ssl': {
                'enabled': True,
                'cert': '/path/to/cert'
            }
        },
        'database': {
            'host': 'db.example.com',
            'port': 5432
        }
    }
    
    print("Original nested dict:")
    print(nested)
    
    flattened = flatten_dict(nested)
    print("\nFlattened dict:")
    print(flattened)
    
    unflattened = unflatten_dict(flattened)
    print("\nUnflattened dict:")
    print(unflattened)
    
    print("\n" + "=" * 60)
    print("File I/O Example")
    print("=" * 60)
    
    # Example data
    sample_data = {
        'application': 'MyApp',
        'version': '1.0.0',
        'settings': {
            'debug': True,
            'log_level': 'INFO'
        }
    }
    
    # Save to YAML
    yaml_file = '/tmp/example_config.yaml'
    save_yaml(sample_data, yaml_file)
    print(f"Saved to {yaml_file}")
    
    # Load from YAML
    loaded_yaml = load_yaml(yaml_file)
    print(f"Loaded from YAML: {loaded_yaml}")
    
    # Save to JSON
    json_file = '/tmp/example_config.json'
    save_json(sample_data, json_file)
    print(f"Saved to {json_file}")
    
    # Load from JSON
    loaded_json = load_json(json_file)
    print(f"Loaded from JSON: {loaded_json}")


if __name__ == "__main__":
    main()
