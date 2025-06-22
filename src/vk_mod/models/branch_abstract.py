from keras import Model
import tensorflow as tf


@tf.keras.utils.register_keras_serializable()
class BranchAbstract(Model):
    def __init__(self, config: dict={}, **kwargs):       
        super().__init__(**kwargs)
        self.config = config

    def get_config(self):
        return self.config