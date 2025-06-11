from keras import Model
import tensorflow as tf


@tf.keras.utils.register_keras_serializable()
class BranchAbstract(Model):
    def get_config(self):
        return super().get_config()
    
    @classmethod
    def from_config(cls, config, custom_objects=None):
        return cls(**config)
