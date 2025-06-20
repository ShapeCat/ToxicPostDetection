import pytest
from .base_client import BaseAPIClient
from .chat_client import ChatClient


@pytest.fixture
def chat_client():  
    return ChatClient(community_token="community_token")


def test_send_message_success(chat_client, requests_mock):
    user_id = 12345
    message = "Test message"
    expected_response = {"response": 1}
    requests_mock.post(f"{BaseAPIClient.url}messages.send", json=expected_response)
    
    result = chat_client.send(user_id, message)

    assert result == expected_response["response"]
    assert f"peer_id={user_id}" in requests_mock.last_request.url
    assert f"message={'+'.join(message.split())}" in requests_mock.last_request.url
    assert "random_id" in requests_mock.last_request.url


def test_get_message_by_id_success(chat_client, requests_mock):
    user_id = 12345
    message_id = 1
    expected_response = {
        "response": 
        {"items": [
            {"id": 1}
            ]
        }
    }
    requests_mock.get(f"{BaseAPIClient.url}messages.getById", json=expected_response)
    
    result = chat_client.get_by_id(user_id, message_id)

    assert isinstance(result, dict) 
    assert result["id"] == 1
    assert f"peer_id={user_id}" in requests_mock.last_request.url
    assert f"message_ids={message_id}" in requests_mock.last_request.url


def test_get_all_chat_messages_success(chat_client, requests_mock):
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
    user_id = 12345
    message_id = 1
    excpected_response = {"response": 1}
    requests_mock.post(f"{BaseAPIClient.url}messages.delete", json=excpected_response)
    
    response = chat_client.delete(user_id, message_id, delete_for_all=delete_for_all)

    assert response
    assert f"delete_for_all={1 if delete_for_all else 0}" in requests_mock.last_request.url
    assert f"peer_id={user_id}" in requests_mock.last_request.url
    assert f"message_id={message_id}" in requests_mock.last_request.url


def test_edit_message_success(chat_client, requests_mock):
    user_id = 12345
    message_id = 1
    mew_text = "New text"
    expected_response = {"response": 1}
    requests_mock.post(f"{BaseAPIClient.url}messages.edit", json=expected_response)
    
    result = chat_client.edit(user_id, message_id, mew_text)
    
    assert result 
    assert f"peer_id={user_id}" in requests_mock.last_request.url
    assert f"cmid={message_id}" in requests_mock.last_request.url
    assert f"message={mew_text.replace(' ', '+')}" in requests_mock.last_request.url
