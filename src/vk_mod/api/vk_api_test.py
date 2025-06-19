from .vk_api import VK_API  
from .wall_client import WallClient
from .chat_client import ChatClient
from .longpoll_client import LongPollClient
from .users_client import UserClient
from .community_client import CommunityClient


def test_vk_api_init_success():
    """
    Test that VK_API is initialized successfully with valid parameters.

    GIVEN: Valid access, community, service keys, and an admin ID
    WHEN:  A VK_API instance is created
    THEN:  The instance should have a WallAPIClient and a ChatClient
    """
    access_token = "test_access_token"
    community_token = "test_community_token"

    vk_api = VK_API(
        access_token=access_token,
        community_token=community_token,
        )
    assert isinstance(vk_api.wall, WallClient)
    assert isinstance(vk_api.chat, ChatClient)
    assert isinstance(vk_api.longpoll, LongPollClient)
    assert isinstance(vk_api.community, CommunityClient)
    assert isinstance(vk_api.user, UserClient)
