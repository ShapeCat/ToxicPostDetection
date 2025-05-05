import numpy as np
from detoxify import Detoxify
from typing import Dict, List, Union
from numpy import ndarray
from .abstract import ToxicClassificationModelAbstract


class DetoxifyModel(ToxicClassificationModelAbstract):
    MODEL_TYPE:str = "multilingual"
    labels:list = ['toxicity','severe_toxicity', 'obscene', 'identity_attack', 'insult', 'threat', 'sexual_explicit']

    def __init__(self) -> None:
        self.model = Detoxify(self.MODEL_TYPE)

    def predict(self, text:str, aggregate:bool=False) -> Union[float, Dict[str, float]]:
        pred:Dict[str, float] = self.model.predict(text)
        if aggregate:
            values = np.array([val for val in pred.values()], dtype=np.float32)
            return self.agregate_proba(values)
        return pred

    def agregate_proba(self, proba:List[float]) -> float:
        return max(proba)
