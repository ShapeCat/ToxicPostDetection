from keras import Model
from typing import Any
import tensorflow as tf


@tf.keras.utils.register_keras_serializable()
class BranchAbstract(Model):
    def __init__(self, **kwargs):        
        config = kwargs.pop('config', {})
        super().__init__(**kwargs)
        self.config = config

    def get_config(self):
        config = super().get_config()
        config.update({"config": self.config})
        return config
    
    @classmethod
    def from_config(cls, config, custom_objects=None):
        custom_config = config.pop("config", {}) 
        return cls(**custom_config, **config)
