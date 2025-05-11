import requests
import pandas as pd
import tensorflow as tf
from keras import applications
from pathlib import Path



class ImagePreprocessor:
    def __init__(self, image_dir:str|Path, img_size:tuple[int, int]=(224, 224)) -> None:  
        """
        Initialize an ImagePreprocessor instance.

        Args:
            image_dir (str|Path): The directory containing the images.
            img_size (tuple[int, int]): The size of the output images. Defaults to (224, 224).
        """
        self.image_dir = image_dir
        self.img_size = img_size

    def load_from_file(self, image_path:str|Path) -> tf.Tensor:
        """
        Load an image from a file and preprocess it.

        Args:
            image_path (str|Path): The path to the image file.

        Returns:
            tf.Tensor: The preprocessed image. If the image path is invalid or the file cannot be read,
                    returns a tensor of zeros with the specified image size.
        """
        if pd.isna(image_path) or image_path == '':
            return tf.zeros((*self.img_size, 3), dtype=tf.float32)
        
        full_path = Path(self.image_dir, image_path)
        try:
            img = tf.io.read_file(full_path)
            return self._preprocess_image(img)
        except:
            return tf.zeros((*self.img_size, 3), dtype=tf.float32)
        
    def load_from_url(self, image_url:str) ->tf.Tensor:
        """
        Load an image from a URL and preprocess it.

        Args:
            image_url (str): The URL of the image to load.

        Returns:
            tf.Tensor: The preprocessed image. If the image URL is invalid, the request times out, or the image cannot be read,
                    returns a tensor of zeros with the specified image size.
        """
        if pd.isna(image_url) or image_url == '':
            return tf.zeros((*self.img_size, 3), dtype=tf.float32)
        try:
            response = requests.get(image_url, timeout=3)
            response.raise_for_status()
            return self._preprocess_image(response.content)         
        except:
            return tf.zeros((*self.img_size, 3), dtype=tf.float32)
        
    def _preprocess_image(self, img):
        """
        Preprocess an image by decoding, resizing, and applying EfficientNet preprocessing.

        Args:
            img: The image data in bytes format.

        Returns:
            A preprocessed tensor suitable for EfficientNet model input.
        """
        img = tf.image.decode_jpeg(img, channels=3)
        img = tf.image.resize(img, self.img_size)
        return applications.efficientnet.preprocess_input(img)
