import re, demoji, string, nltk
import pandas as pd
from IPython.display import display
from typing import Set, List
from num2words import num2words
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tqdm.auto import tqdm
nltk.download(['stopwords', 'wordnet', 'punkt_tab'], quiet=True)
tqdm.pandas()


class TextPreprocessing():
    lemmatizer:WordNetLemmatizer = WordNetLemmatizer()
    stop_words:Set[str] = set(stopwords.words('russian'))
    mention_paceholder:str = "УПОМЯНАНИЕ"
    link_placeholder:str = "ССЫЛКА"

    @staticmethod
    def remove_emoji(text:str) -> str:
        return demoji.replace(text)

    @staticmethod
    def remove_links(text:str) -> str:
        pattern:str = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&amp;+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.sub(pattern, TextPreprocessing.link_placeholder, text).strip()

    @staticmethod
    def remove_mentions(text:str) -> str:
        return re.sub(r'@\w+', TextPreprocessing.mention_paceholder, text).strip()

    @staticmethod
    def clean_stopwords(text:str) -> str:
        return " ".join([word for word in text.split() if word not in TextPreprocessing.stop_words])

    @staticmethod
    def remove_punctuation(text: str) -> str:
        return "".join([i for i in text if i not in string.punctuation])

    @staticmethod
    def lowercase(text:str) -> str:
        return text.lower().strip()

    @staticmethod
    def num_to_words(text:str) -> str:
        def replace_match(match):
            number:str = match.group(0)
            try:
                if '.' in number:
                    return num2words(float(number), lang='ru')
                else:
                    return num2words(int(number), lang='ru')
            except ValueError:
                return number

        pattern:str = r'\b-?\d+(\.\d+)?\b'
        return re.sub(pattern, replace_match, text)

    @staticmethod
    def lemmatize(text:str) -> str:
        words:List[str] = nltk.word_tokenize(text, language="russian")
        words = [TextPreprocessing.lemmatizer.lemmatize(w) for w in words]
        words = [WordNetLemmatizer().lemmatize(w, pos='v') for w in words]
        return ' '.join(words)

    @staticmethod
    def clear_text(text:str) -> str:
        text = TextPreprocessing.remove_emoji(text)
        text = TextPreprocessing.remove_links(text)
        text = TextPreprocessing.remove_mentions(text)
        #text = TextPreprocessing.num_to_words(text)
        text = TextPreprocessing.clean_stopwords(text)
        text = TextPreprocessing.remove_punctuation(text)
        text = TextPreprocessing.lowercase(text)
        text = TextPreprocessing.lemmatize(text)
        return text
    

def na_clean(df:pd.DataFrame, quiet:bool=False) -> None:
    na_count:int = df.isna().any(axis=1).sum()
    if quiet: df.dropna(inplace=True)
    else:
        if not na_count: print("No empty record found")
        else:
            print(f"Found {na_count} rempty records")
            df.dropna(inplace=True)
            print(f"Deleted {na_count} records")

def duplicates_clear(df:pd.DataFrame, quiet:bool=False) -> None:
    duplicates_count:int = df["text"].duplicated().sum()
    if quiet: df.drop_duplicates(inplace=True)
    else:
        if not duplicates_count: print("No dublicated found")
        else:
            print(f"Found {duplicates_count} dublicated records")
            text_counts:pd.Series = df["text"].value_counts()
            display(text_counts[text_counts >= 2])
            df.drop_duplicates(inplace=True)
            print(f"Deleted {duplicates_count} records")

def preprocess_data(df:pd.DataFrame, quiet:bool=False) -> None:
    na_clean(df, quiet)
    #duplicates_clear(df, quiet)
    if quiet:
        df["text"] = df["text"].apply(TextPreprocessing.clear_text)
    else:
        print("Clrearing text...")
        df["text"] = df["text"].progress_apply(TextPreprocessing.clear_text)

   