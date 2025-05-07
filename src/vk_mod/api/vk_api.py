from .wall_client import WallAPIClient
from .chat_client import ChatClient


class VK_API:
    def __init__(self, access_token:str, community_token:str, service_key:str, admin_id:int):
        """
        Initialize a VK_API instance.

        Args:
            access_token (str): The access token for the VK API.
            community_token (str): The community token for the VK API.
            service_key (str): The service key for the VK API.
            admin_id (int): The administrator ID for the chat client.
        """
        self.wall = WallAPIClient(access_token, community_token, service_key)
        self.chat = ChatClient(access_token, community_token, service_key, admin_id)
    