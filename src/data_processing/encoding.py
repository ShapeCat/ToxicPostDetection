import pickle
import numpy as np
from abc import abstractmethod
from keras.layers import TextVectorization
from typing import Union, List, Optional
from pathlib import Path
from keras.utils import pad_sequences


class TextEncoderAbstract():
    @abstractmethod
    def encode(self, text:Union[str, List[str]]):
        ...
    
    @abstractmethod
    def load_from_file(self, path:Union[str, Path]) -> None:
        ...
    
    @abstractmethod
    def save_to_file(self, path:Union[str, Path]) -> None:
        ...


class TextVectorizer(TextEncoderAbstract):
    vectorizer:TextVectorization

    def __init__(self, text:List[str], file:Optional[Path]=None) -> None:
        if file:
            self.load_from_file(file)
        else: 
            self.input_length = get_input_length(text)
            self.max_tokens = count_tokens(text)
            self.vectorizer = TextVectorization(max_tokens=self.max_tokens, output_sequence_length=self.input_length)
            self.vectorizer.adapt(text)


    def load_from_file(self, path:Union[str, Path]) -> None:
        path = Path(path)
        from_disk = pickle.load(open(path, "rb"))
        self.vectorizer = TextVectorization.from_config(from_disk['config'])
        self.vectorizer.set_weights(from_disk['weights'])

    def save_to_file(self, path:Union[str, Path]) -> None:
        path = Path(path)
        pickle.dump({'config': self.vectorizer.get_config(),
             'weights': self.vectorizer.get_weights()}
            , open(path, "wb"))

    def encode(self, text:List[str]):
         vectorized = self.vectorizer(text)
         return pad_sequences(vectorized, maxlen=self.input_length, padding="post", truncating="post")


def get_input_length(data:List[str]) -> int:
         return int(np.percentile([len(sentence.split()) for sentence in data], 95))

def count_tokens(data:List[str]) -> int:
        tokens = set()
        for sentence in data:
            for token in sentence.split():
                tokens.add(token)
        return len(tokens)
