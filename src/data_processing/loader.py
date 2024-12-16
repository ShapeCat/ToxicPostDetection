import pandas as pd
from src.const import SEED
from pathlib import Path
from typing import List, Tuple
from src.utils import hashing
from src.utils.exceptions import HashNotMatchException


def load_dataset(path:Path, sample_limit:int=-1, quiet:bool=False, check_hash=False) -> pd.DataFrame:
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File not found or {str(path)} is not file.")
    if not quiet: print(f"File {str(path)} found. Loading...")

    if check_hash and not hashing.verify_file_hash(path, quiet):
        raise HashNotMatchException("file hash not match")

    if path.suffix == ".txt":
        df = _parse_txt_data(path)
    elif path.suffix == ".csv":
        df = pd.read_csv(path, index_col=0) # Why there is this column
    else:
        raise NotImplementedError("This dataset type not supported.")
    
    if not quiet and sample_limit > len(df):
        print(f"dataset only have {len(df)} records, but requered {sample_limit}")
    sample_limit = min(sample_limit, len(df))
    if sample_limit > 0: return df.sample(sample_limit, random_state=SEED)
    print(f"{sample_limit} records succesfully loaded.")
    return df

def _parse_txt_data(path:Path) -> pd.DataFrame:
    data_list:List[Tuple[str, int, int, int, int]] = []
    with path.open(encoding="utf-8") as file:
        for line in file:
            labels:str = line.split(maxsplit=1)[0]
            text:str = line[len(labels)+1:].strip()
            label_list:List[str] = labels.split(",")
            labels_masks:List[int] = [1 if "__label__NORMAL" in label_list else 0.,
                    1. if "__label__INSULT" in label_list else 0.,
                    1. if "__label__THREAT" in label_list else 0.,
                    1. if "__label__OBSCENITY" in label_list else 0.]
            data_list.append((text, *labels_masks))
    return pd.DataFrame(data_list, columns=["text", "normal", "insult", "threat", "obscenity"])
