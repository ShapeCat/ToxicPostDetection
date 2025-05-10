import pandas as pd
from pathlib import Path
from ..const import SEED


def load_dataset(path:Path, sample_limit:int=-1, quiet:bool=False) -> pd.DataFrame:
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File not found or {str(path)} is not file.")
    if not quiet: print(f"File {str(path)} found. Loading...")

    if path.suffix == ".txt":
        df = _parse_txt_data(path)
    elif path.suffix == ".csv":
        df = pd.read_csv(path, index_col=0) # Why there is this column
    else:
        raise NotImplementedError("This dataset type not supported.")
    
    if not quiet and sample_limit > len(df):
        print(f"dataset only have {len(df)} records, but requered {sample_limit}")
    sample_limit = min(sample_limit, len(df))
    return df.sample(sample_limit, random_state=SEED) if sample_limit > 0 else df
