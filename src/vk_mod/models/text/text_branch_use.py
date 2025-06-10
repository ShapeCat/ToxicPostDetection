import tensorflow_text
import tensorflow as tf
from keras import layers, Model
import tensorflow_hub as hub

@tf.keras.utils.register_keras_serializable()
class TextBranchUSE(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.embed = hub.KerasLayer("https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3", 
                                   trainable=False) 
        self.dense = layers.Dense(128, activation='relu')
        
    def call(self, inputs, training=None, mask=None):
        return self.dense(self.embed(inputs))
    
    def get_config(self):
        return super().get_config()
    
    @classmethod
    def from_config(cls, config, custom_objects=None):
        return cls(**config)
