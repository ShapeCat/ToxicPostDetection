from .wall_client import WallAPIClient
from .chat_client import ChatClient


class VK_API:
    def __init__(self, access_token:str, community_token:str, service_key:str, admin_id:int):
        self.wall = WallAPIClient(access_token, community_token, service_key)
        self.chat = ChatClient(access_token, community_token, service_key, admin_id)
    