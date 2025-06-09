from random import randint
from .base_client import BaseAPIClient


class ChatClient(BaseAPIClient):
    def __init__(self, community_token:str, admin_id:int):
        """
        Initialize a ChatClient instance.

        Args:
            access_token (str): The access token for the VK API.
            community_token (str): The community token for the VK API.
            service_key (str): The service key for the VK API.
            admin_id (int): The administrator ID for the chat client.
        """
        super().__init__(community_token)
        self.admin_id = admin_id

    def send_message_to_admin(self, message:str) -> int:
        """
        Send a message to the admin.

        Args:
            message (str): The message to be sent.

        Returns:
            int: The message ID of the sent message.
        """
        params = {
            'peer_id': self.admin_id,
            'message': message,
            'random_id': randint(1, 10*5)

        }
        response = self.post_request("messages.send", params)
        return response

    def get_message_by_id(self, message_id:int) -> list[dict[str, str]]:
        """
        Get a message by its ID.

        Args:
            message_id (int): The message ID to be retrieved.

        Returns:
            list[dict[str, str]]: A list containing a single message dictionary.

        Raises:
            VKAPIError: If the VK API returns an error.
        """
        params = {
            'peer_id': self.admin_id,
            'cmids': message_id,
        }
        response = self.get_request("messages.getById", params)
        return response['items']

    def get_all_chat_messages(self, count:int=200) -> list[dict[str, str]]:
        """
        Get all messages in the chat.

        Args:
            count (int, optional): The number of messages to retrieve. Defaults to 200.

        Returns:
            list[dict[str, str]]: A list of message dictionaries.

        Raises:
            VKAPIError: If the VK API returns an error.
        """
        params = {
            'peer_id': self.admin_id,
            'count': count,
        }
        response = self.get_request("messages.getHistory", params, self.community_token)
        return response['items']
    
    def delete_message(self, message_id:int, delete_for_all:bool=True) -> int:  
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
            'peer_id': self.admin_id,
            'cmids': message_id,
            'delete_for_all': 1 if delete_for_all else 0,
        }
        response = self.post_request("messages.delete", params, self.community_token)
        return response

    def edit_message(self, message_id:int, message:str) -> int:
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
            'peer_id': self.admin_id,
            'cmid': message_id,
            'message': message,
        }
        response = self.post_request("messages.edit", params)
        return response
