import os, requests
from PIL import Image
from io import BytesIO
from pandas import DataFrame
from datasets import load_dataset


Image.MAX_IMAGE_PIXELS = None


# TODO Add check if file exists
# TODO Add check for non-existant save folder
def load_from_hugginface(dataset_name: str,
                         target_path: os.PathLike,
                         split: str="train",
                         max_rows: int = -1
                         ) -> None:
    dataset:DataFrame = load_dataset(dataset_name, split=split).to_pandas()
    if max_rows > 0:
        dataset = dataset.sample(min(max_rows, len(dataset))) 
    dataset.to_csv(target_path)


def download_image(uri: str,
                   target_path: os.PathLike,
                   mode: str = "RGB"
                   ) -> None:
    response = requests.get(uri , timeout=3)
    image = Image.open(BytesIO(response.content))
    if image.mode != mode:
        image = image.convert(mode)
    image.save(target_path)
