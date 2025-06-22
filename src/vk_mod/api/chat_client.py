from random import randint
from .base_client import BaseAPIClient


class ChatClient(BaseAPIClient):
    def send(self,
             user_id: str,
             text: str,         
             ) -> int:
        """Send a message to a user.

        Args:
            user_id (str): The id of the user to send the message to.
            text (str): The text of the message to send.

        Returns:
            int: The id of the sent message.
        """
        params = {
            'peer_id': user_id,
            'message': text,
            'random_id': randint(1, 10**5)
        }
        response = self.post_request("messages.send", params)
        return response

    def get_by_id(self,
                  message_id: int            
                  ) -> dict[str, str]:
        """Get a message by id from a chat.

        Args:
            user_id (str): The id of the user to retrieve the message from.
            message_id (int): The id of the message to retrieve.

        Returns:
            dict[str, str]: The retrieved message.
        """
        params = {
            'message_ids': message_id,
        }
        response = self.get_request("messages.getById", params)
        return response['items'][0]

    def get_all(self,
                user_id: str,
                count: int = 200
                ) -> list[dict[str, str]]:
        """Get all messages from a chat.

        Args:
            user_id (str): The id of the user to retrieve the messages from.
            count (int): The number of messages to retrieve. Defaults to 200.

        Returns:
            list[dict[str, str]]: The retrieved messages.
        """
        params = {
            'peer_id': user_id,
            'count': count,
        }
        response = self.get_request("messages.getHistory", params)
        return response['items']
    
    def delete(self,
               chat_id: str,
               message_id: int,
               delete_for_all: bool = True
               ) -> bool:
        """Delete a message by its ID.

        Args:
            chat_id (str): The id of the user to delete the message from.
            message_id (int): The id of the message to delete.
            delete_for_all (bool): Whether to delete the message for all or not. Defaults to True.

        Returns:
            bool: Whether the message was successfully deleted.
        """
        params = {
            'peer_id': chat_id,
            'message_id': message_id,
            'delete_for_all': int(delete_for_all),
        }
        response = self.post_request('messages.delete', params)
        return response == 1

    def edit(self,
             user_id: str,
             message_id: int,
             new_text: str
             ) -> bool:
        """Edit a message by its ID.

        Args:
            user_id (str): The id of the user to edit the message from.
            message_id (int): The id of the message to edit.
            new_text (str): The new text to replace the old message with.

        Returns:
            bool: Whether the message was successfully edited.
        """
        params = {
            'peer_id': user_id,
            'cmid': message_id,
            'message': new_text,
        }
        response = self.post_request("messages.edit", params)
        return response == 1
