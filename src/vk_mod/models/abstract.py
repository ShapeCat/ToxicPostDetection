import numpy as np
from abc import abstractmethod
from typing import overload
from sklearn.metrics import log_loss, accuracy_score


class ToxicClassificationModelAbstract():
    labels:list[str] = None

    @abstractmethod
    def predict(self, texts:list[str], aggregate:bool=False) -> float|dict[str, float]:
        raise NotImplementedError()

    @abstractmethod
    def agregate_proba(self, proba:list[float]) -> float:
        raise NotImplementedError()

    @overload
    def score(self, texts:list[str], expected:list[float]) -> None:
        ...
    @overload
    def score(self, texts:list[str], expected:list[list[float]]) -> None:    
        ...
    def score(self, texts, expected):
        if len(texts) != len(expected):
            raise ValueError("expected length must be same as texts")
        if not isinstance(texts, list):
            raise ValueError(f"text data must be list, but got {type(texts)}")
        if not isinstance(expected, list):
            raise ValueError(f"expected data must be list, but got {type(texts)}")
        if isinstance(expected[0], float):
            pred = np.zeros(shape=(len(texts)), dtype=np.float32)
            for i in range(len(texts)): 
                pred[i] = self.agregate_proba([val for val in self.predict(texts[i], aggregate=False).values()])     
            logloss = log_loss(expected, pred, labels=[0., 1.])
            accuracy = accuracy_score(expected, pred.round())
            print(f"Log Loss: {logloss:.4f}")
            print(f"Accuracy: {accuracy:.4f}")
        elif isinstance(expected[0], list):
            pred = np.zeros(shape=(len(texts), len(self.labels)), dtype=np.float32)
            for i in range(len(texts)): 
                pred[i] = np.array([val for val in self.predict(texts[i], aggregate=False).values()], dtype=np.float32)
            logloss = log_loss(expected, pred)
            print(f"Log Loss: {logloss:.4f}")
