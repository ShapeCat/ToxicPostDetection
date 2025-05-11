from keras import layers, Model, saving
import tensorflow as tf
import numpy as np

@saving.register_keras_serializable()
class TextBranch(Model):
    def __init__(self, max_words:int = 20000, max_len:int = 200, embedding_dim:int = 128, **kwargs) -> None:
        """
        Initializes the TextBranch with the specified parameters.

        Parameters:
            max_words (int): The maximum number of words in the vocabulary.
            max_len (int): The maximum length of the input sequence.
            embedding_dim (int): The number of dimensions of the embedding space.
            **kwargs: Additional arguments passed to the base class.

        Returns:
            None
        """
        super().__init__(**kwargs)
        self.max_words: int = max_words
        self.max_len: int = max_len
        self.embedding_dim: int = embedding_dim
        
        self.vectorizer: layers.TextVectorization = layers.TextVectorization(
            max_tokens=max_words,
            output_sequence_length=max_len,
            output_mode='int'
        )
        self.embedding: layers.Embedding = layers.Embedding(max_words + 1, embedding_dim)
        self.bidirectional_gru: layers.Bidirectional = layers.Bidirectional(layers.GRU(64, return_sequences=False))
        self.dropout: layers.Dropout = layers.Dropout(0.3)
    
    def call(self, inputs:tf.Tensor|np.ndarray) -> tf.Tensor:
        """
        Processes the input text data through the model layers.

        Args:
            inputs: A tensor or array-like structure containing input text data.

        Returns:
            A tensor representing the processed output after passing through
            the text vectorization, embedding, bidirectional GRU, and dropout layers.
        """
        x:tf.Tensor = self.vectorizer(inputs)
        x:tf.Tensor = self.embedding(x)
        return self.dropout(self.bidirectional_gru(x))
    
    def get_config(self):
        config = super().get_config()
        config.update({
            "max_words": self.max_words,
            "max_len": self.max_len,
            "embedding_dim": self.embedding_dim
        })
        return config

    @classmethod
    def from_config(cls, config:dict) -> "TextBranch":
        """
        Creates an instance of TextBranch from the given configuration.

        Args:
            config (dict): A dictionary containing the configuration for the model.

        Returns:
            TextBranch: An instance of TextBranch with the specified configuration.
        """
        config = config.copy()
        return cls(
            max_words=config.pop("max_words", 20000),
            max_len=config.pop("max_len", 200), 
            embedding_dim=config.pop("embedding_dim", 128),
            **config
        )
