from keras import layers, optimizers, Model, saving, callbacks
import tensorflow as tf
from .text_branch import TextBranch
from .image_branch import ImageBranch
from ..data import DatasetGenerator
from ..preprocessing import ImagePreprocessor, TextPreprocessor
import pandas as pd


@saving.register_keras_serializable()
class ToxicClassificator(Model):
    def __init__(self, text_branch:TextBranch, image_branch:ImageBranch, **kwargs) -> None:
        """
        Initialize the ToxicClassifier.

        Args:
            text_branch (TextBranch): Instance of the text text branch for text data processing.
            image_branch (ImageBranch): Instance of the image branch for visual data processing.
            **kwargs: Additional keyword arguments for the base Model initialization.

        Returns:
            None
        """
        super().__init__(**kwargs)
        self.text_branch: TextBranch = text_branch
        self.image_branch: ImageBranch = image_branch
        self.concat: layers.Concatenate = layers.Concatenate()
        self.classifier: layers.Dense = layers.Dense(1, activation='sigmoid', dtype='float32')
        
    def call(self, inputs:dict[str, tf.Tensor]) -> tf.Tensor:
        """
        Perform a forward pass of the ToxicClassifier.

        Args:
            inputs (dict[str, tf.Tensor]): A dictionary containing 'text_input' and 'image_input' tensors.

        Returns:
            tf.Tensor: The output tensor after combining text and image features.
        """
        text_features: tf.Tensor = self.text_branch(inputs['text_input'])
        image_features: tf.Tensor = self.image_branch(inputs['image_input'])
        combined: tf.Tensor = self.concat([text_features, image_features])
        return self.classifier(combined)
    
    def compile_model(self) -> None:
        """
        Compile the ToxicClassifier.

        This method configures the model with an optimizer, loss function, and metrics for evaluation.

        Returns:
            None
        """
        super().compile(
            optimizer=optimizers.AdamW(learning_rate=1e-4),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
    def get_config(self) -> dict[str, any]:
        """
        Get the configuration of the ToxicClassifier.

        This method serializes the text and image branches into the configuration dictionary.

        Returns:
            dict[str, any]: The configuration dictionary.
        """
        config = super().get_config()
        config.update({
            "text_branch": saving.serialize_keras_object(self.text_branch),  # type: ignore
            "image_branch": saving.serialize_keras_object(self.image_branch)  # type: ignore
        })
        return config

    @classmethod
    def from_config(cls, config:dict[str, any]) -> 'ToxicClassificator':
        """
        Create an instance of ToxicClassifier from the given configuration.

        Args:
            config (dict[str, any]): A dictionary containing the configuration for the model.

        Returns:
            ToxicClassifier: An instance of ToxicClassifier with the specified configuration.
        """
        config = config.copy()
        text_branch = saving.deserialize_keras_object(config.pop("text_branch"))
        image_branch = saving.deserialize_keras_object(config.pop("image_branch"))
        return cls(text_branch, image_branch, **config) 
    

def train_model(
    train_df: pd.DataFrame, 
    val_df: pd.DataFrame, 
    images_dir: str, 
    epochs: int = 10, 
    patience: int = 5, 
    save_path: str | None = None
) -> ToxicClassificator:
    """
    Train the ToxicClassifier with the provided datasets.

    Args:
        train_df (pd.DataFrame): DataFrame containing the training data.
        val_df (pd.DataFrame): DataFrame containing the validation data.
        images_dir (str): Directory containing the dataset images.
        epochs (int, optional): Number of epochs to train the model. Defaults to 10.
        patience (int, optional): Patience for early stopping. Defaults to 5.
        save_path (str | None, optional): Path to save the model after training. Defaults to None.

    Returns:
        ToxicClassifier: Trained ToxicClassifier instance.
    """
    text_branch = TextBranch()
    image_branch = ImageBranch()
    model = ToxicClassificator(text_branch, image_branch)
    
    text_preprocessor = TextPreprocessor()
    image_preprocessor = ImagePreprocessor(images_dir)
    train_texts = train_df['text'].apply(text_preprocessor.clean).values
    text_branch.vectorizer.adapt(tf.data.Dataset.from_tensor_slices(train_texts).batch(512))
       
    train_ds = DatasetGenerator(train_df, text_preprocessor, image_preprocessor).create_dataset()
    val_ds = DatasetGenerator(val_df, text_preprocessor, image_preprocessor).create_dataset()
    
    model.compile_model()
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=[
            callbacks.EarlyStopping(patience=patience, restore_best_weights=True),
            callbacks.ReduceLROnPlateau(factor=0.5, patience=1),
        ]
    )

    if save_path:
        model.save(save_path)
    return model


def predict_from_file(model: ToxicClassificator, text: str, image_path: str) -> float:
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
    image = ImagePreprocessor("..data/images").load_from_file(image_path)
    return model.predict({
        'text_input': tf.convert_to_tensor([text]),
        'image_input': tf.expand_dims(image, 0)
    })[0][0]


def predict_from_url(model: ToxicClassificator, text: str, image_path: str) -> float:
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
    image = ImagePreprocessor("").load_from_url(image_path)
    return model.predict({
        'text_input': tf.convert_to_tensor([text]),
        'image_input': tf.expand_dims(image, 0)
    })[0][0]


def evaluate_data_combinations(model:ToxicClassificator, validation_Data:pd.DataFrame, images_dir:str) -> None:
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
    has_image = validation_Data['image_path'].apply(lambda x: len(str(x).strip()) > 0)
    
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
