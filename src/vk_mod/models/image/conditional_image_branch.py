import tensorflow as tf
from .image_branch import ImageBranch


@tf.keras.utils.register_keras_serializable()
class ConditionalImageBranch(ImageBranch):
    def call(self, inputs, training=None, mask=None):
        have_image = tf.reduce_max(tf.abs(inputs), axis=[1, 2, 3]) > 0.01
        return tf.cond(
            tf.reduce_any(have_image),
            lambda: super().call(inputs, training, mask),
            lambda: tf.zeros([tf.shape(inputs)[0], 128])
            )
