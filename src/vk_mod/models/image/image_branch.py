import tensorflow as tf
from keras import layers, Model, applications

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
        self.pooling2d = layers.GlobalAveragePooling2D(name='pooling2d')
        self.dense = layers.Dense(128, activation='relu', name='feature_extractor')
        self.dropout = layers.Dropout(0.3, name='dropout')

    def call(self, inputs, training=None, mask=None):
        x = self.base_model(inputs)
        x = self.pooling2d(x)
        x = self.dense(x)
        return self.dropout(x)
    
    def get_config(self) -> dict:
        return super().get_config()
    
    @classmethod
    def from_config(cls, config, custom_objects=None):
        return cls(**config)
