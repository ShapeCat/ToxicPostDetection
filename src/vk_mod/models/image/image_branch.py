import tensorflow as tf
from keras import layers, Model, saving, applications

@tf.keras.utils.register_keras_serializable()
class ImageBranch(Model):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.base_model = applications.EfficientNetB0(
            include_top=False,
            weights='imagenet',
            input_shape=(224, 224, 3)
        )
        self.base_model.trainable = False
        self.pooling2d:layers.GlobalAveragePooling2D = layers.GlobalAveragePooling2D(name='pooling2d')
        self.dense:layers.Dense = layers.Dense(128, activation='relu', name='feature_extractor')
        self.dropout:layers.Dropout = layers.Dropout(0.3, name='dropout')

    def call(self, inputs, training=None, mask=None):
        x:tf.Tensor = self.base_model(inputs)
        x:tf.Tensor = self.pooling2d(x)
        return self.dropout(self.dense(x))
    
    def get_config(self) -> dict:
        return super().get_config()
    
    @classmethod
    def from_config(cls, config, custom_objects=None):
        return cls(**config)
