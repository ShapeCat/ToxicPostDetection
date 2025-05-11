import tensorflow as tf
import pandas as pd
from ..preprocessing import TextPreprocessor, ImagePreprocessor


class DatasetGenerator:
    def __init__(self, df:pd.DataFrame, text_preprocessor:TextPreprocessor, image_prerocesor:ImagePreprocessor, batch_size:int=32) -> None:
        """
        Constructor for Dataset class

        Args:
            df (pd.DataFrame): The dataframe with the toxic or not toxic label
            text_preprocessor (TextPreprocessor): The text preprocessor
            image_prerocesor (ImagePreprocessor): The image preprocessor
            batch_size (int, optional): The batch size for the dataset. Defaults to 32.
        """
        self.df = df
        self.batch_size = batch_size
        self.text_preprocessor = text_preprocessor
        self.image_prerocesor = image_prerocesor
        
    def create_dataset(self) -> tf.data.Dataset:
        """
        Creates a TensorFlow dataset from the data in the dataframe using the specified text and image preprocessors.

        Returns:
            tf.data.Dataset: A TensorFlow dataset where each element is a tuple containing:
                - A dictionary with 'text_input' as a string tensor and 'image_input' as a 3D float32 tensor.
                - A float32 tensor representing the label.
        """
        sugnature = (
                {
                    'text_input': tf.TensorSpec(shape=(), dtype=tf.string),
                    'image_input': tf.TensorSpec(shape=(224,224,3), dtype=tf.float32)
                },
                tf.TensorSpec(shape=(), dtype=tf.float32)
            )
        return (tf.data.Dataset
                   .from_generator(self._generator, output_signature=sugnature)
                   .batch(self.batch_size)
                   .prefetch(tf.data.AUTOTUNE))
    
    def _generator(self):
        """
        A generator that produces a tuple containing a dictionary with 'text_input' as a string tensor and 'image_input' as a 3D float32 tensor, and a float32 tensor representing the label.

        Yields:
            A tuple containing a dicttiionary and a float32 tensor.
        """
        for _, row in self.df.iterrows():
            text = self.text_preprocessor.clean(row['text'])
            image = self.image_prerocesor.load_from_file(row['image_path'])
            yield (
                {
                    'text_input': text,
                    'image_input': image
                },
                row['toxic']
            )
