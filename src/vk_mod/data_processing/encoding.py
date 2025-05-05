import pickle
import numpy as np
from abc import abstractmethod
from pathlib import Path
from keras import layers
from keras import utils


class TextEncoderAbstract():
    @abstractmethod
    def encode(self, text:str|list[str]):
        ...
    
    @abstractmethod
    def load_from_file(self, path:str|Path) -> None:
        ...
    
    @abstractmethod
    def save_to_file(self, path:str|Path) -> None:
        ...

class TextVectorizer(TextEncoderAbstract):
    vectorizer:layers.TextVectorization

    def __init__(self, text:list[str], file:Path|None=None) -> None:
        if file:
            self.load_from_file(file)
        else: 
            self.input_length = get_input_length(text)
            self.max_tokens = count_tokens(text)
            self.vectorizer = layers.TextVectorization(max_tokens=self.max_tokens, output_sequence_length=self.input_length)
            self.vectorizer.adapt(text)

    def load_from_file(self, path:str|Path) -> None:
        path = Path(path)
        from_disk = pickle.load(open(path, "rb"))
        self.vectorizer = layers.TextVectorization.from_config(from_disk['config'])
        self.vectorizer.set_weights(from_disk['weights'])

    def save_to_file(self, path:str|Path) -> None:
        path = Path(path)
        pickle.dump({'config': self.vectorizer.get_config(),
             'weights': self.vectorizer.get_weights()}
            , open(path, "wb"))

    def encode(self, text:list[str]):
         vectorized = self.vectorizer(text)
         return utils.pad_sequences(vectorized, maxlen=self.input_length, padding="post", truncating="post")


def get_input_length(data:list[str]) -> int:
         return int(np.percentile([len(sentence.split()) for sentence in data], 95))

def count_tokens(data:list[str]) -> int:
        tokens = set()
        for sentence in data:
            for token in sentence.split():
                tokens.add(token)
        return len(tokens)
