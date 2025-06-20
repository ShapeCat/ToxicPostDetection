import keras
import numpy as np
import tensorflow as tf
from typing import Any
from keras import layers, optimizers, models, callbacks
from .text import TunableUSEBranch
from .image import TunableImageBranch
from .layers import DataPresense
from ..const import SEED

np.random.seed(SEED)
tf.random.set_seed(SEED)


def build_model(config:dict[str, Any]) -> models.Functional:
    text_input = keras.Input(
        shape=(),
        dtype=tf.string,
        name="text_input"
        )
    image_input = keras.Input(
        shape=(224, 224, 3),
        dtype=tf.float32,
        name="image_input"
        )
    text_presense = DataPresense()(text_input)   
    image_presense = DataPresense()(image_input)   

    text_branch = TunableUSEBranch(
        dropout_rate=config.get("text_branch_dropout_rate", 0.3),
        dropout_postition=config.get('text_branch_dropout_position', "post"),
        dense_units=config.get('text_branch_dense_units', 128),
        additional_dense_units=config.get('text_branch_additional_dense_units', 0)
        )(text_input)  
    image_branch = TunableImageBranch(
        dropout_rate=config.get("image_branch_dropout_rate", 0.3),
        dropout_postition=config.get('image_branch_dropout_position', "post"),
        dense_units=config.get('image_branch_dense_units', 128),
        additional_dense_units=config.get('image_branch_additional_dense_units', 0)
        )(image_input)
    
    x = layers.Concatenate()([
        text_branch,
        image_branch,
        text_presense,
        image_presense
    ])
   
    dense_layers = config.get("main_classifier_dense_layers", 1)
    for i in range(dense_layers):
        units = config.get(f"main_classifier_dense{i}_units", 128)
        kernel_reg = config.get("main_classifier_l2_reg", None)
        if config.get("main_classifier_l2_reg", None):
            kernel_reg = tf.keras.regularizers.l2(config["main_classifier_l2_reg"])
        x = layers.Dense(
            units=units,
            activation='relu',
            kernel_regularizer=kernel_reg
            )(x)
        
        if config.get("main_classifier_use_batchnorm", False):
            x = layers.BatchNormalization()(x)

        dropout = config.get(f'main_classifier_dropout{i}', 0.5)
        x = layers.Dropout(dropout)(x)
    
    classifier = layers.Dense(
        units=1,
        activation='sigmoid',
        dtype=tf.float32
    )(x)

    model = tf.keras.Model(inputs=[text_input, image_input], outputs=classifier)  
    learning_rate = config.get('learning_rate', 1e-4 )
    model.compile(
        optimizer=optimizers.Adam(learning_rate=learning_rate),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    return model


def compare_configurations(
        train_ds: tf.data.Dataset,
        val_ds: tf.data.Dataset,
        test_ds: tf.data.Dataset,
        configurations: list[dict[str, dict[str, Any]]],
        ):
    results = []
    histories = []

    for config in configurations:
        model_name = config.get("test_name")
        model_settings = config.get("configuration") or {}
        print(f'''
            Обучение: {model_name}
            Настройки: {model_settings}
            '''
        )
        
        model = build_model(model_settings)
        history = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=20,
            callbacks=[
                callbacks.EarlyStopping(patience=5, restore_best_weights=True),
                callbacks.ReduceLROnPlateau(factor=0.5, patience=3),
            ],
            use_multiprocessing=True,
            workers=4
        )
        
        test_loss, test_acc = model.evaluate(test_ds, verbose="silent") 
        if history is not None:
            results.append({
                "Модель": config['test_name'],
                "Accuracy": test_acc,
                "Loss": test_loss,
                "Epochs": len(history.history['loss']),
            })
            
            histories.append({
                "name": config['test_name'],
                "history": history.history
            })
    
    return results, histories
