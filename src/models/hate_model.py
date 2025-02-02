import tensorflow as tf
import keras
from keras import layers
from src.models.abstract import ToxicClassificationModelAbstract
from src.data_processing.text_dataset import train_val_split
from pathlib import Path
from keras import callbacks
from typing import List, Optional, Dict, Union
import numpy as np
from src.data_processing.encoding import TextEncoderAbstract


tf.random.set_seed(42)


class ToxicClassificationModel(ToxicClassificationModelAbstract):
    labels:List[str] = ["normal", "insult", "threat", "obscenity"]
    temp_folder:Path = Path("../temp")
    model_path:Path = Path("../pretrained_models/text_classification/text_model.keras")
    encoder_path:Path = Path("../pretrained_models/text_classification/")

    def __init__(self, encoder:TextEncoderAbstract, input_lenght:int, max_tokens:int) -> None:
        self.encoder = encoder

        input = layers.Input(shape=(input_lenght,))
        x = layers.Embedding(input_dim=max_tokens, output_dim=128, mask_zero=True)(input)
        x = layers.Bidirectional(layers.LSTM(64,activation="tanh"))(x)
        x = layers.Dense(64, activation="relu")(x)
        x = layers.Dropout(0.5)(x)
        x = layers.Dense(len(self.labels), activation="sigmoid")(x)
        self.model = keras.Model(input, x) 
        self.model.compile(metrics=["accuracy", keras.metrics.AUC(name="auc")],
                           optimizer=keras.optimizers.Adam(learning_rate=0.001),
                           loss=keras.losses.BinaryCrossentropy())

    def summary(self) -> None:
        self.model.summary()
    
    def train(self, X, Y, batch_size:int=32, epochs:int=10, patience:int=4) -> None:
        train_dataset, val_dataset = train_val_split(X, Y, batch_size)
        train_dataset.apply_encoder(self.encoder)
        val_dataset.apply_encoder(self.encoder)
        early_stopping = callbacks.EarlyStopping(patience=patience, restore_best_weights=True, verbose=1)
        modelBackup = callbacks.BackupAndRestore(self.temp_folder)
        reduceLR = callbacks.ReduceLROnPlateau()
        self.model.fit(train_dataset,batch_size=batch_size,epochs=epochs,verbose=2,validation_data=val_dataset,callbacks=[early_stopping, modelBackup, reduceLR])

    def save(self, path:Optional[Path]=None) -> None:
        if not path:
            path = self.model_path
        self.model.save(path)

    def predict(self, texts: Union[str, List[str]], aggregate: bool = False) -> float | Dict[str, float]:
        if isinstance(texts, str):
            texts = [texts]
        encoded = self.encoder.encode(texts)
        pred = self.model.predict(encoded, verbose=0)
        proba = pred[0]
        if aggregate:
            return self.agregate_proba(proba)
        return dict(zip(self.labels, proba))
    
    def agregate_proba(self, proba:List[float]) -> float:
         array = np.array(proba)
         return 1 - array.T[0] * (1 - array.T[-1])
