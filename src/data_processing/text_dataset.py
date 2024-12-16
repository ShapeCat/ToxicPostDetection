import numpy as np
from keras.utils import PyDataset
from typing import List, Optional, Any, Tuple
from src.data_processing.encoding import TextEncoderAbstract
from sklearn.model_selection import train_test_split
from src.const import SEED

class TextDataset(PyDataset):
    def __init__(self, texts:List[str], labels:list, batchSize:int=32, encoder:Optional[TextEncoderAbstract]=None, samplesLimit:int = -1, **kwargs) -> None:
        super().__init__(**kwargs)
        if(samplesLimit == -1):
            samplesLimit = min(len(texts), len(labels))
        self.labels = labels[:samplesLimit]
        self.batchSize = batchSize
        self.inputs = texts
        if encoder: self.apply_encoder(encoder)

    def __len__(self) -> int:
        return int(np.floor(len(self.inputs) / float(self.batchSize)))
    
    def __getitem__(self, index:int) -> tuple:
        start:int = index * self.batchSize
        end:int = min(start + self.batchSize, len(self.inputs))
        return (np.array([text for text in self.inputs[start:end]]),
                np.array([label for label in self.labels[start:end]]))
    
    def apply_encoder(self, encoder:TextEncoderAbstract) -> None:
        if not isinstance(self.inputs[0], str): raise AttributeError("this dataset already have encoder")
        self.encoder = encoder
        self.inputs = self.encoder.encode(self.inputs)
    

def train_val_split(X:List[str], Y:Any, batchSize:int=32) -> Tuple[TextDataset, TextDataset]:
    X_train, X_test, y_train, y_test = train_test_split(X, Y, random_state=SEED, test_size=0.2)
    train_dataset = TextDataset(X_train, y_train, batchSize)
    test_dataset = TextDataset(X_test, y_test, batchSize)
    return train_dataset, test_dataset


