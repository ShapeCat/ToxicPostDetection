import tensorflow_text
import tensorflow as tf
from keras import layers, Model
import tensorflow_hub as hub


class TextBranchUSE(Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.embed = hub.KerasLayer("https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3", 
                                   trainable=False) 
        self.dense = layers.Dense(128, activation='relu')
        
    def call(self, inputs):
        return self.dense(self.embed(inputs))