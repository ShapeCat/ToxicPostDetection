import tensorflow as tf
from keras import layers, Model, saving, applications


@saving.register_keras_serializable()
class ImageBranch(Model):
    def __init__(self, **kwargs) -> None:
        """
        Initialize the ImageBranch.

        Args:
            **kwargs: Additional keyword arguments for the base Model initialization.
        """
        super().__init__(**kwargs)
        self.base_model = applications.EfficientNetB0(
            include_top=False,
            weights='imagenet',
            input_shape=(224, 224, 3)
        )
        self.base_model.trainable = False
        self.pooling2d:layers.GlobalAveragePooling2D = layers.GlobalAveragePooling2D()
        self.dense:layers.Dense = layers.Dense(128, activation='relu')
        self.dropout:layers.Dropout = layers.Dropout(0.3)

    def call(self, inputs:tf.Tensor) -> tf.Tensor:
        """
        Forward pass of the model.

        Args:
            inputs (tf.Tensor): Input tensor with shape (batch_size, 224, 224, 3).

        Returns:
            tf.Tensor: Output tensor after passing through the model layers.
        """
        x:tf.Tensor = self.base_model(inputs)
        x:tf.Tensor = self.pooling2d(x)
        return self.dropout(self.dense(x))
    
    def get_config(self) -> dict:
        """
        Get the configuration of the model as a dictionary.

        Returns:
            dict: The configuration of the model.
        """
        return super().get_config()
    
    @classmethod
    def from_config(cls, config:dict) -> 'ImageBranch':
        """
        Initialize the `ImageModel` from a configuration dictionary.

        Args:
            config (dict): A dictionary containing the configuration for the model.

        Returns:
            ImageBranch: An instance of `ImageBranch` with the specified configuration.
        """
        return cls(**config)
