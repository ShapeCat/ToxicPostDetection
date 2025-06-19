import os, requests
from PIL import Image
from io import BytesIO
from pathlib import Path
from pandas import DataFrame
from datasets import load_dataset


default_path = Path("../data/raw/")
Image.MAX_IMAGE_PIXELS = None


# TODO Add check if file exists
# TODO Add check for non-existant save folder
def load_from_huggingface(dataset_name:str, split="train", target_path:str|Path=default_path) -> None:
    """
    Downloads a dataset from the huggingface datasets repository and saves it as a csv file to the target_path.
    
    Args:
        dataset_name (str): The name of the dataset on the huggingface datasets repository.
        split (str): The split of the dataset to download. Defaults to "train".
        target_path (str|Path): The path to save the dataset to. Defaults to the default_path.
    """
    save_path = Path(target_path, dataset_name.split('/')[-1]).with_suffix(".csv")
    if isinstance(target_path, str):
        target_path = Path(target_path)
    dataset = load_dataset(dataset_name, split=split)
    DataFrame(dataset).to_csv(save_path)


def download_image(uri: str,
                   target_path: os.PathLike,
                   mode: str = "RGB"
                   ) -> None:
    response = requests.get(uri , timeout=3)
    image = Image.open(BytesIO(response.content))
    if image.mode != mode:
        image = image.convert(mode)
    image.save(target_path)  