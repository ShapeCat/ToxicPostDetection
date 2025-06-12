import tensorflow_text
import tensorflow as tf
import tensorflow_hub as hub
from typing import Literal
from keras import layers
from ..branch_abstract import BranchAbstract


class TunableUSEBranch(BranchAbstract):
    def __init__(self,
                encoder_size:Literal['small', 'large'] = 'small',
                dropout_rate:float = 0.3,
                dropout_postition:Literal['pre', 'post', 'none'] = 'post',
                dense_units:int = 128,
                **kwargs):
        super().__init__(**kwargs)
        self.config = {
            'encoder_size': encoder_size,
            'dropout_rate': dropout_rate,
            'dropout_postition': dropout_postition,
            'dense_units': dense_units,          
        }

        if encoder_size == 'small':
            model_url = "https://www.kaggle.com/models/google/universal-sentence-encoder/TensorFlow2/multilingual/2"
        elif encoder_size == 'large':
            model_url = "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"
        else:
            raise ValueError(f"Unknown encoder size: {encoder_size}")                          
        self.embed = hub.KerasLayer(model_url, trainable=False, name='embeding') 
        
        self.dense = layers.Dense(dense_units, activation='relu', name=f'feature_extractor')
        self.dropout = layers.Dropout(dropout_rate, name='dropout') if dropout_postition != 'none' else None

    def call(self, inputs, training=None, mask=None):
        x = self.embed(inputs)
        if self.dropout and self.config['dropout_postition'] == 'pre':
            x = self.dropout(x)
        x = self.dense(x)
        if self.dropout and self.config['dropout_postition'] == 'post':
            x = self.dropout(x)
        return x
    

class ConfigurableConditionalUSEBranch(TunableUSEBranch): 
    def call(self, inputs, training=None, mask=None):
        have_text = tf.strings.length(inputs) > 0
        return tf.cond(
            tf.reduce_any(have_text),
            lambda: super().call(inputs, training, mask),
            lambda: tf.zeros([tf.shape(inputs)[0], self.config['dense_units']])
        )