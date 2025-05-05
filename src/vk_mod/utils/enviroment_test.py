import pytest
from environment import load_env


def test_load_env_exists(mocker):
    mock_env_file = {"TEST_VAR": "test_value"}
    mock = mocker.patch("environment.dotenv_values", return_value=mock_env_file)
    
    result = load_env("TEST_VAR", "default_value")

    assert result == "test_value"  
    mock.assert_called_once_with("../.env") 

def test_load_env_missing_with_default(mocker):
    mock_env_file = {}
    mock = mocker.patch("environment.dotenv_values", return_value=mock_env_file)
    
    result = load_env("MISSING_VAR", "default_value")

    assert result == "default_value"
    mock.assert_called_once_with("../.env")

def test_load_env_missing_no_default(mocker):
    mock_env_file = {}
    mock = mocker.patch("environment.dotenv_values", return_value=mock_env_file)
    
    result = load_env("MISSING_VAR")

    assert result is None
    mock.assert_called_once_with("../.env")

def test_load_env_error(mocker, capsys):
    mock = mocker.patch("environment.dotenv_values", side_effect=Exception("Test exception"))
    
    result = load_env("TEST_VAR", default_value="fallback")
    captured = capsys.readouterr()

    assert result == "fallback"
    assert "There is an error while reading .env file: Test exception" in captured.out
    mock.assert_called_once_with("../.env")
