import pandas as pd
from pathlib import Path
from ..const import SEED


def load_dataset(path:Path|list[Path], sample_limit:int=-1) -> pd.DataFrame:
    """
    Loads a dataset from the given path(s) and returns a DataFrame. If multiple paths are given, they are concatenated together. If sample_limit is greater than 0, it is divided by the number of paths and used as the sample limit for each dataset.

    Args:
        path (Path|list[Path]): The path(s) to the CSV files to be loaded.
        sample_limit (int): The maximum number of samples to load from the dataset(s). If greater than 0, it is divided by the number of paths and used as the sample limit for each dataset.

    Returns:
        pd.DataFrame: The loaded dataset.
    """
    if not isinstance(path, list):
        path = [path]
    df = pd.DataFrame()
    sample_limit = int(sample_limit//len(path)) if sample_limit > 0 else sample_limit
    for p in path:
        df = pd.concat([df, _load_dataset(p, sample_limit)], ignore_index=True)
    return df.fillna("")


def _load_dataset(path:Path, sample_limit:int=-1):
    """
    Loads a dataset from a CSV file and returns a DataFrame. The dataset must contain a 'blocked' column,
    which is converted to integer type. If a sample limit is specified, the function returns a random 
    sample of the dataset up to the given limit.

    Args:
        path (Path): The path to the CSV file to be loaded.
        sample_limit (int): The maximum number of samples to load from the dataset. If greater than 0, a random
                            sample of the specified size will be returned.

    Raises:
        FileNotFoundError: If the specified file does not exist or is not a file.
        ValueError: If the file is not a CSV file or does not contain a 'blocked' column.

    Returns:
        pd.DataFrame: The loaded dataset or a random sample of it if a sample limit is specified.
    """
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File not found or {str(path)} is not file.")
    if path.suffix != ".csv":
        raise ValueError("Only .csv file supported")
    
    df = pd.read_csv(path)
    if ('blocked' not in df.columns):
        raise ValueError("CSV must contain 'blocked' column")   
    df['blocked'] = df['blocked'].astype(int) 

    sample_limit = min(sample_limit, len(df))
    return df.sample(sample_limit, random_state=SEED) if sample_limit > 0 else df
