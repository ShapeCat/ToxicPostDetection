import pytest
from environment import load_config, NoOptionError, NoSectionError


TEST_CONFIG = """
[section]
str_value = Строка
int_value = 4
float_value = 4.44
bool_value = true
"""


@pytest.fixture
def temp_config(tmp_path):
    def generate_ini_file(content):
        ini_file_path = tmp_path / "config.ini"
        ini_file_path.write_text(content)
        return str(ini_file_path)
    return generate_ini_file


@pytest.mark.parametrize("return_type, expected", [
    ("str", "Строка"),
    ("bool", True),
])
def test_load_str_value_exists(tmp_config, return_type, expected):
    ini_path = tmp_config(TEST_CONFIG)
    assert load_config("section", "str_value", file_path=ini_path, return_type=return_type) == expected


@pytest.mark.parametrize("return_type, expected", [
    ("bool", True),
    ("str", "true"),
])
def test_load_bool_value_exists(tmp_config, return_type, expected):
    ini_path = tmp_config(TEST_CONFIG)
    assert load_config("section", "bool_value", file_path=ini_path, return_type=return_type) == expected


@pytest.mark.parametrize("return_type, expected", [
    ("int", 4),
    ("str", "4"), 
    ("bool", True), 
])
def test_load_int_value_exists(tmp_config, return_type, expected):
    ini_path = tmp_config(TEST_CONFIG)
    assert load_config("section", "int_value", file_path=ini_path, return_type=return_type) == expected


@pytest.mark.parametrize("return_type, expected", [
    ("float", 4.44),
    ("str", "4.44"),
    ("bool", True),
])
def test_load_float_value_exists(tmp_config, return_type, expected):
    ini_path = tmp_config(TEST_CONFIG)
    assert load_config("section", "float_value", file_path=ini_path, return_type=return_type) == expected


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_config("section", "str_value", file_path="missing.ini")
    assert load_config("section", "str_value", file_path="missing.ini", default_value="default") == "default"


def test_missing_section(tmp_config):
    ini_path = tmp_config(TEST_CONFIG)
    with pytest.raises(NoSectionError):
        load_config("missing_section", "str_value", file_path=ini_path)
    assert load_config("missing_section", "str_value", file_path=ini_path, default_value="default") == "default"


def test_missing_key(tmp_config):
    ini_path = tmp_config(TEST_CONFIG)
    with pytest.raises(NoOptionError):
        load_config("section", "missing_key", file_path=ini_path)
    assert load_config("section", "missing_key", file_path=ini_path, default_value="default") == "default"


@pytest.mark.parametrize("key, return_type", [
    ("str_value", "int"), 
    ("str_value", 'float'),
])
def test_conversion_error(tmp_config, key, return_type):
    ini_path = tmp_config(TEST_CONFIG)
    with pytest.raises(ValueError):
        load_config("section", key, file_path=ini_path, return_type=return_type)
    assert load_config("section", key, file_path=ini_path, return_type=return_type, default_value="default") == "default"
