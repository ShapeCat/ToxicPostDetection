from dotenv import dotenv_values
from typing import Any, Optional

def load_env(value_name:str, default_value:Optional[Any]=None) -> Any:
    try:
        env = dotenv_values("../.env")
        return env.get(value_name, default_value)
    except Exception as e:
        print(f"There is an error while reading .env file: {e}")
        return default_value
