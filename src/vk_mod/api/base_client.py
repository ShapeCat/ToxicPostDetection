import requests
from typing import Any
from .exceptions import VKAPIError


class BaseAPIClient:
    url = 'https://api.vk.com/method/'
    api_version = "5.199"

    def __init__(self, community_token: str) -> None:
        """
        Initialize a VK API client with a community token.

        Args:
            community_token (str): The community token to use for the client.
        """
        self.community_token = community_token

    def post_request(self,
                     method: str,
                     params: dict[str, str] = {},
                     access_token: str | None = None
                     ) -> Any:
        """
        Make a POST request to VK API method.

        Args:
            method (str): VK API method name.
            params (dict[str, str]): Parameters for the request.
            access_token (str | None): The access token to use for the request. If None, the community token is used.

        Returns:
            Any: The response from the VK API.

        Raises:
            VKAPIError: If the VK API returns an error.
        """
        params.update({
            'access_token': access_token if access_token else self.community_token,
            'v': self.api_version
        })       
        response = requests.post(self.url + method, params=params)
        response.raise_for_status()
        json_response = response.json()
        
        if 'error' in json_response:
            error = json_response['error']
            raise VKAPIError(f"There is an error while calling VK API {method} method: {error['error_msg']}({error['error_code']})")
        return json_response.get('response')
    
    def get_request(self,
                    method: str,
                    params: dict[str, str] = {},
                    access_token: str | None = None
                    ) -> Any:
        """
        Make a GET request to VK API method.

        Args:
            method (str): VK API method name.
            params (dict[str, str]): Parameters for the request.
            access_token (str | None): The access token to use for the request. If None, the community token is used.

        Returns:
            Any: The response from the VK API.

        Raises:
            VKAPIError: If the VK API returns an error.
        """
        params.update({
            'access_token': access_token if access_token  else self.community_token,
            'v': self.api_version
        })       
        response = requests.get(self.url+method, params=params)
        response.raise_for_status()
        json_response = response.json()
        
        if 'error' in json_response:
            error = json_response['error']
            raise VKAPIError(f"There is an error while calling VK API {method} method: {error['error_msg']}({error['error_code']})")               
        return json_response.get('response')

