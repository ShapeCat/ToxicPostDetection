import tensorflow as tf
from keras.layers import Layer

@tf.keras.utils.register_keras_serializable()
class LayerAbstract(Layer):
    def __init__(self, **kwargs):
        super(LayerAbstract, self).__init__(**kwargs)

    def get_config(self) -> dict:
        return super().get_config()
    
