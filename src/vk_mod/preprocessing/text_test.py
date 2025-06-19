import pytest
from .text import TextPreprocessor


def test_default_initialization_success():
    preprocessor = TextPreprocessor()
    assert preprocessor.mention_placeholder == "УПОМЯНАНИЕ"
    assert preprocessor.link_placeholder == "ССЫЛКА"
    assert preprocessor.encoding == "utf-8"


def test_custom_initialization_success():
    custom_link_placeholder = "LINK"
    custom_mention_placeholder = "MENTION"
    custom_encoding = "ascii"
    preprocessor = TextPreprocessor(
            link_placeholder=custom_link_placeholder, 
            mention_placeholder=custom_mention_placeholder,
            encoding=custom_encoding
        )
    assert preprocessor.link_placeholder == custom_link_placeholder
    assert preprocessor.mention_placeholder == custom_mention_placeholder
    assert preprocessor.encoding == custom_encoding


@pytest.mark.parametrize('encoding, input_data, expected', [
    ("cp1251", "Цена: ¥1000", "Цена: 1000"),
    ('utf-8', "Привет! 你好! 😊", "Привет! 你好! 😊")
])
def test_remove_unknown_symbols_success(encoding, input_data, expected):
    preprocessor = TextPreprocessor(encoding=encoding)
    result = preprocessor._remove_unknown_symbols(input_data)
    assert result == expected


@pytest.mark.parametrize('input_data, expected', [
    ("Привет 😊", "Привет "),
    ("Hello 😂", "Hello ")
])
def test_remove_emoji_success(input_data, expected):
    preprocessor = TextPreprocessor()
    result = preprocessor._remove_emoji(input_data)
    assert result == expected


@pytest.mark.parametrize('placeholder, input_data, expected', [
    ("default", "@user привет", "УПОМЯНАНИЕ привет"),
    ("MENTION", "Hello @user", "Hello MENTION")
])
def test_replace_mentions_success(placeholder, input_data, expected):
    if placeholder != "default":
        preprocessor = TextPreprocessor(mention_placeholder=placeholder)
    else:
        preprocessor = TextPreprocessor()
    result = preprocessor._replace_mentions(input_data)
    assert result == expected


@pytest.mark.parametrize('placeholder, input_data, expected', [
    ("default", "Заходите на https://example.com", "Заходите на ССЫЛКА"),
    ("default", "Заходите на http://test.ru", "Заходите на ССЫЛКА"),
    ("LINK", "Visit http://test.ru", "Visit LINK")
])
def test_replace_links_success(placeholder, input_data, expected):
    if placeholder != "default":
        preprocessor = TextPreprocessor(link_placeholder=placeholder)
    else:
        preprocessor = TextPreprocessor()
    result = preprocessor._replace_links(input_data)
    assert result == expected


@pytest.mark.parametrize("input_data, expected", [
        (None, ""),
        (123, ""),
        ([], ""),
        ("Текст", "Текст"),
        (" @me Напиши мне на http://site.com 😊! ¥", "УПОМЯНАНИЕ Напиши мне на ССЫЛКА ! ¥")
])
def test_clean_success(input_data, expected):
    preprocessor = TextPreprocessor()
    assert preprocessor.clean(input_data) == expected
