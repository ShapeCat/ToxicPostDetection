import tensorflow as tf
from .layer_abstract import LayerAbstract


class DataPresense(LayerAbstract):
    def call(self, inputs):
        if inputs.dtype == tf.string:
            data_presense = tf.strings.length(inputs) > 0
        else:
            data_presense = tf.reduce_max(tf.abs(inputs), axis=[1,2,3]) > 0.01
        data_presense = tf.cast(data_presense, tf.float32)
        return tf.expand_dims(data_presense, axis=-1)
