import pytest
from .vk_api import VK_API  
from .wall_client import WallAPIClient
from .chat_client import ChatClient


def test_vk_api_init_success():
    """
    Test that VK_API is initialized successfully with valid parameters.

    GIVEN: Valid access, community, service keys, and an admin ID
    WHEN:  A VK_API instance is created
    THEN:  The instance should have a WallAPIClient and a ChatClient
    """
    access_token = "test_access_token"
    community_token = "test_community_token"
    service_key = "test_service_key"
    admin_id = 12345

    vk_api = VK_API(
        access_token=access_token,
        community_token=community_token,
        service_key=service_key,
        admin_id=admin_id
        )
    assert isinstance(vk_api.wall, WallAPIClient)
    assert isinstance(vk_api.chat, ChatClient)


def test_vk_api_init_string_admin_id_success():
    """
    Test that VK_API is initialized successfully with a string admin ID.

    GIVEN: Valid access, community, service keys, and a string admin ID
    WHEN:  A VK_API instance is created
    THEN:  The instance should have a WallAPIClient and a ChatClient, and the admin ID should be converted to an integer
    """
    access_token = "test_access_token"
    community_token = "test_community_token"
    service_key = "test_service_key"
    admin_id = "12345"

    vk_api = VK_API(access_token=access_token,
                    community_token=community_token,
                    service_key=service_key,
                    admin_id=admin_id)
    assert vk_api.chat.admin_id == 12345


@pytest.mark.parametrize("admin_id", [None, "", "qwerty"])
def test_vk_api_init_invalid_admin_id_exception(admin_id):
    """
    Test that VK_API initialization raises an exception when given an invalid admin ID.

    GIVEN: An invalid admin ID (None, empty string, or a string that can't be converted to an integer)
    WHEN:  A VK_API instance is created
    THEN:  A ValueError should be raised, with a message indicating that the admin ID must be convertible to an integer
    """
    access_token = "test_access_token"
    community_token = "test_community_token"
    service_key = "test_service_key"

    with pytest.raises(ValueError) as exc_info:
        VK_API(access_token=access_token,
               community_token=community_token,
               service_key=service_key,
               admin_id=admin_id)
    assert "admin_id must be convertible to integer" in str(exc_info.value)
