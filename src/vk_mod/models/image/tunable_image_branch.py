import tensorflow as tf
from keras import layers, applications
from typing import Literal
from keras.applications.mobilenet_v3 import MobileNetV3Large
from keras.applications.efficientnet import EfficientNetB0
from ..branch_abstract import BranchAbstract


class TunableImageBranch(BranchAbstract):
    def __init__(self,
                 base_model:Literal['efficientnet', 'mobilenet'] = 'efficientnet',         
                 dense_units:int = 128,
                 dropout_postition:Literal['pre', 'post', 'none'] = 'post',
                 dropout_rate:float = 0.3,
                 additional_dense_units:int = 0,
                 **kwargs) -> None:
        config = {
            'base_model': base_model,
            'dense_units': dense_units,
            'dropout_postition': dropout_postition,
            'dropout_rate': dropout_rate,
            "additional_dense_units": additional_dense_units
            }
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
        self.dense_meta = layers.Dense(additional_dense_units, activation='relu') if additional_dense_units > 0 else None
        self.dense = layers.Dense(dense_units, activation='relu', name=f'feature_extractor')
        self.dropout = layers.Dropout(dropout_rate, name='dropout') if dropout_postition != 'none' else None
            
    def call(self, inputs, training=None, mask=None):
        x = self.base_model(inputs)
        x = self.pooling2d(x)
        if self.dense_meta:
            x = self.dense_meta(x)
        if self.dropout and self.config['dropout_postition'] == 'pre': 
            x = self.dropout(x)
        x = self.dense(x)
        if self.dropout and self.config['dropout_postition'] == 'post':
            x = self.dropout(x)
        return x


class ConfigurableConditionalImageBranch(TunableImageBranch):
    def call(self, inputs, training=None, mask=None):
        have_image = tf.reduce_max(tf.abs(inputs), axis=[1, 2, 3]) > 0.01
        return tf.cond(
            tf.reduce_any(have_image),
            lambda: super().call(inputs, training, mask),
            lambda: tf.zeros([tf.shape(inputs)[0], self.config['dense_units']])
            )