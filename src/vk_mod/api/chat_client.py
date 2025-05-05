from random import randint
from .base_client import BaseAPIClient


class ChatClient(BaseAPIClient):
    def __init__(self, access_token:str, community_token:str, service_key:str, admin_id:int):
        super().__init__(access_token, community_token, service_key)
        self.admin_id = admin_id

    def send_message_to_admin(self, message:str) -> int:
        params = {
            'peer_id': self.admin_id,
            'message': message,
            'random_id': randint(1, 10*5)

        }
        response = self.post_request("messages.send", params, self.community_token)
        return response

    def get_message_by_id(self, message_id:int) -> list[dict[str, str]]:
        params = {
            'peer_id': self.admin_id,
            'cmids': message_id,
        }
        response = self.get_request("messages.getById", params, self.community_token)
        return response['items']

    def get_all_chat_messages(self, count:int=200) -> list[dict[str, str]]:
        params = {
            'peer_id': self.admin_id,
            'count': count,
        }
        response = self.get_request("messages.getHistory", params, self.community_token)
        return response['items']

    def delete_message(self, message_id:int, delete_for_all:bool=True) -> list[dict[str, str]]:  
        params = {
            'peer_id': self.admin_id,
            'cmids': message_id,
            'delete_for_all': 1 if delete_for_all else 0,
        }
        response = self.get_request("messages.delete", params, self.community_token)
        return response

    def edit_message(self, message_id:int, message:str) -> int:
        params = {
            'peer_id': self.admin_id,
            'cmid': message_id,
            'message': message,
        }
        response = self.get_request("messages.edit", params, self.community_token)
        return response
