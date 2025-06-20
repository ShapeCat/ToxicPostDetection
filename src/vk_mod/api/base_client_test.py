import pytest
from .exceptions import VKAPIError
from .base_client import BaseAPIClient


@pytest.fixture
def api_client_fixture():
    return BaseAPIClient(community_token="test_community_token")


def test_initialize_success():
    community_token = "test_community_token"
    client = BaseAPIClient(community_token=community_token)
    assert client.community_token == community_token


def test_post_request_success(api_client_fixture, requests_mock):
    method = "users.get"
    params = {
        "user_ids": "1",
        "name": "Name"
    }
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
    assert f"access_token={api_client_fixture.community_token}" in requests_mock.last_request.url
    assert f"v={api_client_fixture.api_version}" in requests_mock.last_request.url


def test_get_request_success(api_client_fixture, requests_mock):
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
    assert f"access_token={api_client_fixture.community_token}" in requests_mock.last_request.url
    assert f"v={api_client_fixture.api_version}" in requests_mock.last_request.url


def test_post_request_api_error(api_client_fixture, requests_mock):
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

    with pytest.raises(VKAPIError):
        api_client_fixture.post_request(method, params)


def test_get_request_api_error(api_client_fixture, requests_mock): 
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

    with pytest.raises(VKAPIError):
        api_client_fixture.get_request(method, params)


def test_post_request_custom_token_success(api_client_fixture, requests_mock):
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
    assert f"access_token={custom_token}" in requests_mock.last_request.url
    assert f"v={api_client_fixture.api_version}" in requests_mock.last_request.url


def test_get_request_custom_token_success(api_client_fixture, requests_mock):
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
    assert f"access_token={custom_token}" in requests_mock.last_request.url
    assert f"v={api_client_fixture.api_version}" in requests_mock.last_request.url
