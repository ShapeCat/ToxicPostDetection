from dotenv import dotenv_values
from typing import overload


@overload
def load_env(value_name:str, default_value:bool|None=None) -> bool|None: ...
@overload
def load_env(value_name:str, default_value:int|None=None) -> int|None: ...
@overload
def load_env(value_name:str, default_value:str|None=None) -> str|None: ...
@overload
def load_env(value_name:str, default_value:float|None=None) -> float|None: ...
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
