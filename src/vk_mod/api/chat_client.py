from random import randint
from .base_client import BaseAPIClient


class ChatClient(BaseAPIClient):
    def send(self, message:str, user_id:str) -> int:
        params = {
            'peer_id': user_id,
            'message': message,
            'random_id': randint(1, 10*5)

        }
        response = self.post_request("messages.send", params)
        return response

    def get_by_id(self, message_id:int, user_id:str) -> list[dict[str, str]]:
        params = {
            'peer_id': user_id,
            'cmids': message_id,
        }
        response = self.get_request("messages.getById", params)
        return response['items']

    def get_all(self, user_id:str, count:int=200) -> list[dict[str, str]]:
        params = {
            'peer_id': user_id,
            'count': count,
        }
        response = self.get_request("messages.getHistory", params, self.community_token)
        return response['items']
    
    def delete(self, user_id:str, message_id:int, delete_for_all:bool=True) -> int:  
        """
        Delete a message by its ID.

        Args:
            message_id (int): The ID of the message to be deleted.
            delete_for_all (bool, optional): If True, delete the message for all chat members. If False, delete only for the user. Defaults to True.

        Returns:
            int: The result of the delete operation.

        Raises:
            VKAPIError: If the VK API returns an error.
        """
        params = {
            'peer_id': user_id,
            'cmids': message_id,
            'delete_for_all': 1 if delete_for_all else 0,
        }
        response = self.post_request("messages.delete", params, self.community_token)
        return response

    def edit(self, user_id:str, message_id:int, message:str) -> int:
        """
        Edit a message by its ID.

        Args:
            message_id (int): The ID of the message to be edited.
            message (str): The new text of the message.

        Returns:
            int: The result of the edit operation.

        Raises:
            VKAPIError: If the VK API returns an error.
        """
        params = {
            'peer_id': user_id,
            'cmid': message_id,
            'message': message,
        }
        response = self.post_request("messages.edit", params)
        return response
