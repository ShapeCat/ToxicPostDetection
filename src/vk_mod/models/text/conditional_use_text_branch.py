import tensorflow as tf
from .text_branch_use import TextBranchUSE


@tf.keras.utils.register_keras_serializable()
class ConditionalUSEBranch(TextBranchUSE): 
    def call(self, inputs, training=None, mask=None):
        have_text = tf.strings.length(inputs) > 0
        return tf.cond(
            tf.reduce_any(have_text),
            lambda: super().call(inputs, training, mask),
            lambda: tf.zeros([tf.shape(inputs)[0], 128])
        )