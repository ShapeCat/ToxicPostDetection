from .wall_client import WallAPIClient
from .chat_client import ChatClient


class VK_API:
    def __init__(self, access_token:str, community_token:str, service_key:str, admin_id:int|str):
        """
        Initialize a VK_API instance.

        Args:
            access_token (str): The access token for the VK API.
            community_token (str): The community token for the VK API.
            service_key (str): The service key for the VK API.
            admin_id (int|str): The administrator ID for the chat client. Can be either an integer or a str which can be converted to an integer.

        Raises:
            ValueError: If admin_id is not convertible to integer.
        """
        if not isinstance(admin_id, int):
            try:
                admin_id = int(admin_id)
            except (ValueError, TypeError):
                raise ValueError("admin_id must be convertible to integer")
        self.wall = WallAPIClient(access_token, community_token, service_key)
        self.chat = ChatClient(access_token, community_token, service_key, admin_id)
    