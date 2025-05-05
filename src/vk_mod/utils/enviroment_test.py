import pytest
from environment import load_env


def test_load_env_read_string_return_int(mocker):
    mock_env_file = {"MAX_RETRIES": "5"}
    mocker.patch("environment.dotenv_values", return_value=mock_env_file)
    
    result = load_env("MAX_RETRIES", 0)
    assert result == 5
    assert isinstance(result, int)

def test_load_env_read_string_return_bool(mocker):
    mock_env_file = {
        "BOOL_1": "1",
        "BOOL_YES": "yes",
        "BOOL_ON": "on",
        "BOOL_TRUE": "true"
    }
    mocker.patch("environment.dotenv_values", return_value=mock_env_file)
    
    assert load_env("BOOL_1", False) is True
    assert load_env("BOOL_YES", False) is True
    assert load_env("BOOL_ON", False) is True
    assert load_env("BOOL_TRUE", False) is True

def test_load_env_read_string_return_float(mocker):
    mock_env_file = {"RATING": "4.5"}
    mocker.patch("environment.dotenv_values", return_value=mock_env_file)
    
    result = load_env("RATING", 0.0)
    assert result == 4.5
    assert isinstance(result, float)

def test_load_env_read_invalid_return_default(mocker):
    mock_env_file = {"PORT": "invalid"}
    mocker.patch("environment.dotenv_values", return_value=mock_env_file)
    
    result = load_env("PORT", 8080)
    assert result == 8080 

def test_load_env_read_file(mocker):
    mock = mocker.patch("environment.dotenv_values")
    load_env("VAR", "default")
    mock.assert_called_once_with("../.env") 

def test_load_env_missing_value_return_default(mocker):
    mock_env_file = {}
    mocker.patch("environment.dotenv_values", return_value=mock_env_file)
    result = load_env("MISSING_VAR", "default")
    assert result == "default"

def test_load_env_missing_value_no_default_return_none(mocker):
    mock_env_file = {}
    mocker.patch("environment.dotenv_values", return_value=mock_env_file)
    result = load_env("MISSING_VAR")
    assert result is None
