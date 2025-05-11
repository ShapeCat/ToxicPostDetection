import pandas as pd
from pathlib import Path
from ..const import SEED


def load_dataset(path:Path, sample_limit:int=-1, quiet:bool=False) -> pd.DataFrame:
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File not found or {str(path)} is not file.")
    if path.suffix != ".csv":
        raise ValueError("Only .csv file supported")
    
    df = pd.read_csv(path).fillna("")
    if ('toxic' not in df.columns
        and 'text' not in df.columns
        and 'image_path' not in df.columns):
        raise ValueError("CSV must contain 'toxic' 'image_path' and 'text' columns")   
    df['toxic'] = df['toxic'].astype(int) 

    sample_limit = min(sample_limit, len(df))
    return df.sample(sample_limit, random_state=SEED) if sample_limit > 0 else df
