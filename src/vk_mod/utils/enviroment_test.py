import pytest
from environment import load_env


def test_load_env_read_string_return_int(mocker):  
    """
    Test that load_env will convert a string from the .env file into an int.

    GIVEN: a .env file with a string value
    WHEN:  load_env is called with the name of the value and a default value
    THEN:  the result is an int with the same value as the string
    """
    
    mock_env_file = {"MAX_RETRIES": "5"}
    mocker.patch("environment.dotenv_values", return_value=mock_env_file)
    
    result = load_env("MAX_RETRIES", 0)
    assert result == 5
    assert isinstance(result, int)

def test_load_env_read_string_return_bool(mocker):
    """
    Test that load_env will convert various string representations of truthy values to boolean True.

    GIVEN: a .env file containing string representations of truthy boolean values
    WHEN:  load_env is called with the name of the value and a default boolean value
    THEN:  the result is True for all the truthy string representations
    """
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
    """
    Test that load_env will convert a string from the .env file into a float.

    GIVEN: a .env file with a string value
    WHEN:  load_env is called with the name of the value and a default float value
    THEN:  the result is a float with the same value as the string
    """
    mock_env_file = {"RATING": "4.5"}
    mocker.patch("environment.dotenv_values", return_value=mock_env_file)
    
    result = load_env("RATING", 0.0)
    assert result == 4.5
    assert isinstance(result, float)

def test_load_env_read_invalid_return_default(mocker):
    """
    Test that load_env will return the default value if the value from the .env file cannot be converted to the requested type.

    GIVEN: a .env file with an invalid value
    WHEN:  load_env is called with the name of the value and a default value
    THEN:  the result is the default value
    """
    mock_env_file = {"PORT": "invalid"}
    mocker.patch("environment.dotenv_values", return_value=mock_env_file)
    
    result = load_env("PORT", 8080)
    assert result == 8080 

def test_load_env_read_file(mocker):
    """
    Test that load_env will read the .env file if it exists and not mock it out.

    GIVEN: a valid .env file
    WHEN:  load_env is called
    THEN:  the .env file is read and the expected value is returned
    """
    mock = mocker.patch("environment.dotenv_values")
    load_env("VAR", "default")
    mock.assert_called_once_with("../.env") 

def test_load_env_missing_value_return_default(mocker):
    """
    Test that load_env will return the default value if the value is not present in the .env file.

    GIVEN: a .env file with no value
    WHEN:  load_env is called with the name of the value and a default value
    THEN:  the result is the default value
    """
    mock_env_file = {}
    mocker.patch("environment.dotenv_values", return_value=mock_env_file)
    result = load_env("MISSING_VAR", "default")
    assert result == "default"

def test_load_env_missing_value_no_default_return_none(mocker):
    """
    Test that load_env will return None if the value is not present in the .env file and no default value is provided.

    GIVEN: a .env file with no value
    WHEN:  load_env is called with the name of the value and no default value
    THEN:  the result is None
    """
    mock_env_file = {}
    mocker.patch("environment.dotenv_values", return_value=mock_env_file)
    result = load_env("MISSING_VAR")
    assert result is None
