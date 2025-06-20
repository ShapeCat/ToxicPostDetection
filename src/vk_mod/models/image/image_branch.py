import tensorflow as tf
from keras import layers, applications
from keras.applications.mobilenet_v3 import MobileNetV3Large
from keras.applications.efficientnet import EfficientNetB0
from typing import Literal
from ..branch_abstract import BranchAbstract


class ImageBranch(BranchAbstract):
    def __init__(self, base_model:Literal['efficientnet', 'mobilenet'] = 'efficientnet', **kwargs) -> None:
        config = {'base_model': base_model}
        super().__init__(config=config, **kwargs)
               
        if base_model == 'efficientnet':
            self.base_model = EfficientNetB0(
                include_top=False,
                weights='imagenet',
                input_shape=(224, 224, 3)
            )
        elif base_model == 'mobilenet':
            self.base_model = MobileNetV3Large(
                include_top=False,
                weights='imagenet',
                input_shape=(224, 224, 3)
            )
        else:
            raise ValueError(f"Unknown base model: {base_model}")
        self.base_model.trainable = False
        self.pooling2d = layers.GlobalAveragePooling2D(name='pooling2d')
        self.dense = layers.Dense(128, activation='relu', name='feature_extractor')
        self.dropout = layers.Dropout(0.3, name='dropout')

    def call(self, inputs, training=None, mask=None):
        x = self.base_model(inputs)
        x = self.pooling2d(x)
        x = self.dense(x)
        x = self.dropout(x)
        return x


class ConditionalImageBranch(ImageBranch):
    def call(self, inputs, training=None, mask=None):
        have_image = tf.reduce_max(tf.abs(inputs), axis=[1, 2, 3]) > 0.01
        return tf.cond(
            tf.reduce_any(have_image),
            lambda: super().call(inputs, training, mask),
            lambda: tf.zeros([tf.shape(inputs)[0], 128])
            )
