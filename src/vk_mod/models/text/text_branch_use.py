import tensorflow_text
import tensorflow as tf
import tensorflow_hub as hub
from typing import Literal
from keras import layers
from ..branch_abstract import BranchAbstract


class TextBranchUSE(BranchAbstract):
    def __init__(self, encoder_size:Literal['small', 'large'] = 'small', **kwargs):
        config = {
            'encoder_size': encoder_size,
        }
        super().__init__(config=config, **kwargs)

        if encoder_size == 'small':
            model_url = "https://www.kaggle.com/models/google/universal-sentence-encoder/TensorFlow2/multilingual/2"
        elif encoder_size == 'large':
            model_url = "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"
        else:
            raise ValueError(f"Unknown encoder size: {encoder_size}")   
        self.embed = hub.KerasLayer(model_url, trainable=False, name='embeding') 
        
        self.dense = layers.Dense(128, activation='relu', name='feature_extractor')
        self.dropout = layers.Dropout(0.3, name='dropout')
        
    def call(self, inputs, training=None, mask=None):
        x = self.embed(inputs)
        x = self.dense(x)
        x = self.dropout(x)
        return x


class ConditionalUSEBranch(TextBranchUSE): 
    def call(self, inputs, training=None, mask=None):
        have_text = tf.strings.length(inputs) > 0
        return tf.cond(
            tf.reduce_any(have_text),
            lambda: super().call(inputs, training, mask),
            lambda: tf.zeros([tf.shape(inputs)[0], 128])
        )