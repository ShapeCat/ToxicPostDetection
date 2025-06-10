import tensorflow as tf
from keras import layers, Model


@tf.keras.utils.register_keras_serializable()
class TextBranch(Model):
    def __init__(self, max_words:int = 20000, max_len:int = 200, embedding_dim:int = 128, **kwargs) -> None:
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
    
    def call(self, inputs, training=None, mask=None):
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
    def from_config(cls, config, custom_objects=None):
        config = config.copy()
        return cls(
            max_words=config.pop("max_words", 20000),
            max_len=config.pop("max_len", 200), 
            embedding_dim=config.pop("embedding_dim", 128),
            **config
        )
