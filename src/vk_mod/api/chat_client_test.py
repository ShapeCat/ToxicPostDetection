import pytest
from .base_client import BaseAPIClient
from .chat_client import ChatClient


@pytest.fixture
def chat_client():  
    """
    Fixture to provide a ChatClient instance for testing.

    Returns:
        ChatClient: A ChatClient instance with test access, community, and service keys.
    """
    return ChatClient(
        community_token="community_token",
    )


def test_send_message_success(chat_client, requests_mock):
    """
    Test that send_message_to_admin sends a message to the admin successfully.

    GIVEN: A ChatClient instance and a mocked VK API response
    WHEN:  send_message_to_admin is called with a message
    THEN:  the response is parsed correctly, and the URL contains the correct parameters
    """
    user_id = 12345
    expected_response = {"response": 1}
    requests_mock.post(f"{BaseAPIClient.url}messages.send", json=expected_response)
    
    result = chat_client.send("Test message", user_id)
    assert result == expected_response["response"]
    assert f"peer_id={user_id}" in requests_mock.last_request.url
    assert "message=Test+message" in requests_mock.last_request.url
    assert "random_id" in requests_mock.last_request.url


def test_get_message_by_id_success(chat_client, requests_mock):
    """
    Test that get_message_by_id retrieves a message by id successfully.

    GIVEN: A ChatClient instance and a mocked VK API response
    WHEN:  get_message_by_id is called with a message id
    THEN:  the response is parsed correctly, and the URL contains the correct parameters
    """
    user_id = 12345
    expected_response = {
        "response": 
        {"items": [
            {"id": 1}
            ]
        }
    }
    requests_mock.get(f"{BaseAPIClient.url}messages.getById", json=expected_response)
    
    result = chat_client.get_by_id(1, user_id)
    assert isinstance(result, list) 
    assert result[0]["id"] == 1
    assert f"peer_id={user_id}" in requests_mock.last_request.url


def test_get_all_chat_messages_success(chat_client, requests_mock):
    """
    Test that get_all_chat_messages retrieves the correct number of messages.

    GIVEN: A ChatClient instance and a mocked VK API response
    WHEN:  get_all_chat_messages is called with a specified count
    THEN:  the response contains the correct number of items, and the URL includes the correct parameters
    """
    user_id = 12345
    count = 5
    expected_response = {
        "response": 
        {"items": [
            {"id": 1}, 
            {"id": 2}
            ]
        }
    }
    requests_mock.get(f"{BaseAPIClient.url}messages.getHistory", json=expected_response)
    
    result = chat_client.get_all(user_id, count=count)
    assert len(result) == 2 
    assert f"peer_id={user_id}" in requests_mock.last_request.url
    assert f"count={count}" in requests_mock.last_request.url


@pytest.mark.parametrize("delete_for_all", [True, False])
def test_delete_message_parametrize_success(chat_client, requests_mock, delete_for_all):
    """
    Test that delete_message successfully deletes a message with and without the delete_for_all parameter.

    GIVEN: A ChatClient instance and a mocked VK API response
    WHEN:  delete_message is called with a message id and the delete_for_all parameter with a value of True or False
    THEN:  the response is parsed correctly, and the URL contains the correct parameters
    """
    user_id = 12345
    delete_for_all = 1 if delete_for_all else 0
    cmids = 1
    excpected_response = {"response": 1}
    requests_mock.post(f"{BaseAPIClient.url}messages.delete", json=excpected_response)
    
    response = chat_client.delete(user_id, cmids, delete_for_all=delete_for_all)
    assert response == 1
    assert f"delete_for_all={delete_for_all}" in requests_mock.last_request.url
    assert f"peer_id={user_id}" in requests_mock.last_request.url
    assert f"cmids={cmids}" in requests_mock.last_request.url


def test_edit_message_success(chat_client, requests_mock):
    """
    Test that edit_message successfully edits a message.

    GIVEN: A ChatClient instance and a mocked VK API response
    WHEN:  edit_message is called with a message id and new text
    THEN:  the response is parsed correctly, and the URL contains the correct parameters
    """
    user_id = 12345
    cmids = 1
    mew_text = "New text"
    expected_response = {"response": 1}
    requests_mock.post(f"{BaseAPIClient.url}messages.edit", json=expected_response)
    
    result = chat_client.edit(user_id, cmids, mew_text)
    assert result == 1 
    assert f"peer_id={user_id}" in requests_mock.last_request.url
    assert f"cmid={cmids}" in requests_mock.last_request.url
    assert f"message={mew_text.replace(' ', '+')}" in requests_mock.last_request.url
