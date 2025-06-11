import tensorflow_text
import tensorflow as tf
import tensorflow_hub as hub
from typing import Literal
from keras import layers, Model


@tf.keras.utils.register_keras_serializable()
class TextBranchUSE(Model):
    def __init__(self, encoder_size:Literal['small', 'large'] = 'small', **kwargs):
        super().__init__(**kwargs)
        if encoder_size == 'small':
            model_url = "https://www.kaggle.com/models/google/universal-sentence-encoder/TensorFlow2/multilingual/2"
        elif encoder_size == 'large':
            model_url = "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"
        else:
            raise ValueError(f"Unknown encoder size: {encoder_size}")
            
        self.embed = hub.KerasLayer(model_url, trainable=False, name='embeding') 
        self.dense = layers.Dense(128, activation='relu', name='feature_extractor')
        
    def call(self, inputs, training=None, mask=None):
        embeddings = self.embed(inputs)
        return self.dense(embeddings)
    
    def get_config(self):
        return super().get_config()
    
    @classmethod
    def from_config(cls, config, custom_objects=None):
        return cls(**config)

@tf.keras.utils.register_keras_serializable()
class ConditionalUSEBranch(TextBranchUSE): 
    def call(self, inputs, training=None, mask=None):
        have_text = tf.strings.length(inputs) > 0
        return tf.cond(
            tf.reduce_any(have_text),
            lambda: super().call(inputs, training, mask),
            lambda: tf.zeros([tf.shape(inputs)[0], 128])
        )