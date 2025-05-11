import pandas as pd
from pathlib import Path
from ..const import SEED


def load_dataset(path:Path|str, sample_limit:int = -1) -> pd.DataFrame:
    """
    Loads dataset from csv file

    Args:
        path (Path or str): path to csv file
        sample_limit (int, optional): limit of samples to load. Defaults to unlimited.

    Raises:
        FileNotFoundError: if path is not a file
        ValueError: if file is not a csv file or if it does not contain 'toxic' 'image_path' and 'text' columns

    Returns:
        pd.DataFrame: dataset
    """
    if isinstance(path, str):
        path = Path(str)
        
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"File not found or {str(path)} is not file.")
    if path.suffix != ".csv":
        raise ValueError("Only .csv file supported")
    
    df = pd.read_csv(path)
    if ('toxic' not in df.columns
        and 'text' not in df.columns
        and 'image_path' not in df.columns):
        raise ValueError("CSV must contain 'toxic' 'image_path' and 'text' columns")   
    df['toxic'] = df['toxic'].astype(int) 

    sample_limit = min(sample_limit, len(df))
    return df.sample(sample_limit, random_state=SEED) if sample_limit > 0 else df


def _parse_txt_data(path:Path) -> pd.DataFrame:
    data_list:list[tuple[str, int, int, int, int]] = []
    with path.open(encoding="utf-8") as file:
        for line in file:
            labels:str = line.split(maxsplit=1)[0]
            text:str = line[len(labels)+1:].strip()
            label_list:list[str] = labels.split(",")
            labels_masks:list[int] = [1 if "__label__NORMAL" in label_list else 0.,
                    1. if "__label__INSULT" in label_list else 0.,
                    1. if "__label__THREAT" in label_list else 0.,
                    1. if "__label__OBSCENITY" in label_list else 0.]
            data_list.append((text, *labels_masks))
    return pd.DataFrame(data_list, columns=["text", "normal", "insult", "threat", "obscenity"])
