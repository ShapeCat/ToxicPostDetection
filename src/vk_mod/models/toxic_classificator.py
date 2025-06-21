import tensorflow as tf
from pathlib import Path
from pandas import DataFrame
from keras import layers, optimizers, callbacks, models
from .text import *
from .image import *
from .layers import DataPresense
from ..data import DatasetGenerator
from ..preprocessing import ImagePreprocessor, TextPreprocessor


def build_model():
    text_input = tf.keras.Input(shape=(), dtype=tf.string, name='text_input')
    text_presense = DataPresense()(text_input)   
    text_branch = TextBranchUSE(encoder_size='small')(text_input)
    text_branch = layers.Multiply()([text_branch, text_presense])

    image_input = tf.keras.Input(shape=(224, 224, 3), dtype=tf.float32, name='image_input')
    image_presense = DataPresense()(image_input)
    image_branch = ImageBranch(base_model='mobilenet')(image_input)
    image_branch = layers.Multiply()([image_branch, image_presense])

    x = layers.Concatenate(name='concatination')([text_branch, image_branch, text_presense, image_presense])
    x = layers.Dense(192, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3, name='dropout1')(x)
    x = layers.Dense(64, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.5, name='dropout2')(x)
    
    classifier = layers.Dense(1, activation='sigmoid', dtype=tf.float32, name='classifier')(x)
    model = tf.keras.Model(inputs=[text_input, image_input], outputs=classifier)  
    model.compile(
        optimizer=optimizers.Adam(learning_rate=1e-3),
        loss='binary_crossentropy',
        metrics=["accuracy"]
    )
    return model


def build_and_train(
    train_df: DataFrame, 
    val_df: DataFrame, 
    images_dir: str, 
    epochs: int = 10, 
    patience: int = 5, 
    min_delta: float = 0.01,
    save_path: str | None = None
):
    model = build_model()
    text_preprocessor = TextPreprocessor()
    image_preprocessor = ImagePreprocessor(images_dir, image_model='mobilenet')
    train_ds = DatasetGenerator(train_df, text_preprocessor, image_preprocessor, batch_size=64).create_dataset()
    val_ds = DatasetGenerator(val_df, text_preprocessor, image_preprocessor, batch_size=64).create_dataset()
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=[
            callbacks.EarlyStopping(patience=patience, restore_best_weights=True, min_delta=min_delta), # type: ignore
            callbacks.ReduceLROnPlateau(factor=0.5, patience=1),
        ]
    )

    if save_path:
        model.save(save_path)
    return model    


def predict_from_file(model, text: str, image_path: str) -> float:
    """
    Predict the toxicity of a given text and image.

    Args:
        model (ToxicClassifier): The model to use for prediction.
        text (str): The text to predict.
        image_path (str): The path to the image to predict.

    Returns:
        float: The predicted toxicity.
    """
    text = TextPreprocessor().clean(text)
    image = ImagePreprocessor("..data/images", image_model='mobilenet').load_from_file(image_path)
    return model.predict({
        'text_input': tf.convert_to_tensor([text]),
        'image_input': tf.expand_dims(image, 0)
    })[0][0]


def predict_from_url(model, text: str, image_path: str) -> float:
    """
    Predict the toxicity of a given text and image.

    Args:
        model (ToxicClassifier): The model to use for prediction.
        text (str): The text to predict.
        image_path (str): The path to the image to predict.

    Returns:
        float: The predicted toxicity.
    """
    text = TextPreprocessor().clean(text)
    image = ImagePreprocessor("", image_model='mobilenet').load_from_url(image_path)
    return model.predict({
        'text_input': tf.convert_to_tensor([text]),
        'image_input': tf.expand_dims(image, 0)
    })[0][0]


def evaluate_data_combinations(model, validation_Data:DataFrame, images_dir:str) -> None:
    """
    Evaluate and prints the model on all possible data combinations
    Args:
        model (ToxicClassificator): The model to evaluate.
        validation_Data (pd.DataFrame): The validation data.
        images_dir (str): The directory containing the dataset images.

    Returns:
        None
    """
    text_preprocessor = TextPreprocessor()
    image_preprocessor = ImagePreprocessor(images_dir)
    
    has_text = validation_Data['text'].apply(lambda x: len(str(x).strip()) > 0)
    has_image = validation_Data['image_name'].apply(lambda x: len(str(x).strip()) > 0)
    
    subgroups = {
        'Только Текст': validation_Data[has_text & ~has_image],
        'Только Картинка': validation_Data[~has_text & has_image],
        'Только Текст+Картинка': validation_Data[has_text & has_image],
        'Весь набор': validation_Data
    }
    for name, subgroup in subgroups.items():
        print(f"Данные: {name}")
        if len(subgroup) == 0:
            continue
        ds = DatasetGenerator(subgroup, text_preprocessor, image_preprocessor).create_dataset()
        model.evaluate(ds, verbose=1)
