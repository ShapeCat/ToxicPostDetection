import torch
import numpy as np
from typing import List, Dict, Union
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from .abstract import ToxicClassificationModelAbstract


class RuBertModel(ToxicClassificationModelAbstract):
    MODEL_NAME:str = 'cointegrated/rubert-tiny-toxicity'
    labels:list = ['non-toxic', 'insult', 'obscenity', 'threat', 'dangerous']

    def __init__(self) -> None:
        self.encorer = AutoTokenizer.from_pretrained(self.MODEL_NAME)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.MODEL_NAME)

    def predict(self, text:str, aggregate:bool=False) -> Union[float,Dict[str, float]]:
        if not isinstance(text, str):
            raise TypeError("Input string must be string")
    
        with torch.no_grad():
            inputs = self.encorer(text, return_tensors='pt', truncation=True, padding=True).to(self.model.device)
            proba = torch.sigmoid(self.model(**inputs).logits).cpu().numpy()
        proba:np.ndarray = proba[0]
        if aggregate:
            return self.agregate_proba(proba)
        return dict(zip(self.labels, proba))

    def agregate_proba(self, proba:List[float]) -> float:
         array = np.array(proba)
         return 1 - array.T[0] * (1 - array.T[-1])
