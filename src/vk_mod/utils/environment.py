from typing import Any, Literal
from configparser import ConfigParser, NoOptionError, NoSectionError
from pathlib import Path


def load_config(section:str, key:str, file_path:str|Path = "config.ini", default_value:Any = None, return_type:Literal["str", "int", "float", "bool"] = "str") -> Any:
    """
    Load a configuration value from a file.

    Args:
        section (str): The section of the configuration file to read from.
        key (str): The key of the configuration value to read.
        file_path (str|Path, optional): The path to the configuration file. Defaults to "config.ini".
        default_value (Any, optional): The default value to return if the key is not found or the file is not found. Defaults to None.
        return_type (Literal["str", "int", "float", "bool"], optional): The type to convert the read value to. Defaults to "str".

    Raises:
        FileNotFoundError: If the file is not found and no default value is specified.
        ValueError: If the key is not found, the value cannot be converted to the specified type, or the file cannot be read.
        NoOptionError: If the key is not found in the specified section.
        NoSectionError: If the section is not found in the file.

    Returns:
        Any: The read value converted to the specified type or the default value if the key is not found or the file is not found.
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    if not file_path.exists():
        if default_value is None:
            raise FileNotFoundError(f"Config file not found: {file_path}")
        return default_value
    
    try:
        parser = ConfigParser()
        parser.read(file_path)
        value = parser.get(section, key)
        if value is None:
            if default_value is None:
                raise ValueError(f"Key {key} not found in {file_path}")
            return default_value
        
        if return_type is "bool":
            return bool(value)      
        if return_type is "int":
            return int(value)     
        if return_type is "float":
            return float(value)
        return str(value)
    
    except (NoOptionError, NoSectionError):
        if default_value is None:
            raise
        return default_value
    except ValueError as e: 
        if default_value is None:
            raise
        return default_value
