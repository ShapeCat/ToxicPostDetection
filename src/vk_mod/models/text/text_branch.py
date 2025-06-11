import tensorflow as tf
from keras import layers
from ..branch_abstract import BranchAbstract


class TextBranch(BranchAbstract):
    def __init__(self, max_words:int = 20000, max_len:int = 200, embedding_dim:int = 128, **kwargs) -> None:
        super().__init__(**kwargs)
        self.max_words = max_words
        self.max_len = max_len
        self.embedding_dim = embedding_dim
        
        self.vectorizer = layers.TextVectorization(
            max_tokens=max_words,
            output_sequence_length=max_len,
            output_mode='int',
            name='vectorizer'
        )
        self.embedding = layers.Embedding(max_words + 1, embedding_dim, name='embedding')
        self.bidirectional_gru = layers.Bidirectional(layers.GRU(64, return_sequences=False,), name='bidirectional_gru')
        self.dropout = layers.Dropout(0.3, name='dropout')
    
    def call(self, inputs, training=None, mask=None):
        x = self.vectorizer(inputs)
        x = self.embedding(x)
        x = self.bidirectional_gru(x)
        return self.dropout(x)
