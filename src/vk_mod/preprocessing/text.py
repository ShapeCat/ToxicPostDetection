import demoji, re


class TextPreprocessor:
    def __init__(self, link_placeholder:str="ССЫЛКА", mention_placeholder:str="УПОМЯНАНИЕ", encoding:str="cp1251") -> None:
        """
        Initialize a TextPreprocessor instance with optional placeholders and encoding.

        Args:
            link_placeholder (str): The placeholder string for links. Defaults to "ССЫЛКА".
            mention_placeholder (str): The placeholder string for mentions. Defaults to "УПОМЯНАНИЕ".
            encoding (str): The text encoding to use. Defaults to "cp1251".
        """
        self.mention_placeholder = mention_placeholder
        self.link_placeholder = link_placeholder
        self.encoding = encoding

    def clean(self, text:str) -> str:
        """
        Clean the input text by processing it through several cleaning steps.

        Args:
            text (str): The input text to be cleaned.

        Returns:
            str: The cleaned text if the input is a string, otherwise an empty string.
        """
        return self._clean_text(text) if isinstance(text, str) else ""
    
    def _clean_text(self, text:str) -> str:
        """
        Clean the text by removing unknown symbols, emojis, and replacing links and mentions with placeholders.

        Args:
            text (str): The input text to clean.

        Returns:
            str: The cleaned text.
        """
        text = self._remove_unknown_symbols(text)
        text = self._remove_emoji(text)
        text = self._replace_mentions(text)
        return self._replace_links(text)
    
    def _remove_unknown_symbols(self, text:str) -> str:
        """
        Remove unknown symbols from the text by encoding it in the specified encoding and then decoding it back to a string.

        Args:
            text (str): The input text that may contain unknown symbols.

        Returns:
            str: The text with unknown symbols removed.
        """
        return text.encode(self.encoding, "ignore").decode(self.encoding)
    
    def _remove_emoji(self, text:str) -> str:
        """
        Remove emojis from the text.

        Args:
            text (str): The input text containing emojis.

        Returns:
            str: The text with emojis removed.
        """
        return demoji.replace(text)
    
    def _replace_links(self, text:str) -> str:
        """
        Replace links in the text with a placeholder.

        Args:
            text (str): The input text containing links.

        Returns:
            str: The text with links replaced by the link placeholder.
        """
        return re.sub(r'http[s]?://\S+', self.link_placeholder, text).strip()
    
    def _replace_mentions(self, text:str) -> str:
        """
        Replace user mentions in the text with a placeholder.

        Args:
            text (str): The input text containing user mentions.

        Returns:
            str: The text with user mentions replaced by the mention placeholder.
        """
        return re.sub(r'@\w+', self.mention_placeholder, text).strip()