import pytest
from .exceptions import VKAPIError
from .base_client import BaseAPIClient


@pytest.fixture
def api_client_fixture():
    """
    Fixture to provide a BaseAPIClient instance for testing.

    Returns:
        BaseAPIClient: An instance of BaseAPIClient initialized with test access, community, and service keys.
    """
    return BaseAPIClient(
        community_token="test_community_token",
    )


def test_post_request_success(api_client_fixture, requests_mock):
    """
    Test that a successful POST request is handled correctly by BaseAPIClient.

    GIVEN: A BaseAPIClient instance and a mocked successful VK API response
    WHEN:  post_request is called with valid method and parameters
    THEN:  the response is parsed correctly, and the access token/version are included in the URL
    """
    method = "users.get"
    params = {"user_ids": "1", "name": "Name"}
    url = f"{api_client_fixture.url}{method}"
    expected_response = {
        "response": 
        {
            "id": 1
        }
    }
    requests_mock.post(url, json=expected_response)

    response = api_client_fixture.post_request(method, params)
    assert response == expected_response["response"]
    assert requests_mock.last_request.url.startswith(url)
    assert "access_token=test_community_token" in requests_mock.last_request.url
    assert "v=5.199" in requests_mock.last_request.url


def test_get_request_success(api_client_fixture, requests_mock):
    """
    Test that a successful GET request is handled correctly by BaseAPIClient.

    GIVEN: A BaseAPIClient instance and a mocked successful VK API response
    WHEN:  get_request is called with valid method and parameters
    THEN:  the response is parsed correctly, and the access token/version are included in the URL
    """
    method = "users.get"
    params = {"user_ids": "1"}
    url = f"{api_client_fixture.url}{method}"
    expected_response = {
        "response": {
            "id": 1,
            "name": "user"
        }
    }
    requests_mock.get(url, json=expected_response)

    response = api_client_fixture.get_request(method, params)
    assert response == expected_response["response"]
    assert requests_mock.last_request.url.startswith(url)
    assert "access_token=test_community_token" in requests_mock.last_request.url
    assert "v=5.199" in requests_mock.last_request.url


def test_post_request_api_error(api_client_fixture, requests_mock):
    """
    Test that VK API errors in POST requests raise VKAPIError with correct details.

    GIVEN: A BaseAPIClient instance and a mocked VK API error response
    WHEN:  post_request is called with invalid parameters
    THEN:  a VKAPIError is raised with the error message and code from the API response [[1]]
    """
    method = "users.get"
    params = {"user_ids": "1", "name": "Name"}
    url = f"{api_client_fixture.url}{method}"
    expected_error_code = 5
    expected_error_msg = "Not found"
    expected_response = {
        "error": {
            "error_code": expected_error_code,
            "error_msg": expected_error_msg
        }
    }
    requests_mock.post(url, json=expected_response)

    with pytest.raises(VKAPIError) as exc_info:
        api_client_fixture.post_request(method, params)
    assert str(exc_info.value) == f"There is an error while calling VK API {method} method: {expected_error_msg}({expected_error_code})"


def test_get_request_api_error(api_client_fixture, requests_mock):
    """
    Test that VK API errors in GET requests raise VKAPIError with correct details.

    GIVEN: A BaseAPIClient instance and a mocked VK API error response
    WHEN:  get_request is called with invalid parameters
    THEN:  a VKAPIError is raised with the error message and code from the API response [[8]]
    """
    method = "users.get"
    params = {"user_ids": "1"}
    url = f"{api_client_fixture.url}{method}"
    expected_error_code = 5
    expected_error_msg = "Not found"
    expected_response = {
        "error": {
            "error_code": expected_error_code,
            "error_msg": expected_error_msg
        }
    }
    requests_mock.get(url, json=expected_response)

    with pytest.raises(VKAPIError) as exc_info:
        api_client_fixture.get_request(method, params)
    assert str(exc_info.value) == f"There is an error while calling VK API {method} method: {expected_error_msg}({expected_error_code})"


def test_post_request_custom_token_success(api_client_fixture, requests_mock):
    """
    Test that a custom access token is used in POST requests.

    GIVEN: A BaseAPIClient instance and a mocked successful VK API response
    WHEN:  post_request is called with a custom access token
    THEN:  the custom token is included in the request URL instead of the default token [[6]]
    """
    method = "users.get"
    params = {"user_ids": "1", "name": "Name"}
    custom_token = "custom_access_token"
    url = f"{api_client_fixture.url}{method}"
    expected_response = {
        "response": {
            "id": 1,
        }
    }
    requests_mock.post(url, json=expected_response)

    response = api_client_fixture.post_request(method, params, access_token=custom_token)
    assert response == expected_response["response"]
    assert requests_mock.last_request.url.startswith(url)
    assert "access_token=custom_access_token" in requests_mock.last_request.url
    assert "v=5.199" in requests_mock.last_request.url


def test_get_request_custom_token_success(api_client_fixture, requests_mock):
    """
    Test that a custom access token is used in GET requests.

    GIVEN: A BaseAPIClient instance and a mocked successful VK API response
    WHEN:  get_request is called with a custom access token
    THEN:  the custom token is included in the request URL instead of the default token [[6]]
    """
    method = "users.get"
    params = {"user_ids": "1"}
    custom_token = "custom_access_token"
    url = f"{api_client_fixture.url}{method}"
    expected_response = {
        "response": {
            "id": 1,
            "name": "user"
        }
    }
    requests_mock.get(url, json=expected_response)

    response = api_client_fixture.get_request(method, params, access_token=custom_token)
    assert response == expected_response["response"]
    assert requests_mock.last_request.url.startswith(url)
    assert "access_token=custom_access_token" in requests_mock.last_request.url
    assert "v=5.199" in requests_mock.last_request.url
