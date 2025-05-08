from dotenv import dotenv_values
from typing import overload


@overload
def load_env(value_name:str, default_value:bool|None=None) -> bool|None: 
    """
    Load value from .env file by name and convert it to bool.

    Args:
        value_name (str): Name of the value to load.
        default_value (bool|None, optional): Default value if there is no such value in .env file or if the value is not a bool. Defaults to None.

    Returns:
        bool|None: Loaded value or None if default_value is None.
    """
    ... # pragma: no cover
@overload
def load_env(value_name:str, default_value:int|None=None) -> int|None: 
    """
    Load value from .env file by name and convert it to int.

    Args:
        value_name (str): Name of the value to load.
        default_value (int|None, optional): Default value if there is no such value in .env file or if the value is not an int. Defaults to None.

    Returns:
        int|None: Loaded value or None if default_value is None.
    """
    ... # pragma: no cover
@overload
def load_env(value_name:str, default_value:str|None=None) -> str|None: 
    """
    Load value from .env file by name and return it as a string.

    Args:
        value_name (str): Name of the value to load.
        default_value (str|None, optional): Default value if there is no such value in .env file. Defaults to None.

    Returns:
        str|None: Loaded value or None if default_value is None.
    """
    ... # pragma: no cover
@overload
def load_env(value_name:str, default_value:float|None=None) -> float|None: 
    """
    Load value from .env file by name and convert it to float.

    Args:
        value_name (str): Name of the value to load.
        default_value (float|None, optional): Default value if there is no such value in .env file or if the value is not a float. Defaults to None.

    Returns:
        float|None: Loaded value or None if default_value is None.
    """
    ... # pragma: no cover
def load_env(value_name: str, default_value: bool|int|str|float|None = None) -> bool|int|str|float|None:
    try:
        env = dotenv_values("../.env")
        value = env.get(value_name)
        if value is None:
            return default_value
        
        if isinstance(default_value, bool):
            return value.lower() in ("true", "1", "yes", "on")
        elif isinstance(default_value, int):
            return int(value)
        elif isinstance(default_value, float):
            return float(value)
        return value 
    except Exception as e:
        print(f"There is an error while reading .env file: {e}")
        return default_value
